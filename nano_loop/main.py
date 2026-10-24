"""
main.py

core query loop
"""

import ast
import json
from dotenv import load_dotenv
from functools import partial


load_dotenv()

from nano_loop.tool_definitions.write_file import write_file, write_file_header
from nano_loop.tool_definitions.read_file import read_file, read_file_header
from nano_loop.tool_definitions.run_python import run_python, run_python_header
from shared.llm import ModelInvoker
from shared.sandbox import Sandbox

SOLVER_PROMPT = open("nano_loop/system_prompts/solver_v2.md").read()



class ToolProcessor:
    def __init__(self, sandbox):
        self.tool_map = {
                        "get_weather": {"path": "nano_loop/tool_definitions/get_weather.py", "function": get_weather},
                        "get_population": {"path": "nano_loop/tool_definitions/get_population.py", "function": get_population},
                        "write_file": {"path": "nano_loop/tool_definitions/write_file.py", "function": partial(write_file, sandbox=sandbox)},
                        "read_file": {"path": "nano_loop/tool_definitions/read_file.py", "function": partial(read_file, sandbox=sandbox)},
                        "run_python": {"path": "nano_loop/tool_definitions/run_python.py", "function": partial(run_python, sandbox=sandbox)},
                        "submit": {"path": "nano_loop/tool_definitions/submit.py", "function": submit},
                        }
    
    def use_tool(self, cleaned_tool_call):
        func = self.tool_map[cleaned_tool_call["name"]]["function"]
        print(f"[{cleaned_tool_call['name']}] args: {str(cleaned_tool_call['arguments'])[:300]}")
        res = func(**cleaned_tool_call["arguments"])
        print(f"[{cleaned_tool_call['name']}] result: {str(res)[:500]}")
        tool_response_block = {"role": "tool", "tool_call_id": cleaned_tool_call["id"], "content": f"{res}"}
        return tool_response_block



class NanoLoop:
    def __init__(self, model, HEADLESS, prompt=""):
        self.HEADLESS = HEADLESS
        
        self.msg_history = [{"role": "system", "content": SOLVER_PROMPT}]
        if self.HEADLESS: self.msg_history.append({"role": "user", "content": prompt})
        
        self.tool_catologue = [write_file_header, read_file_header, run_python_header]
        
        self.sandbox = Sandbox()
        self.tool_processor = ToolProcessor(self.sandbox)
        self.model_invoker = ModelInvoker(model)

    def start(self):
        LOOPING = True
        ASK_INPUT = True
        if self.HEADLESS: ASK_INPUT = False

        turns = 0
        empty_calls = 0
        while LOOPING:
            if ASK_INPUT:
                user_msg = input("\nUser: ")
                self.msg_history.append({"role": "user", "content": user_msg})
            response_block, tool_calls = self.model_invoker.invoke(self.msg_history, self.tool_catologue)
            self.msg_history.append(response_block)
            turns += 1
            empty_calls = empty_calls + 1 if not tool_calls and not response_block["content"].strip() else 0
            if self.HEADLESS and empty_calls == 3:
                return ""
            if self.HEADLESS and turns == 50:
                return response_block["content"]
            if tool_calls:
                for idx in tool_calls.keys():
                    try:
                        cleaned_tool_call = {
                            "id": tool_calls[idx]['id'],
                            "name": tool_calls[idx]['function']['name'],
                            "arguments": json.loads(tool_calls[idx]['function']['arguments'])
                        }
                        tool_response_block = self.tool_processor.use_tool(cleaned_tool_call)
                    except Exception as e:
                        tool_response_block = {"role": "tool", "tool_call_id": tool_calls[idx]['id'], "content": f"Tool call failed: {e!r}. Fix it and try again."}
                    self.msg_history.append(tool_response_block)
                ASK_INPUT = False
                continue

            if self.HEADLESS:
                if "```" in (response_block["content"] or ""):   # has a final code block -> done
                    return response_block["content"]
                self.msg_history.append({"role": "user", "content": "Continue. Use your tools, and when you're done reply with the full solution.py in one ```python block."})
                continue
            ASK_INPUT = True
