from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from . import approvals, memory, tasks
from .db import initialize_database
from .orchestrator import orchestrator
from .security import require_token

ROOT = Path(__file__).resolve().parent.parent
app = FastAPI(title="NEKROS", version="0.1.0")
app.mount("/static", StaticFiles(directory=ROOT / "web"), name="static")

@app.on_event("startup")
def startup():
    initialize_database()

class TextBody(BaseModel):
    content: str = Field(min_length=1, max_length=10000)

class TaskBody(BaseModel):
    title: str = Field(min_length=1, max_length=300)

class ApprovalBody(BaseModel):
    action: str = Field(min_length=1, max_length=100)
    details: str = Field(min_length=1, max_length=2000)

class DecisionBody(BaseModel):
    approved: bool

@app.get("/")
def home():
    return FileResponse(ROOT / "web" / "index.html")

@app.get("/api/health")
def health():
    return {"status": "online", "name": "NEKROS", "version": "0.1.0"}

@app.get("/api/memories", dependencies=[Depends(require_token)])
def get_memories():
    return memory.list_memories()

@app.post("/api/memories", dependencies=[Depends(require_token)])
def save_memory(body: TextBody):
    try:
        return memory.add_memory(body.content)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

@app.post("/api/tasks", dependencies=[Depends(require_token)])
def save_task(body: TaskBody):
    try:
        return tasks.add_task(body.title)
    except ValueError as exc:
        raise HTTPException(400, str(exc))

@app.post("/api/approvals", dependencies=[Depends(require_token)])
def ask_approval(body: ApprovalBody):
    return approvals.request(body.action, body.details)

@app.post("/api/approvals/{item_id}/decision", dependencies=[Depends(require_token)])
def decide_approval(item_id: int, body: DecisionBody):
    result = approvals.decide(item_id, body.approved)
    if result is None:
        raise HTTPException(404, "Pending approval not found")
    return result

@app.post("/api/chat", dependencies=[Depends(require_token)])
async def chat(body: TextBody):
    try:
        return {"reply": await orchestrator.respond(body.content)}
    except ValueError as exc:
        raise HTTPException(400, str(exc))
