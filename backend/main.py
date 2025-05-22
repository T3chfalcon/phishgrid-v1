from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from pathlib import Path
import json
import os

from auth.auth import (
    authenticate_user,
    create_access_token,
    get_user,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from auth.models import Token, UserLogin
from campaigns.campaign_manager import CampaignManager
from campaigns.models import CampaignCreate, CampaignUpdate
from kits.kit_manager import KitManager
from tracking.tracker import Tracker, TrackingEvent, EventType

app = FastAPI(title="PhishGrid API")

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

# Initialize managers
campaign_manager = CampaignManager(BASE_DIR / "data" / "campaigns")
kit_manager = KitManager(BASE_DIR / "kits")
tracker = Tracker(BASE_DIR / "data" / "tracking")

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend")), name="static")
app.mount("/kits", StaticFiles(directory=str(BASE_DIR / "kits")), name="kits")

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Campaign endpoints
@app.post("/campaigns", response_model=Campaign)
async def create_campaign(
    campaign: CampaignCreate,
    current_user: User = Depends(get_user)
):
    return campaign_manager.create_campaign(campaign, current_user.email)

@app.get("/campaigns", response_model=List[Campaign])
async def list_campaigns(current_user: User = Depends(get_user)):
    return campaign_manager.list_campaigns(current_user.email)

@app.get("/campaigns/{campaign_id}", response_model=Campaign)
async def get_campaign(
    campaign_id: str,
    current_user: User = Depends(get_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign or campaign.created_by != current_user.email:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.put("/campaigns/{campaign_id}", response_model=Campaign)
async def update_campaign(
    campaign_id: str,
    update_data: CampaignUpdate,
    current_user: User = Depends(get_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign or campaign.created_by != current_user.email:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign_manager.update_campaign(campaign_id, update_data.dict())

@app.delete("/campaigns/{campaign_id}")
async def delete_campaign(
    campaign_id: str,
    current_user: User = Depends(get_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign or campaign.created_by != current_user.email:
        raise HTTPException(status_code=404, detail="Campaign not found")
    if campaign_manager.delete_campaign(campaign_id):
        return {"status": "success"}
    raise HTTPException(status_code=500, detail="Failed to delete campaign")

# Kit endpoints
@app.get("/kits")
async def list_kits(current_user: User = Depends(get_user)):
    return kit_manager.list_kits()

@app.get("/kits/{kit_id}")
async def get_kit(
    kit_id: str,
    current_user: User = Depends(get_user)
):
    kit = kit_manager.get_kit(kit_id)
    if not kit:
        raise HTTPException(status_code=404, detail="Kit not found")
    return kit

# Tracking endpoints
@app.post("/track/{campaign_id}/{target_id}")
async def track_event(
    campaign_id: str,
    target_id: str,
    event_type: EventType,
    request: Request
):
    # Get client IP and user agent
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "Unknown")
    
    # Get additional data from request body
    additional_data = await request.json() if request.method == "POST" else {}
    
    # Create and save event
    event = TrackingEvent(
        campaign_id=campaign_id,
        target_id=target_id,
        event_type=event_type,
        ip_address=client_ip,
        user_agent=user_agent,
        additional_data=additional_data
    )
    tracker.track_event(event)
    
    return {"status": "success"}

@app.get("/campaigns/{campaign_id}/stats")
async def get_campaign_stats(
    campaign_id: str,
    current_user: User = Depends(get_user)
):
    campaign = campaign_manager.get_campaign(campaign_id)
    if not campaign or campaign.created_by != current_user.email:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return tracker.get_campaign_stats(campaign_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 