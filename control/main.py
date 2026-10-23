"""
main.py

single-turn llm call
"""
from llm import ModelInvoker
from dotenv import load_dotenv


load_dotenv()

class Control:
    def __init__(self, model, prompt):
        self.model_invoker = ModelInvoker(model)
        self.prompt = prompt

    def start(self):
        response_block, _ = self.model_invoker.invoke([{"role": "system", "content": "You will be posed a coding question. Return the answer and only the answer in python."}, {"role": "user", "content": self.prompt}], [])
        return response_block["content"]
