# Singleton & FR9 & FR10

import json

class FileManager:
    _instance = None
    _file = "tasks.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance

    def save_tasks(self, tasks):
        with open(self._file, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=4, ensure_ascii=False)

    def load_tasks(self):
        try:
            with open(self._file, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
