from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from enum import Enum

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    RUNNING = "running"
    COMPLETED = "completed"
    PAUSED = "paused"

class PhishingKit(BaseModel):
    id: str
    name: str
    description: str
    risk_level: str
    tags: List[str]
    email_template: str
    landing_page: str
    trackable_fields: List[str]

class Target(BaseModel):
    email: EmailStr
    name: Optional[str] = None
    department: Optional[str] = None
    tracking_id: str

class Campaign(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    kit_id: str
    targets: List[Target]
    status: CampaignStatus
    created_at: datetime = datetime.now()
    scheduled_for: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_by: str  # User email

class CampaignCreate(BaseModel):
    name: str
    description: Optional[str] = None
    kit_id: str
    targets: List[Target]
    scheduled_for: Optional[datetime] = None

class CampaignUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CampaignStatus] = None
    scheduled_for: Optional[datetime] = None 