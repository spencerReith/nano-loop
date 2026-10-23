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
        
        self.tool_catologue = [write_file_header, read_file_header, run_python_header]
        # if self.HEADLESS: self.tool_catologue.append(submit_header)
        
        self.sandbox = Sandbox()
        self.tool_processor = ToolProcessor(self.sandbox)
        # self.model_invoker = ModelInvoker("moonshotai/kimi-k3", HEADLESS)
        self.model_invoker = ModelInvoker("ibm-granite/granite-4.2-8b")

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
                    self.msg_history.append(tool_response_block)
                ASK_INPUT = False
                continue

            if self.HEADLESS:
                return response_block
            ASK_INPUT = True

# myLoop = NanoLoop(True, "what is gaurdians of the galaxy. also whats the weather in philly. also whats the poplaton in tianemen sauare.s. also pls write it to a file using ur tool.")
# print(myLoop.start())



PALINDROMIC_OPS = open("problems/palindromic_ops.md").read()
SHADOW_PAIRS = open("problems/shadow_pairs.md").read()
ALTERNATING_SUM_DELETION = open("problems/alternating_sum_deletion.md").read()
MINIMUM_DELETIONS_TO_MAKE_ARRAY_SHARP = open("problems/minimum_deletions_to_make_array_sharp.md").read()
MAXIMUM_PRODUCT_PAIR_WITH_TARGET_SUM = open("problems/maximum_product_pair_with_target_sum.md").read()
REARRANGE_ARRAY_BY_REMOVING_DISTINCT_VALUES = open("problems/rearrange_array_by_removing_distinct_values.md").read()
COUNT_VALUES_WITH_EQUALLY_SPACED_OCCURRENCES_I = open("problems/count_values_with_equally_spaced_occurrences_i.md").read()
CHECK_ASCII_PALINDROMIC = open("problems/check_ascii_palindromic.md").read()
LAST_VISITED_CELL_IN_A_DIRECTIONAL_GRID = open("problems/last_visited_cell_in_a_directional_grid.md").read()
MAXIMUM_EQUAL_ADJACENT_PAIRS_AFTER_AT_MOST_ONE_REPLACEMENT = open("problems/maximum_equal_adjacent_pairs_after_at_most_one_replacement.md").read()
TRANSFORM_ARRAY_USING_PAIR_OPERATIONS = open("problems/transform_array_using_pair_operations.md").read()
COUNT_GOOD_CYCLIC_ROTATIONS = open("problems/count_good_cyclic_rotations.md").read()
K_TH_DIGIT_IN_INFINITE_STRING = open("problems/k_th_digit_in_infinite_string.md").read()

myLoop2 = NanoLoop(True, K_TH_DIGIT_IN_INFINITE_STRING)
print(myLoop2.start())