import json

def load_config() -> dict[str]:
    with open("config.json") as c:
        return json.load(c)