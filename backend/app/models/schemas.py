from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class IncidentBase(BaseModel):
    title: str

class IncidentCreate(IncidentBase):
    pass

class Incident(IncidentBase):
    id: int
    severity: str
    status: str
    risk_score: float
    created_at: datetime
    evidence_summary: Dict[str, Any]
    ai_explanation: Optional[str] = None
    attack_type: Optional[str] = None
    recommended_actions: List[str] = []
    mitre_mapping: Optional[str] = None

    class Config:
        from_attributes = True

class AnalysisRequest(BaseModel):
    email_text: Optional[str] = None
    url: Optional[str] = None
    audio_filename: Optional[str] = None
