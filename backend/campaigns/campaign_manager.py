import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .models import Campaign, CampaignCreate, CampaignStatus, Target

class CampaignManager:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.campaigns_file = data_dir / "campaigns.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.campaigns_file.exists():
            self.campaigns_file.write_text("{}")

    def _load_campaigns(self) -> dict:
        with open(self.campaigns_file) as f:
            return json.load(f)

    def _save_campaigns(self, campaigns: dict):
        with open(self.campaigns_file, "w") as f:
            json.dump(campaigns, f, indent=2, default=str)

    def create_campaign(self, campaign_data: CampaignCreate, created_by: str) -> Campaign:
        campaigns = self._load_campaigns()
        
        # Generate unique ID and tracking IDs
        campaign_id = str(uuid.uuid4())
        for target in campaign_data.targets:
            target.tracking_id = str(uuid.uuid4())

        campaign = Campaign(
            id=campaign_id,
            name=campaign_data.name,
            description=campaign_data.description,
            kit_id=campaign_data.kit_id,
            targets=campaign_data.targets,
            status=CampaignStatus.DRAFT,
            scheduled_for=campaign_data.scheduled_for,
            created_by=created_by
        )

        campaigns[campaign_id] = campaign.dict()
        self._save_campaigns(campaigns)
        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        campaigns = self._load_campaigns()
        if campaign_id in campaigns:
            return Campaign(**campaigns[campaign_id])
        return None

    def list_campaigns(self, created_by: Optional[str] = None) -> List[Campaign]:
        campaigns = self._load_campaigns()
        result = []
        for campaign_data in campaigns.values():
            campaign = Campaign(**campaign_data)
            if created_by is None or campaign.created_by == created_by:
                result.append(campaign)
        return result

    def update_campaign(self, campaign_id: str, update_data: dict) -> Optional[Campaign]:
        campaigns = self._load_campaigns()
        if campaign_id not in campaigns:
            return None

        campaign = Campaign(**campaigns[campaign_id])
        for key, value in update_data.items():
            if hasattr(campaign, key):
                setattr(campaign, key, value)

        campaigns[campaign_id] = campaign.dict()
        self._save_campaigns(campaigns)
        return campaign

    def delete_campaign(self, campaign_id: str) -> bool:
        campaigns = self._load_campaigns()
        if campaign_id not in campaigns:
            return False

        del campaigns[campaign_id]
        self._save_campaigns(campaigns)
        return True 