import re

def parse_email(email_text: str) -> dict:
    if not email_text:
        return {"risk_score": 0.0, "indicators": []}
    
    indicators = []
    risk_score = 0.0
    
    email_lower = email_text.lower()
    
    # Financial keywords
    if any(kw in email_lower for kw in ["urgent", "transfer", "invoice", "payment", "wire", "urgently"]):
        indicators.append("urgency_and_financial_request")
        risk_score += 0.4
        
    # Lookalike domains in text
    if re.search(r"@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email_text):
        # Basic mock check for lookalikes - if it contains common misspelling
        if "acme-payments" in email_lower or "rnicrosoft" in email_lower or "gmai1" in email_lower:
            indicators.append("lookalike_domain")
            risk_score += 0.5
            
    # Executive spoofing
    if any(kw in email_lower for kw in ["ceo", "president", "traveling", "don't call"]):
        indicators.append("executive_impersonation_pattern")
        risk_score += 0.3
        
    risk_score = min(1.0, risk_score)
    return {"risk_score": risk_score, "indicators": indicators}
