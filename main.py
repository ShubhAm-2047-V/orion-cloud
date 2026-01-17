from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Orion brain is running"}

@app.get("/status")
def status():
    return {
        "status": "running",
        "time": datetime.now().isoformat()
    }
