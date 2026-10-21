"""
write_file.py

write_file
"""


write_file_header = {
    "type": "function",
    "function": {
        "name": "write-file",
        "description": "use if you want to write a file",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "content": {"type": "string"}
            },
            "required": ["path", "contents"]
        }
    }
}
def write_file_header(arguments):
   sandbox.write_file(path, content)
   return