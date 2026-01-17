from fastapi import FastAPI
from datetime import datetime
from typing import Dict, List
import uuid

app = FastAPI(title="Orion Cloud Brain")

LAPTOP_STATUS: Dict[str, dict] = {}
COMMAND_QUEUE: Dict[str, List[dict]] = {}

@app.get("/")
def root():
    return {"message": "Orion Cloud Brain is running"}

@app.post("/laptop/heartbeat")
def laptop_heartbeat(laptop_id: str):
    LAPTOP_STATUS[laptop_id] = {
        "online": True,
        "last_seen": datetime.utcnow().isoformat()
    }
    COMMAND_QUEUE.setdefault(laptop_id, [])
    return {"status": "ok"}

@app.get("/laptop/{laptop_id}/status")
def laptop_status(laptop_id: str):
    return LAPTOP_STATUS.get(
        laptop_id,
        {"online": False, "last_seen": None}
    )

@app.post("/command/send")
def send_command(laptop_id: str, command: str, sender: str):
    cmd = {
        "id": str(uuid.uuid4()),
        "command": command,
        "sender": sender,
        "time": datetime.utcnow().isoformat(),
        "executed": False
    }
    COMMAND_QUEUE.setdefault(laptop_id, []).append(cmd)
    return {"queued": True, "command_id": cmd["id"]}

@app.get("/command/pull")
def pull_commands(laptop_id: str):
    queue = COMMAND_QUEUE.get(laptop_id, [])
    pending = [c for c in queue if not c["executed"]]
    for c in pending:
        c["executed"] = True
    return pending
