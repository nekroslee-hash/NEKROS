from .db import connection

def add_task(title: str):
    title = title.strip()
    if not title:
        raise ValueError("Task title cannot be empty")
    with connection() as db:
        cur = db.execute("INSERT INTO tasks(title) VALUES (?)", (title,))
        return dict(db.execute("SELECT * FROM tasks WHERE id=?", (cur.lastrowid,)).fetchone())
