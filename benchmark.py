"""
benchmark.py

runs each agent on each problem, grades the code in a sandbox.
problems/<name>.md + cases/<name>.json are linked by name.
"""

import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

from sandbox import Sandbox
from main import NanoLoop
from control.main import Control

DEFAULT_MODELS = ["ibm-granite/granite-4.2-8b"]
AGENTS = {
    "nanoloop": lambda model, prompt: NanoLoop(model, True, prompt),
    "control": lambda model, prompt: Control(model, prompt),
}
TIMEOUT_BUFFER = 5  # seconds on top of the problem's limit before docker kills a hung process
MAX_WORKERS = 16  # agent jobs running at once. grading is always one at a time, after all agents finish
LOG_TO_FILES = True  # each job's prints go to logs/<run>/<model>/<problem>_<agent>.log instead of the terminal
JOB_TIMEOUT = 3600  # seconds an agent job may run before it's marked AGENT_TIMEOUT and abandoned


class ThreadRouter:
    """stand-in for sys.stdout: writes from a thread with a log file set go there, everything else to the terminal"""
    def __init__(self, default):
        self.default = default
        self.local = threading.local()

    def write(self, s):
        return (getattr(self.local, "file", None) or self.default).write(s)

    def flush(self):
        (getattr(self.local, "file", None) or self.default).flush()

# runs inside the sandbox. timer starts after import so container/import overhead doesn't count
GRADER = '''
import json, sys, time
method, limit = sys.argv[1], float(sys.argv[2])
cases = json.load(open("cases.json"))
def done(**r):
    print(json.dumps(r)); sys.exit()
try:
    from solution import Solution
    fn = getattr(Solution(), method)
except Exception as e:
    done(status="ERROR", error=repr(e))
start = time.perf_counter()
for i, c in enumerate(cases):
    try:
        out = json.loads(json.dumps(fn(**c["input"])))  # tuples -> lists etc
    except Exception as e:
        done(status="ERROR", case=i, error=repr(e))
    if time.perf_counter() - start > limit:
        done(status="TIMEOUT", case=i)
    if out != c["expected"]:
        done(status="FAIL", case=i, got=str(out)[:200], expected=str(c["expected"])[:200])
done(status="PASS", seconds=round(time.perf_counter() - start, 3))
'''


def load_problems():
    problems = {}
    for md in sorted(pathlib.Path("problems").glob("*.md")):
        cases = pathlib.Path("cases") / f"{md.stem}.json"
        if not cases.exists():
            print(f"skipping {md.stem}: no cases file")
            continue
        text = md.read_text()
        problems[md.stem] = {
            "prompt": text,
            "method": re.search(r"def (\w+)\(self", text).group(1),
            "limit": float(re.search(r"\*\*Time limit:\*\* ([\d.]+)s", text).group(1)),
            "cases": cases.read_text(),
        }
    return problems


def extract_code(text):
    blocks = re.findall(r"```(?:python|py)\n(.*?)```", text or "", re.DOTALL)
    return blocks[-1] if blocks else None


def grade(problem, code):
    sandbox = Sandbox()
    try:
        sandbox.write_file("solution.py", code)
        sandbox.write_file("cases.json", problem["cases"])
        sandbox.write_file("grader.py", GRADER)
        r = subprocess.run(
            ["docker", "exec", sandbox.name, "timeout", str(problem["limit"] + TIMEOUT_BUFFER),
             "python", "grader.py", problem["method"], str(problem["limit"])],
            capture_output=True, text=True,
        )
        if r.returncode == 124:
            return {"status": "TIMEOUT", "note": "killed (hung)"}
        try:
            return json.loads(r.stdout.strip().splitlines()[-1])
        except (IndexError, json.JSONDecodeError):
            return {"status": "ERROR", "error": (r.stdout + r.stderr)[-500:]}
    finally:
        sandbox.kill()


