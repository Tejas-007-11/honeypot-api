from fastapi import FastAPI, Header, HTTPException
from datetime import datetime

app = FastAPI(title="Agentic Honeypot API")

import os
API_KEY = os.getenv("API_KEY") # move to env later

@app.get("/honeypot")
def honeypot_status(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "status": "active",
        "honeypot_id": "hp_001",
        "message": "Honeypot service is running",
        "timestamp": datetime.utcnow().isoformat()
    }
