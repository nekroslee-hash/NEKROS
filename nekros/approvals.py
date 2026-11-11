from .db import connection

def request(action: str, details: str):
    with connection() as db:
        cur = db.execute("INSERT INTO approvals(action,details) VALUES (?,?)", (action,details))
        return dict(db.execute("SELECT * FROM approvals WHERE id=?", (cur.lastrowid,)).fetchone())

def decide(item_id: int, approved: bool):
    with connection() as db:
        cur = db.execute("UPDATE approvals SET status=? WHERE id=? AND status='pending'", ("approved" if approved else "rejected",item_id))
        if cur.rowcount == 0:
            return None
        return dict(db.execute("SELECT * FROM approvals WHERE id=?", (item_id,)).fetchone())
