import json
import os
def load_config():
    if os.path.exists("config.json"):
        with open("config.json","r") as file:
            config = json.load(file)
            return config
    else:
        raise FileNotFoundError
