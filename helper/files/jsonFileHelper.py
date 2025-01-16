import json
import os


class JsonFileHelper:
    @staticmethod
    def read_json_file(file_path: str) -> dict:
        if not os.path.exists(file_path):
            return {}

        with open(file_path, 'r') as file:
            return json.load(file)

    @staticmethod
    def write_json_file(file_path: str, data: dict):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
