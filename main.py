from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

# -----------------------------
# Laptop state storage
# -----------------------------
LAPTOP_STATE = {
    "online": False,
    "last_seen": None
}

HEARTBEAT_TIMEOUT = 10  # seconds


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {"message": "Orion brain is running"}


# -----------------------------
# Brain status (for logo)
# -----------------------------
@app.get("/status")
def status():
    return {
        "status": "running",
        "time": datetime.utcnow().isoformat()
    }


# -----------------------------
# Laptop heartbeat
# -----------------------------
@app.post("/laptop/heartbeat")
def laptop_heartbeat():
    LAPTOP_STATE["online"] = True
    LAPTOP_STATE["last_seen"] = datetime.utcnow()
    return {"heartbeat": "received"}


# -----------------------------
# Laptop status (for heartbeat line)
# -----------------------------
@app.get("/laptop/status")
def laptop_status():
    if LAPTOP_STATE["last_seen"] is None:
        return {"online": False, "last_seen": None}

    now = datetime.utcnow()
    if now - LAPTOP_STATE["last_seen"] > timedelta(seconds=HEARTBEAT_TIMEOUT):
        LAPTOP_STATE["online"] = False

    return {
        "online": LAPTOP_STATE["online"],
        "last_seen": (
            LAPTOP_STATE["last_seen"].isoformat()
            if LAPTOP_STATE["last_seen"]
            else None
        )
    }
