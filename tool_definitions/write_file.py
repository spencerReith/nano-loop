"""
write_file.py

write_file
"""


write_file_header = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "use if you want to write a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "content"]
        }
    }
}
def write_file(path, content, sandbox):
   print("writing")
   sandbox.write_file(path, content)
   return f"Content written to {path}"

