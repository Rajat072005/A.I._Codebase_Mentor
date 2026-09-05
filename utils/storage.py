

import json

def save_json(data, filename):

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def load_json(filename):

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
