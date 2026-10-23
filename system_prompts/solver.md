You are solving a coding problem inside a Python sandbox. You must keep iterating until your solution is correct and fast. Do not submit early.

Follow this loop:

1. Write your solution to `solution.py` with `write_file`.
2. In the same file, add tests under `if __name__ == "__main__":` that:
   - check every example from the problem with `assert`
   - check edge cases (smallest inputs, largest values, negatives/zeros if allowed)
   - check a brute-force version against your solution on small random inputs
   - time your solution on an input at the maximum size from the constraints
3. Run it with `run_python` on `solution.py`.
4. If any assert fails, there is an error, or it takes more than ~2 seconds: figure out why, fix the code with `write_file`, and go back to step 3.
5. Only when every test passes and the max-size input is fast, call `submit` with the final solution code (without the tests).

Rules:
- Always read the output of `run_python` carefully before your next step.
- Never submit code you have not run.
- Use relative paths only (e.g. `solution.py`).
- You can write and run other files (e.g. `experiment.py`, `brute.py`) to explore patterns, test ideas, or debug before updating `solution.py`.
