# Kimi + Granite runs, 2026-10-23

## Runs involved

| Run ID | What | Status |
|---|---|---|
| `20261023-203756` | Kimi-k3 + granite-4.2-8b, all 102 problems, 8 workers | **Stopped by hand** after 101 Kimi jobs; granite never started |
| `20261023-211822` | Re-run: 111 Kimi jobs (see below) + all 204 granite jobs, 8 workers | The run to use for those jobs |

Results: `results/<run id>.json`. Logs: `logs/<run id>/<model>/<problem>_<agent>.log`.

## What happened in `20261023-203756`

- About 20:48 into the run, Kimi requests started coming back **completely empty**: no text and no tool call.
  Jobs that started and finished before then had none. After that point, even single-call control jobs got empty replies.
  This looks like a provider-side problem. It couldn't be confirmed at the time because the provider wasn't logged.
- NanoLoop had a new "no tool call and no code block → send *Continue…*" nudge with **no cap**, so each empty reply
  triggered another call. 7 nanoloop jobs looped **~1,000–2,300 times each**.
  Overall that came to 9,765 of 10,040 model calls being empty.
- Every call resends the whole conversation. That is roughly 300M input tokens resent, which explains the spend.
  Visible output was only ~0.5M tokens, so hidden reasoning tokens were **not** the cause.
- **Cost:** about **$56 for 101 Kimi jobs**. The earlier clean run (`20261023-011152`) cost $11.23 for 136 jobs.
- Ctrl+C did not stop the worker threads. The process had to be killed.

Of the 16 jobs that got empty replies:
- 8 were stuck looping when the run was killed, so they have no result.
- 5 were control jobs with a single empty reply, which grade as NO_CODE.
- 3 nanoloop jobs recovered and finished with an answer.

## Fixes made afterwards

- `main.py` (`NanoLoop.start`, headless only):
  - 3 empty replies in a row → return `""`.
  - Hard cap of **50 turns**.
- `llm.py`: every call now logs `finish_reason`, `provider`, reasoning chars, and `usage` (tokens + cost).
- A single test call afterwards came back normal: provider Wafer, `finish_reason: tool_calls`, 0 reasoning tokens.

## Re-run (`20261023-211822`)

Kimi jobs re-run: **111** = 8 stuck + 8 that finished but had empty replies + 95 never started.
Every other Kimi job is marked `SKIPPED` in this run's results.
The exact list is the set of `(problem, agent)` pairs whose status is not `SKIPPED` in `20261023-211822`.
Granite: all 204 jobs, in this run only.

The re-run used the same code as the stopped run, plus the fixes above. Note that the 93 Kimi jobs kept from the stopped run
ran *before* those fixes; they had no empty replies, so the fixes wouldn't have changed them.

## How to get the full Kimi results

For each `(problem, agent)`:
1. take it from `20261023-211822` if its status there is not `SKIPPED`,
2. otherwise take it from `20261023-203756`.

The 93 jobs taken from `20261023-203756` were still **ungraded** when that run was stopped. Grade them separately,
using `grade()` from `benchmark.py` on each saved output, before comparing.

**Done:** the 93 earlier jobs were graded and merged into **`results/20261023-merged-kimi-granite.json`**.
Every entry there has a `from_run` field.

## Re-run outcome

- No truly empty replies.
- No agent errors and no 1-hour timeouts.
- API errors:
  - 4× 504 provider idle timeouts. The jobs survived them.
  - 3× 400 "context too long" in one granite job. DeepInfra rejected a prompt over ~65k tokens because 65,536 output tokens are requested by default. The job ended via the empty-reply cutoff.
- Cost: Kimi ~$15, granite ~$1.

## Results (102 problems: 66 Medium, 36 Hard)

| Model | nanoloop | control | only nanoloop | only control |
|---|---|---|---|---|
| kimi-k3 | **90 (88%)** | 63 (61%) | 34 | 7 |
| granite-4.2-8b | **58 (56%)** | 50 (49%) | 15 | 7 |

Kimi on Hard problems: nanoloop 83% vs control 44%.

### Contamination check (by problem ID / date)

- Kimi was listed 2026-07-16. Its control pass rate is 76% on the oldest problems (IDs 3932–3987, published before its release)
  and 41–62% on newer ones. That is a possible memorization effect on the oldest batch, so compare the loop gain on IDs ≥ 4010 for the cleanest signal.
- Granite was listed 2026-08-31. Its pass rate is flat (~50%) across the date buckets, which shows no sign of memorization.
