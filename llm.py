"""
llm.py

invoke llm
"""

import requests
import json
from dotenv import load_dotenv
import os


load_dotenv()


def invoke_llm(msg: str):
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
        "messages": [
            {
            "role": "user",
            "content": msg
            }
        ],
        "reasoning": {"enabled": False}
    }),
    stream=True
    )

    ## Stream response
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
    print("\n")

invoke_llm("hi")