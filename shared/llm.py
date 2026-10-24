"""
llm.py

invoke llm
"""

import requests
import json
import os



class ModelInvoker:
    def __init__(self, model):
        self.model = model


    def invoke(self, msg_history, tool_catologue):
        token = os.getenv("KEY")
        data = {
            "model": self.model,
            "stream": True,
            "tools": tool_catologue,
            "messages": msg_history,
            "reasoning": {"enabled": False}
        }
        # if self.REQUIRE_TOOLS:
        #     data["tool_choice"] = "required"
        #     data["provider"] = {"require_parameters": True}

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
        finish_reason, provider, usage, reasoning_chars = None, None, None, 0
        print("\nAssistant: ", end="")
        for line in response.iter_lines():
            line = line.decode("utf-8")
            if line.startswith("data: "):
                data = line[6:]  
                if data == "[DONE]":
                    break
                chunk = json.loads(data)
                if "error" in chunk:
                    print(f"\n[stream error] {chunk['error']}")
                provider = chunk.get("provider", provider)
                usage = chunk.get("usage", usage)
                if not chunk.get("choices"):
                    continue
                delta = chunk["choices"][0]["delta"]
                finish_reason = chunk["choices"][0].get("finish_reason") or finish_reason
                reasoning_chars += len(delta.get("reasoning") or "")
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
        
        print(f"\n[finish_reason: {finish_reason} | provider: {provider} | reasoning chars: {reasoning_chars} | usage: {usage}]")
        response_block = {"role": "assistant", "content": rspns}
        if tool_calls:
            response_block["tool_calls"] = list(tool_calls.values())
        return (response_block, tool_calls)
