"""
main.py

core query loop
"""

import ast
from dotenv import load_dotenv 


load_dotenv()



from tool_definitions.get_weather import get_weather, get_weather_header
from tool_definitions.get_population import get_population, get_population_header
from tool_definitions.submit import submit, submit_header
from llm import ModelInvoker


class ToolProcessor:
    def __init__(self):
        self.tool_map = {
                        "get_weather": {"path": "tool_definitions/get_weather.py", "function": get_weather},
                        "get_population": {"path": "tool_definitions/get_population.py", "function": get_population},
                        "submit": {"path": "tool_definitions/submit.py", "function": submit},
                        }
    
    def use_tool(self, cleaned_tool_call):
        func = self.tool_map[cleaned_tool_call["name"]]["function"]
        res = func(cleaned_tool_call["arguments"])
        tool_response_block = {"role": "tool", "tool_call_id": cleaned_tool_call["id"], "content": res}
        return tool_response_block



class NanoLoop:
    def __init__(self, HEADLESS, prompt=""):
        self.HEADLESS = HEADLESS
        
        self.msg_history = [{"role": "system", "content": "You answer everything extremely clearly and concisely"}]
        if self.HEADLESS: self.msg_history.append({"role": "user", "content": prompt})
        
        self.tool_catologue = [get_weather_header, get_population_header]
        if self.HEADLESS: self.tool_catologue.append(submit_header)
        
        self.tool_processor = ToolProcessor()
        self.model_invoker = ModelInvoker("moonshotai/kimi-k3", HEADLESS)

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

myLoop = NanoLoop(True, "what is gaurdians of the galaxy. also whats the weather in philly. also whats the poplaton in tianemen sauare.s")
print(myLoop.start())