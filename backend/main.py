from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from datetime import datetime
from pathlib import Path

app = FastAPI()

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory (parent of backend folder)
BASE_DIR = Path(__file__).parent.parent

# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / "backend" / "logs"
LOGS_DIR.mkdir(exist_ok=True)

@app.post("/track/{campaign_id}")
async def track_event(campaign_id: str, request: Request):
    # Get client IP and user agent
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    
    # Get event data from request body
    event_data = await request.json()
    
    # Create event object
    event = {
        "timestamp": datetime.now().isoformat(),
        "ip_address": client_ip,
        "user_agent": user_agent,
        "event_type": event_data.get("event_type"),
        "target_email": event_data.get("target_email"),
        "additional_data": event_data.get("additional_data", {})
    }
    
    # Append to campaign log file
    log_file = LOGS_DIR / f"{campaign_id}.json"
    
    # Create file if it doesn't exist
    if not log_file.exists():
        log_file.write_text("")
    
    # Append event as newline-delimited JSON
    with open(log_file, "a") as f:
        f.write(json.dumps(event) + "\n")
    
    return JSONResponse({"status": "success"})

# Mount static files for frontend
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend")), name="static")
app.mount("/kits", StaticFiles(directory=str(BASE_DIR / "kits")), name="kits")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 