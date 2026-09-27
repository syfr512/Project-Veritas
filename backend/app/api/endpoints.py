from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain import Incident as DBIncident
from app.models.schemas import Incident, IncidentCreate, AnalysisRequest
from app.services.email_analyzer import parse_email
from app.services.url_analyzer import parse_url
from app.services.ml_mock import analyze_audio
from app.services.fusion_engine import fuse_evidence
from app.services.llm_copilot import generate_copilot_response
from typing import List
import shutil
import os

router = APIRouter()

@router.post("/incidents/", response_model=Incident)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    db_incident = DBIncident(title=incident.title)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/incidents/", response_model=List[Incident])
def get_incidents(db: Session = Depends(get_db)):
    return db.query(DBIncident).order_by(DBIncident.created_at.desc()).all()

@router.get("/incidents/{incident_id}", response_model=Incident)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(DBIncident).filter(DBIncident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

def process_analysis(incident, email_text, url, audio_filename, db):
    email_result = parse_email(email_text or "")
    url_result = parse_url(url or "")
    audio_result = analyze_audio(audio_filename or "")
    
    fusion_results = fuse_evidence(email_result, url_result, audio_result)
    ai_response = generate_copilot_response(fusion_results)
    
    incident.risk_score = fusion_results["risk_score"]
    incident.severity = fusion_results["severity"]
    incident.status = "Verification Required" if fusion_results["risk_score"] >= 60 else "Investigating"
    incident.evidence_summary = fusion_results
    incident.ai_explanation = ai_response.get("ai_explanation", "")
    incident.attack_type = ai_response.get("attack_type", "")
    incident.recommended_actions = ai_response.get("recommended_actions", [])
    incident.mitre_mapping = ai_response.get("mitre_mapping", "")
    
    db.commit()
    db.refresh(incident)
    return incident

@router.post("/incidents/{incident_id}/analyze", response_model=Incident)
def analyze_incident(incident_id: int, req: AnalysisRequest, db: Session = Depends(get_db)):
    incident = db.query(DBIncident).filter(DBIncident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return process_analysis(incident, req.email_text, req.url, req.audio_filename, db)

@router.post("/incidents/{incident_id}/analyze_file", response_model=Incident)
def analyze_incident_file(incident_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    incident = db.query(DBIncident).filter(DBIncident.id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Save file temporarily to read it if it's text/email, or just pass filename for audio mock
    os.makedirs("/tmp/veritas", exist_ok=True)
    temp_path = f"/tmp/veritas/{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        pass

    # Read content if text or eml
    email_text = ""
    if file.filename.endswith(".txt") or file.filename.endswith(".eml"):
        try:
            with open(temp_path, "r", encoding="utf-8") as f:
                email_text = f.read()
        except Exception:
            pass

    return process_analysis(incident, email_text, "", file.filename, db)
