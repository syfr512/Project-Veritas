from sqlalchemy import Column, Integer, String, Float, Text, DateTime, JSON
import datetime
from app.database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    severity = Column(String, default="PENDING") # LOW, MEDIUM, HIGH, CRITICAL, PENDING
    status = Column(String, default="New") # New, Investigating, Verification Required, Confirmed Threat, Benign, Closed
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Store evidence JSON
    evidence_summary = Column(JSON, default={})
    
    # Store LLM analysis
    ai_explanation = Column(Text, nullable=True)
    attack_type = Column(String, nullable=True)
    recommended_actions = Column(JSON, default=[])
    mitre_mapping = Column(String, nullable=True)
