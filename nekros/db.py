import sqlite3
from contextlib import contextmanager
from .config import settings

@contextmanager
def connection():
    db = sqlite3.connect(settings.database_path)
    db.row_factory = sqlite3.Row
    try:
        yield db
        db.commit()
    finally:
        db.close()

def initialize_database():
    with connection() as db:
        db.execute("CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY, content TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT DEFAULT 'pending')")
        db.execute("CREATE TABLE IF NOT EXISTS approvals (id INTEGER PRIMARY KEY, action TEXT NOT NULL, details TEXT NOT NULL, status TEXT DEFAULT 'pending')")
