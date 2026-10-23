"""
main.py

core query loop
"""

import ast
from dotenv import load_dotenv 
from functools import partial


load_dotenv()



from tool_definitions.get_weather import get_weather, get_weather_header
from tool_definitions.get_population import get_population, get_population_header
from tool_definitions.write_file import write_file, write_file_header
from tool_definitions.read_file import read_file, read_file_header
from tool_definitions.run_python import run_python, run_python_header
from tool_definitions.submit import submit, submit_header
from llm import ModelInvoker
from sandbox import Sandbox

SOLVER_PROMPT = open("system_prompts/solver.md").read()



class ToolProcessor:
    def __init__(self, sandbox):
        self.tool_map = {
                        "get_weather": {"path": "tool_definitions/get_weather.py", "function": get_weather},
                        "get_population": {"path": "tool_definitions/get_population.py", "function": get_population},
                        "write_file": {"path": "tool_definitions/write_file.py", "function": partial(write_file, sandbox=sandbox)},
                        "read_file": {"path": "tool_definitions/read_file.py", "function": partial(read_file, sandbox=sandbox)},
                        "run_python": {"path": "tool_definitions/run_python.py", "function": partial(run_python, sandbox=sandbox)},
                        "submit": {"path": "tool_definitions/submit.py", "function": submit},
                        }
    
    def use_tool(self, cleaned_tool_call):
        func = self.tool_map[cleaned_tool_call["name"]]["function"]
        print(f"[{cleaned_tool_call['name']}] args: {str(cleaned_tool_call['arguments'])[:300]}")
        res = func(**cleaned_tool_call["arguments"])
        print(f"[{cleaned_tool_call['name']}] result: {str(res)[:500]}")
        tool_response_block = {"role": "tool", "tool_call_id": cleaned_tool_call["id"], "content": f"{res}"}
        return tool_response_block



class NanoLoop:
    def __init__(self, HEADLESS, prompt=""):
        self.HEADLESS = HEADLESS
        
        self.msg_history = [{"role": "system", "content": SOLVER_PROMPT}]
        if self.HEADLESS: self.msg_history.append({"role": "user", "content": prompt})
        
        self.tool_catologue = [get_weather_header, get_population_header, write_file_header, read_file_header, run_python_header]
        if self.HEADLESS: self.tool_catologue.append(submit_header)
        
        self.sandbox = Sandbox()
        self.tool_processor = ToolProcessor(self.sandbox)
        # self.model_invoker = ModelInvoker("moonshotai/kimi-k3", HEADLESS)
        self.model_invoker = ModelInvoker("ibm-granite/granite-4.2-8b", HEADLESS)

    def start(self):
        LOOPING = True
        ASK_INPUT = True
        if self.HEADLESS: ASK_INPUT = False

        while LOOPING:
            if ASK_INPUT:
                user_msg = input("\nUser: ")
                self.msg_history.append({"role": "user", "content": user_msg})
            response_block, tool_calls = self.model_invoker.invoke(self.msg_history, self.tool_catologue)
            self.msg_history.append(response_block)
            if tool_calls:
                for idx in tool_calls.keys():
                    cleaned_tool_call = {
                        "id": tool_calls[idx]['id'],
                        "name": tool_calls[idx]['function']['name'],
                        "arguments": ast.literal_eval(tool_calls[idx]['function']['arguments'])
                    }
                    tool_response_block = self.tool_processor.use_tool(cleaned_tool_call)
                    if cleaned_tool_call["name"] == "submit":
                        return tool_response_block
                    self.msg_history.append(tool_response_block)
                ASK_INPUT = False
                continue

            ASK_INPUT = True

# myLoop = NanoLoop(True, "what is gaurdians of the galaxy. also whats the weather in philly. also whats the poplaton in tianemen sauare.s. also pls write it to a file using ur tool.")
# print(myLoop.start())



PALINDROMIC_OPS = open("problems/palindromic_ops.md").read()
SHADOW_PAIRS = open("problems/shadow_pairs.md").read()
ALTERNATING_SUM_DELETION = open("problems/alternating_sum_deletion.md").read()

myLoop2 = NanoLoop(True, ALTERNATING_SUM_DELETION)
print(myLoop2.start())