"""
get_weather.py

made up weather
"""

get_weather_header = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "use if you want to get the weather at a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}
def get_weather(location):
    return "it is sunny"