"""
main.py

core query loop
"""

import ast


from llm import invoke_llm 
from dotenv import load_dotenv 

from tool_map import tool_map


load_dotenv()

msg_history = []

system_prompt = "You answer everything extremely clearly and concisely"
msg_history.append({"role": "system", "content": system_prompt})



def process(cleaned_tool_call):
    print("\n### processing tool call\n####")
    func = tool_map[cleaned_tool_call["name"]]["function"]
    res = func(cleaned_tool_call["arguments"])
    tool_response_block = {"role": "tool", "tool_call_id": cleaned_tool_call["id"], "content": res}
    print(tool_response_block)



def chat_loop():
    user_msg = input("\nUser: ")
    msg_history.append({"role": "user", "content": user_msg})

    response_block, tool_calls = invoke_llm(msg_history)

    msg_history.append(response_block)
    if tool_calls: msg_history.append({"role": "assistant", "tool_calls": tool_calls.values()})

    print(f"\n##############################\nMSG HISTORY:\n##############################\n{msg_history}\n##############################\n")

    if tool_calls:
        print('\n### processing tool call \n')
        for idx in tool_calls.keys():
            print(tool_calls[idx])
            cleaned_tool_call = {
                "id": tool_calls[idx]['id'],
                "name": tool_calls[idx]['function']['name'],
                "arguments": ast.literal_eval(tool_calls[idx]['function']['arguments'])
            }
            # print(cleaned_tool_call)
            process(cleaned_tool_call)

    msg_history.append(response_block)
    chat_loop()

chat_loop()