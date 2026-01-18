from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

LAST_HEARTBEAT = None
TIMEOUT_SECONDS = 10


@app.get("/")
def root():
    return {"message": "Orion brain is running"}


@app.get("/status")
def status():
    online = False

    if LAST_HEARTBEAT:
        online = (datetime.utcnow() - LAST_HEARTBEAT) < timedelta(seconds=TIMEOUT_SECONDS)

    return {
        "online": online,
        "last_seen": LAST_HEARTBEAT
    }


@app.post("/heartbeat/")
def heartbeat(data: dict):
    global LAST_HEARTBEAT
    LAST_HEARTBEAT = datetime.utcnow()

    return {
        "status": "ok",
        "time": LAST_HEARTBEAT
    }
