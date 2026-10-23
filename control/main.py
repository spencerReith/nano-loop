"""
main.py

single-turn llm call
"""
from llm import ModelInvoker
from dotenv import load_dotenv


load_dotenv()

class Control:
    def __init__(self, model):
        self.model_invoker = ModelInvoker(model, False)

    def start(self, prompt):
        res = self.model_invoker.invoke([{"role": "user", "content": prompt}], [])
        print(res)


control = Control("ibm-granite/granite-4.2-8b")
control.start("hello, tell me ur name")