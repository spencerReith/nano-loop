"""
get_population.py

get_population
"""


get_population_header = {
    "type": "function",
    "function": {
        "name": "get_population",
        "description": "use if you want to get the population at a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }
}
def get_population(arguments):
   return "population is 5"