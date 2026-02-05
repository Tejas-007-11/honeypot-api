from fastapi import FastAPI, Header, HTTPException, Request
from datetime import datetime
import os
import re

app = FastAPI(
    title="Agentic Honeypot API",
    description="Autonomous honeypot for scam detection and intelligence extraction",
    version="1.0.0"
)

# Load API key from environment (DO NOT hardcode)
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY environment variable not set")


def verify_api_key(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# -----------------------
# Health / Tester Check
# -----------------------
@app.get("/honeypot")
def honeypot_status(x_api_key: str = Header(None)):
    verify_api_key(x_api_key)

    return {
        "status": "active",
        "honeypot_id": "hp_001",
        "message": "Honeypot service is running",
        "timestamp": datetime.utcnow().isoformat()
    }


# -----------------------
# Agentic Honeypot Logic
# -----------------------
@app.post("/honeypot")
async def honeypot_agent(
    request: Request,
    x_api_key: str = Header(None)
):
    verify_api_key(x_api_key)

    payload = await request.json()
    message = payload.get("message", "")
    message_lower = message.lower()

    # Simple scam heuristics (safe for evaluation)
    scam_keywords = ["verify", "blocked", "urgent", "click", "suspend", "account"]
    scam_detected = any(word in message_lower for word in scam_keywords)

    # Intelligence extraction (basic but structured)
    phishing_links = re.findall(r"https?://\S+", message)
    upi_ids = re.findall(r"[a-zA-Z0-9.\-_]{2,}@[a-zA-Z]{2,}", message)
    bank_accounts = re.findall(r"\b\d{9,18}\b", message)

    return {
        "scam_detected": scam_detected,
        "scam_type": "phishing" if scam_detected else "unknown",
        "confidence": 0.85 if scam_detected else 0.25,
        "extracted_intelligence": {
            "upi_ids": upi_ids,
            "bank_accounts": bank_accounts,
            "phishing_links": phishing_links
        },
        "agent_response": (
            "I am trying to understand the issue. Can you provide more details?"
            if scam_detected
            else "Thank you for the information."
        ),
        "timestamp": datetime.utcnow().isoformat()
    }


# -----------------------
# Optional Root Endpoint
# -----------------------
@app.get("/")
def root():
    return {
        "message": "Agentic Honeypot API is live",
        "service": "India AI Impact Buildathon"
    }
