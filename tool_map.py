"""
tool_map.py

mapping of tool names to function names
"""
from tool_definitions.get_weather import get_weather, get_weather_header
from tool_definitions.get_population import get_population, get_population_header

tool_map = {
    "get_weather": {"path": "tool_definitions/get_weather.py", "function": get_weather},
    "get_population": {"path": "tool_definitions/get_population.py", "function": get_population},
}

## catologue
tool_catologue = [get_weather_header, get_population_header]