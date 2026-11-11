import pytest
from nekros import approvals, memory, tasks
from nekros.db import initialize_database

@pytest.fixture(autouse=True)
def isolated_db(tmp_path, monkeypatch):
    from nekros import db
    monkeypatch.setattr(db.settings, "database_path", str(tmp_path / "test.db"))
    initialize_database()

def test_memory_round_trip():
    item = memory.add_memory("NEKROS test")
    assert item["content"] == "NEKROS test"
    assert memory.list_memories()[0]["id"] == item["id"]

def test_task_creation():
    assert tasks.add_task("Build core")["status"] == "pending"

def test_approval_flow():
    item = approvals.request("delete_file", "Delete temporary file")
    assert item["status"] == "pending"
    assert approvals.decide(item["id"], True)["status"] == "approved"

def test_empty_memory_rejected():
    with pytest.raises(ValueError):
        memory.add_memory(" ")
