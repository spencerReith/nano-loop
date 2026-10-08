"""
llm.py

invoke llm
"""

import requests
import json
import os

from tool_map import tool_catologue



def invoke_llm(msg_history: list[dict]):
    ## Make post to OpenRouter
    token = os.getenv("KEY")
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer, {token}",
        "Content-Type": "application/json",
    },
    data=json.dumps({
        "model": "moonshotai/kimi-k3",
        "stream": True,
        "tools": tool_catologue,
        "messages": msg_history,
        "reasoning": {"enabled": False}
    }),
    stream=True
    )

    ## Stream response, return response block
    rspns = ""
    tool_calls = {}
    print("Assistant: ", end="")
    for line in response.iter_lines():
        line = line.decode("utf-8")
        if line.startswith("data: "):
            data = line[6:]  
            if data == "[DONE]":
                break
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]: ## msg content
                print(delta["content"], end="", flush=True)
                rspns += delta["content"]
            for call in delta.get("tool_calls", []): ## tool calls
                i = call["index"]
                if i not in tool_calls:
                    tool_calls[i] = {
                        "id": call.get("id"),
                        "type": "function",
                        "function": {
                            "name": call["function"].get("name", ""),
                            "arguments": ""
                        }
                    }
                tool_calls[i]["function"]["arguments"] += call["function"].get("arguments", "")
    
    response_block = {"role": "assistant", "content": rspns}
    if tool_calls:
        response_block["tool_calls"] = list(tool_calls.values())
    return (response_block, tool_calls)
