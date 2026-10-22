"""
read_file.py

read_file
"""


read_file_header = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "use if you want to read a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"]
        }
    }
}
def read_file(path, sandbox):
   print("reading")
   content = sandbox.read_file(path)
   return f"Content at {path}:\n{content}"

