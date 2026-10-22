"""
llm.py

invoke llm
"""

import requests
import json
import os



class ModelInvoker:
    def __init__(self, model, HEADLESS):
        self.model = model
        self.HEADLESS = HEADLESS

    def invoke(self, msg_history, tool_catologue):
        token = os.getenv("KEY")
        data = {
            "model": self.model,
            "stream": True,
            "tools": tool_catologue,
            "messages": msg_history,
            "reasoning": {"enabled": False}
        }
        if self.HEADLESS:
            data["tool_choice"] = "required"
            data["provider"] = {"require_parameters": True}

        response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer, {token}",
            "Content-Type": "application/json",
        },
        data = json.dumps(data),
        stream=True
        )
        # print(response.text)

        rspns = ""
        tool_calls = {}
        print("\nAssistant: ", end="")
        for line in response.iter_lines():
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]  
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                delta = chunk["choices"][0]["delta"]
                if "content" in delta and delta["content"]:
                    print(delta["content"], end="", flush=True)
                    rspns += delta["content"]
                for call in delta.get("tool_calls", []):
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
