"""
submit.py

submit
"""


submit_header = {
    "type": "function",
    "function": {
        "name": "submit",
        "description": "Use to submit final answer",
        "parameters": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"}
            },
            "required": ["answer"]
        }
    }
}
def submit(arguments):
   print("submiting")
   return arguments