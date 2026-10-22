"""
run_python.py

run_python
"""


run_python_header = {
    "type": "function",
    "function": {
        "name": "run_python",
        "description": "use if you want to run python",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"]
        }
    }
}
def run_python(path, sandbox):
   print("running python")
   res = sandbox.run_python(path)
   return f"Result running {path}: {res}"

