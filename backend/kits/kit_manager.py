import json
from pathlib import Path
from typing import List, Optional
from .models import PhishingKit

class KitManager:
    def __init__(self, kits_dir: Path):
        self.kits_dir = kits_dir
        self.kits_file = kits_dir / "kits.json"
        self._ensure_kits_dir()

    def _ensure_kits_dir(self):
        self.kits_dir.mkdir(parents=True, exist_ok=True)
        if not self.kits_file.exists():
            # Create default kits
            default_kits = {
                "gtb-alert": {
                    "id": "gtb-alert",
                    "name": "GTBank Deactivation Alert",
                    "description": "Simulates a GTBank account deactivation alert",
                    "risk_level": "medium",
                    "tags": ["banking", "urgent", "account"],
                    "email_template": "email.html",
                    "landing_page": "index.html",
                    "trackable_fields": ["email", "password", "account_number"]
                },
                "nepa-bill": {
                    "id": "nepa-bill",
                    "name": "NEPA Overdue Bill",
                    "description": "Simulates an overdue electricity bill notification",
                    "risk_level": "low",
                    "tags": ["utility", "bill", "payment"],
                    "email_template": "email.html",
                    "landing_page": "index.html",
                    "trackable_fields": ["email", "phone", "address"]
                },
                "cac-filing": {
                    "id": "cac-filing",
                    "name": "CAC Company Filing Alert",
                    "description": "Simulates a Corporate Affairs Commission filing notification",
                    "risk_level": "high",
                    "tags": ["business", "compliance", "urgent"],
                    "email_template": "email.html",
                    "landing_page": "index.html",
                    "trackable_fields": ["email", "company_name", "rc_number"]
                }
            }
            self._save_kits(default_kits)

    def _load_kits(self) -> dict:
        with open(self.kits_file) as f:
            return json.load(f)

    def _save_kits(self, kits: dict):
        with open(self.kits_file, "w") as f:
            json.dump(kits, f, indent=2)

    def get_kit(self, kit_id: str) -> Optional[PhishingKit]:
        kits = self._load_kits()
        if kit_id in kits:
            return PhishingKit(**kits[kit_id])
        return None

    def list_kits(self) -> List[PhishingKit]:
        kits = self._load_kits()
        return [PhishingKit(**kit_data) for kit_data in kits.values()]

    def get_kit_template(self, kit_id: str, template_type: str) -> Optional[str]:
        kit = self.get_kit(kit_id)
        if not kit:
            return None

        template_file = self.kits_dir / kit_id / getattr(kit, template_type)
        if template_file.exists():
            return template_file.read_text()
        return None

    def add_kit(self, kit: PhishingKit) -> bool:
        kits = self._load_kits()
        if kit.id in kits:
            return False

        kits[kit.id] = kit.dict()
        self._save_kits(kits)
        return True

    def update_kit(self, kit_id: str, update_data: dict) -> Optional[PhishingKit]:
        kits = self._load_kits()
        if kit_id not in kits:
            return None

        kit = PhishingKit(**kits[kit_id])
        for key, value in update_data.items():
            if hasattr(kit, key):
                setattr(kit, key, value)

        kits[kit_id] = kit.dict()
        self._save_kits(kits)
        return kit

    def delete_kit(self, kit_id: str) -> bool:
        kits = self._load_kits()
        if kit_id not in kits:
            return False

        del kits[kit_id]
        self._save_kits(kits)
        return True 