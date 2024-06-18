import json

def save_to_json(file_path: str, _dict: dict) -> None:
    with open(file_path, 'w') as fp:
        json.dump(_dict, fp)