import json
import os

class FileBackedKeyValuesStore:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)

    def save(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)

    def set(self, key: str, value: str):
        self.data[key] = value
        self.save()

    def contains(self, key: str) -> bool:
        return key in self.data

    def get(self, key: str) -> str | None:
        return self.data.get(key)

    def delete(self, key: str):
        if key in self.data:
            del self.data[key]
            self.save()