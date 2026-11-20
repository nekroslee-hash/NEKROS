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
        db.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # Safe, additive migrations: existing memories are preserved.
        columns = {row["name"] for row in db.execute("PRAGMA table_info(memories)")}
        migrations = {
            "category": "ALTER TABLE memories ADD COLUMN category TEXT NOT NULL DEFAULT 'general'",
            "importance": "ALTER TABLE memories ADD COLUMN importance INTEGER NOT NULL DEFAULT 3",
            "tags": "ALTER TABLE memories ADD COLUMN tags TEXT NOT NULL DEFAULT ''",
        }
        for name, statement in migrations.items():
            if name not in columns:
                db.execute(statement)

        db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, status TEXT DEFAULT 'pending')")
        db.execute("CREATE TABLE IF NOT EXISTS approvals (id INTEGER PRIMARY KEY, action TEXT NOT NULL, details TEXT NOT NULL, status TEXT DEFAULT 'pending')")
