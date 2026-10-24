"""
main.py

single-turn llm call
"""
from shared.llm import ModelInvoker
from dotenv import load_dotenv


load_dotenv()

SYSTEM_PROMPT = """You will be posed a coding question.

When you are done, output your answer as one Python code block.
The code block must contain the full `class Solution` with the exact method header given in the problem.

Example of the required format:

```python
class Solution:
    def methodName(self, x: int) -> int:
        ...
```"""

class Control:
    def __init__(self, model, prompt):
        self.model_invoker = ModelInvoker(model)
        self.prompt = prompt

    def start(self):
        response_block, _ = self.model_invoker.invoke([{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": self.prompt}], [])
        return response_block["content"]