def run_agent(make_agent, model, problem, log_path=None, agents=None, key=None):
    """runs one agent on one problem. returns (error result or None, final text)"""
    log = open(log_path, "w") if log_path else None
    if log:
        sys.stdout.local.file = log
    agent = None
    try:
        agent = make_agent(model, problem["prompt"])
        if agents is not None:
            agents[key] = agent  # so main() can kill its sandbox if the job is abandoned
        return None, agent.start()
    except Exception as e:  # agent crashed (e.g. bad tool call); don't kill the whole run
        return {"status": "AGENT_ERROR", "error": repr(e)}, None
    finally:
        if hasattr(agent, "sandbox"):
            agent.sandbox.kill()
        if log:
            sys.stdout.local.file = None
            log.close()


def main(models=None):
    models = models or sys.argv[1:] or DEFAULT_MODELS
    problems = load_problems()
    run_id = time.strftime("%Y%m%d-%H%M%S")
    out = pathlib.Path("results") / f"{run_id}.json"
    out.parent.mkdir(exist_ok=True)
    results = {m: {name: {} for name in problems} for m in models}
    lock = threading.Lock()

    def save():
        with lock:
            out.write_text(json.dumps({"models": models, "results": results}, indent=2))

    if LOG_TO_FILES and not isinstance(sys.stdout, ThreadRouter):
        sys.stdout = ThreadRouter(sys.stdout)

    started, agents = {}, {}

    def job(model, name, agent_name):
        started[(model, name, agent_name)] = time.time()
        log_path = None
        if LOG_TO_FILES:
            log_dir = pathlib.Path("logs") / run_id / model.replace("/", "__")
            log_dir.mkdir(parents=True, exist_ok=True)
            log_path = log_dir / f"{name}_{agent_name}.log"
        return run_agent(AGENTS[agent_name], model, problems[name], log_path, agents, (model, name, agent_name))

    # phase 1: all agents on all problems, in parallel
    jobs = [(m, name, a) for m in models for name in problems for a in AGENTS]
    print(f"running {len(jobs)} agent jobs ({len(models)} models x {len(problems)} problems x {len(AGENTS)} agents), {MAX_WORKERS} at a time")
    pool = ThreadPoolExecutor(MAX_WORKERS)
    futures = {pool.submit(job, *j): j for j in jobs}
    pending, done, abandoned = set(futures), 0, []
    while pending:
        finished, pending = wait(pending, timeout=10, return_when=FIRST_COMPLETED)
        # threads can't be killed: a job over JOB_TIMEOUT is recorded and no longer waited on
        overdue = [f for f in pending if futures[f] in started and time.time() - started[futures[f]] > JOB_TIMEOUT]
        for f in overdue:
            pending.discard(f)
            abandoned.append(futures[f])
        for f in list(finished) + overdue:
            m, name, a = futures[f]
            error, text = f.result() if f in finished else ({"status": "AGENT_TIMEOUT"}, None)
            with lock:
                results[m][name][a] = dict(error or {"status": "UNGRADED"}, output=text)
            save()
            done += 1
            print(f"[{done}/{len(jobs)}] {m} / {name} / {a}: {(error or {}).get('status', 'done')}")
    pool.shutdown(wait=False)

    # phase 2: grade one at a time so solutions don't compete for CPU
    print("grading...")
    for m in models:
        for name, problem in problems.items():
            for a in AGENTS:
                r = results[m][name][a]
                if r["status"] != "UNGRADED":
                    continue
                code = extract_code(r["output"])
                if code is None:
                    r.update(status="NO_CODE")
                else:
                    r.update(grade(problem, code), output=code)
                save()

    width = max(map(len, models))
    print("\n" + "model".ljust(width) + "".join(a.rjust(12) for a in AGENTS))
    for m in models:
        print(m.ljust(width) + "".join(
            f"{sum(row[a]['status'] == 'PASS' for row in results[m].values())}/{len(problems)}".rjust(12) for a in AGENTS))

    print(f"\nsaved {out}")

    if abandoned:  # their threads are still running: kill their sandboxes and exit without waiting on them
        for k in abandoned:
            if hasattr(agents.get(k), "sandbox"):
                agents[k].sandbox.kill()
        sys.stdout.flush()
        os._exit(0)


if __name__ == "__main__":
    main()
