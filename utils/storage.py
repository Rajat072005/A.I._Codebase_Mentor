"""
Storage Utilities
------------------
Simple JSON read/write helpers used across the project.
"""

import json


def save_json(data, filename):
    """Save any Python object to a JSON file."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_json(filename):
    """Load a JSON file and return the parsed Python object."""
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)
