import re

def parse_url(url: str) -> dict:
    if not url:
        return {"risk_score": 0.0, "indicators": []}
        
    indicators = []
    risk_score = 0.0
    
    url_lower = url.lower()
    
    # IP-based URL
    if re.search(r"http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_lower):
        indicators.append("ip_based_url")
        risk_score += 0.6
        
    # Lookalike domains
    if "security" in url_lower or "login" in url_lower or "acme-payments" in url_lower:
        indicators.append("suspicious_keywords_in_url")
        risk_score += 0.4
        
    # Free hosting or unusual TLDs
    if any(tld in url_lower for tld in [".xyz", ".top", ".info"]):
        indicators.append("suspicious_tld")
        risk_score += 0.3
        
    risk_score = min(1.0, risk_score)
    return {"risk_score": risk_score, "indicators": indicators}
