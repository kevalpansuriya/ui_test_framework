import json

def load_config():
    with open('data/test_data.json') as f:
        return json.load(f)
