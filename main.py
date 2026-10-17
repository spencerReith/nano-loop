"""
main.py

core query loop
"""

import ast
from llm import invoke_llm 
from dotenv import load_dotenv 


load_dotenv()


###### build tool catalogue
from tool_definitions.get_weather import get_weather, get_weather_header
from tool_definitions.get_population import get_population, get_population_header

tool_map = {
    "get_weather": {"path": "tool_definitions/get_weather.py", "function": get_weather},
    "get_population": {"path": "tool_definitions/get_population.py", "function": get_population},
}
tool_catologue = [get_weather_header, get_population_header]
#################################################################

###### processing tool calls
def use_tool(cleaned_tool_call):
    func = tool_map[cleaned_tool_call["name"]]["function"]
    res = func(cleaned_tool_call["arguments"])
    tool_response_block = {"role": "tool", "tool_call_id": cleaned_tool_call["id"], "content": res}
    return tool_response_block
##############################################################################


###### init msg history
msg_history = []
system_prompt = "You answer everything extremely clearly and concisely"
msg_history.append({"role": "system", "content": system_prompt})
##############################################################################


class NanoLoop:
    def __init__(self, HEADLESS):
        self.HEADLESS = HEADLESS
        self.tool_catologue = [get_weather_header, get_population_header]

    def start(self):
        LOOPING = True
        ASK_INPUT = True
        while LOOPING:
            if ASK_INPUT:
                user_msg = input("\nUser: ")
                msg_history.append({"role": "user", "content": user_msg})
            response_block, tool_calls = invoke_llm(msg_history, self.tool_catologue, self.HEADLESS)
            msg_history.append(response_block)

            if tool_calls:
                for idx in tool_calls.keys():
                    cleaned_tool_call = {
                        "id": tool_calls[idx]['id'],
                        "name": tool_calls[idx]['function']['name'],
                        "arguments": ast.literal_eval(tool_calls[idx]['function']['arguments'])
                    }
                    tool_response_block = use_tool(cleaned_tool_call)
                    msg_history.append(tool_response_block)
                ASK_INPUT = False
                continue

            ASK_INPUT = True

nano_loop()