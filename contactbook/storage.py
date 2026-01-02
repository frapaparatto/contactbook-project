
import os
import json
from typing import Dict, Protocol
from .contact_exceptions import StorageError, FileCorruptionError


class Storage(Protocol):
    def save(self, data: Dict[str, dict], path: str): ...
    def load(self, path: str) -> Dict[str, dict]: ...


class JsonStorage:
    def save(self, data: Dict[str, dict], path: str) -> None:
        if not path:
            raise StorageError("Save path is empty.")

        # ensure the directory exists
        dirpath = os.path.dirname(path) or "."

        try:
            os.makedirs(dirpath, exist_ok=True)
            # first open a file and then in that file write data
            with open(path, "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            raise StorageError(f"Could not save the file to'{path}': {e}") from e


    def load(self, path: str) -> Dict[str, dict]:
        if not path or not os.path.exists(path):
            raise StorageError(f"File '{path}' not found.")

        if os.path.getsize(path) == 0:
            return {}
            
        try:
            with open(path, "r") as contacts_file:
                data = json.load(contacts_file)

        except json.JSONDecodeError as e:
            raise FileCorruptionError("Invalid JSON file.") from e

        if not isinstance(data, dict):
            raise FileCorruptionError("Invalid format, expected a dict of contacts")

        return data

