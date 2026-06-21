import shelve
from pathlib import Path

class DataStore:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent.resolve()
        self.data_store_file = self.base_dir / "xray_config" / "db" / "data_store.db"
    
    def _open_data_store(self):
        return shelve.open(self.data_store_file)

    def insert(self, key, value):
        with self._open_data_store() as db:
            if not key in db:
                db[key] = value
    
    def get(self, key):
        with self._open_data_store() as db:
            return db.get(key, None)
