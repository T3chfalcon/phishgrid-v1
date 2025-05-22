import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from pydantic import BaseModel

class EventType(str, Enum):
    EMAIL_OPEN = "email_open"
    LINK_CLICK = "link_click"
    FORM_SUBMIT = "form_submit"

class TrackingEvent(BaseModel):
    campaign_id: str
    target_id: str
    event_type: EventType
    timestamp: datetime = datetime.now()
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    additional_data: Dict = {}

class Tracker:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.events_file = data_dir / "events.json"
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.events_file.exists():
            self.events_file.write_text("[]")

    def _load_events(self) -> List[dict]:
        with open(self.events_file) as f:
            return json.load(f)

    def _save_events(self, events: List[dict]):
        with open(self.events_file, "w") as f:
            json.dump(events, f, indent=2, default=str)

    def track_event(self, event: TrackingEvent):
        events = self._load_events()
        events.append(event.dict())
        self._save_events(events)

    def get_campaign_events(self, campaign_id: str) -> List[TrackingEvent]:
        events = self._load_events()
        return [
            TrackingEvent(**event)
            for event in events
            if event["campaign_id"] == campaign_id
        ]

    def get_target_events(self, campaign_id: str, target_id: str) -> List[TrackingEvent]:
        events = self._load_events()
        return [
            TrackingEvent(**event)
            for event in events
            if event["campaign_id"] == campaign_id and event["target_id"] == target_id
        ]

    def get_campaign_stats(self, campaign_id: str) -> Dict:
        events = self.get_campaign_events(campaign_id)
        stats = {
            "total_events": len(events),
            "email_opens": 0,
            "link_clicks": 0,
            "form_submissions": 0,
            "unique_targets": set()
        }

        for event in events:
            stats["unique_targets"].add(event.target_id)
            if event.event_type == EventType.EMAIL_OPEN:
                stats["email_opens"] += 1
            elif event.event_type == EventType.LINK_CLICK:
                stats["link_clicks"] += 1
            elif event.event_type == EventType.FORM_SUBMIT:
                stats["form_submissions"] += 1

        stats["unique_targets"] = len(stats["unique_targets"])
        return stats 