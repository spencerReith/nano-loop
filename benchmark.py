"""
benchmark.py

runs each agent on each problem, grades the code in a sandbox.
problems/<name>.md + cases/<name>.json are linked by name.
"""

import json
import pathlib
import re
import subprocess
import time

from sandbox import Sandbox
from main import NanoLoop
from control.main import Control

MODEL = "ibm-granite/granite-4.2-8b"
AGENTS = {
    "nanoloop": lambda prompt: NanoLoop(MODEL, True, prompt),
    "control": lambda prompt: Control(MODEL, prompt),
}
TIMEOUT_BUFFER = 5  # seconds on top of the problem's limit before docker kills a hung process

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


def run_agent(make_agent, problem):
    agent = make_agent(problem["prompt"])
    try:
        text = agent.start()
    except Exception as e:  # agent crashed (e.g. bad tool call); don't kill the whole run
        return {"status": "AGENT_ERROR", "error": repr(e)}, None
    finally:
        if hasattr(agent, "sandbox"):
            agent.sandbox.kill()
    code = extract_code(text)
    if code is None:
        return {"status": "NO_CODE"}, text
    return grade(problem, code), code


def main():
    problems = load_problems()
    out = pathlib.Path("results") / f"{time.strftime('%Y%m%d-%H%M%S')}.json"
    out.parent.mkdir(exist_ok=True)
    results = {}
    for name, problem in problems.items():
        results[name] = {}
        for agent_name, make_agent in AGENTS.items():
            print(f"\n=== {name} / {agent_name} ===")
            result, output = run_agent(make_agent, problem)
            result["output"] = output
            results[name][agent_name] = result
            print(f"\n-> {result['status']}")
            out.write_text(json.dumps({"model": MODEL, "results": results}, indent=2))  # save as we go

    width = max(map(len, results))
    print("\n" + "problem".ljust(width) + "".join(a.rjust(12) for a in AGENTS))
    for name, row in results.items():
        print(name.ljust(width) + "".join(row[a]["status"].rjust(12) for a in AGENTS))
    print("passed".ljust(width) + "".join(
        f"{sum(row[a]['status'] == 'PASS' for row in results.values())}/{len(results)}".rjust(12) for a in AGENTS))

    print(f"\nsaved {out}")


if __name__ == "__main__":
    main()
