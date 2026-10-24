You will be posed a coding question. Solve it in python.

You have these tools:
- 'write_file(path, content)' writes a file.
- 'read_file(path)' reads a file you wrote.
- 'run_python(path)' runs a python file you wrote and shows its output. It only takes a path, so write the file first.

Follow these steps:

1. Write your solution to `solution.py`.

2. Write a test file `test.py` that calls your solution on EVERY example from the problem statement and prints what it got next to what was expected. For example:

```python
from solution import Solution
s = Solution()
print(s.methodName(4), "expected", 4)
print(s.methodName(15), "expected", 7)
```

3. Run `test.py` with run_python. Running `solution.py` by itself prints nothing and proves nothing, so always run `test.py`.

4. If any output differs from the expected value, or there is an error, fix `solution.py` and run `test.py` again. Repeat until every example matches.

5. When every example matches, reply with your final answer: the ENTIRE contents of `solution.py` (the version that passed), pasted into one ```python code block, with nothing after it. Include every line of the method body, not just the header. If you are unsure what is in the file, use read_file on `solution.py` first. Do not call a tool to submit.
