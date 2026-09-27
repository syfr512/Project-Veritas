from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.domain import Incident as DBIncident
from app.models.schemas import Incident
from app.api.endpoints import process_analysis
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class EmailForwardPayload(BaseModel):
    subject: str
    sender_email: str
    body_text: str
    attachment_filename: Optional[str] = None
    # In a real integration, the attachment would be a base64 encoded string or a URL to download

@router.post("/email-forward", status_code=202)
def handle_incoming_email(payload: EmailForwardPayload, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Business Integration Webhook:
    Simulates a Microsoft 365 or Google Workspace mail flow rule that forwards 
    suspicious emails automatically to the Veritas system without manual upload.
    """
    # 1. Create a new incident automatically
    incident_title = f"Automated Scan: {payload.subject}"
    db_incident = DBIncident(title=incident_title)
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    
    # Format the email text for the analyzer
    formatted_email_text = f"From: {payload.sender_email}\nSubject: {payload.subject}\n\n{payload.body_text}"
    
    # 2. Add the heavy analysis to a background task so the webhook returns immediately (prevents timeouts)
    background_tasks.add_task(
        process_analysis, 
        incident=db_incident, 
        email_text=formatted_email_text, 
        url="", 
        media_filename=payload.attachment_filename or "", 
        db=db
    )
    
    return {
        "message": "Email received and queued for multimodal analysis.", 
        "incident_id": db_incident.id,
        "status": "PROCESSING"
    }
