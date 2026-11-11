from .db import connection

def add_memory(content: str):
    content = content.strip()
    if not content:
        raise ValueError("Memory cannot be empty")
    with connection() as db:
        cur = db.execute("INSERT INTO memories(content) VALUES (?)", (content,))
        return dict(db.execute("SELECT * FROM memories WHERE id=?", (cur.lastrowid,)).fetchone())

def list_memories():
    with connection() as db:
        return [dict(row) for row in db.execute("SELECT * FROM memories ORDER BY id DESC LIMIT 100")]
