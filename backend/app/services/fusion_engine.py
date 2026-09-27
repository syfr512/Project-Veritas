def fuse_evidence(email_result: dict, url_result: dict, media_result: dict) -> dict:
    # Weights for the fusion engine (adjusted for generic media)
    W_EMAIL = 0.35
    W_URL = 0.35
    W_MEDIA = 0.30
    
    # Calculate weighted score
    fused_score = (
        (email_result.get("risk_score", 0.0) * W_EMAIL) +
        (url_result.get("risk_score", 0.0) * W_URL) +
        (media_result.get("risk_score", 0.0) * W_MEDIA)
    )
    
    # Scale to 0-100
    final_score = min(100, int(fused_score * 100))
    
    if final_score >= 80:
        severity = "CRITICAL"
    elif final_score >= 60:
        severity = "HIGH"
    elif final_score >= 30:
        severity = "MEDIUM"
    else:
        severity = "LOW"
        
    all_indicators = (
        email_result.get("indicators", []) + 
        url_result.get("indicators", []) + 
        media_result.get("indicators", [])
    )
    
    return {
        "risk_score": final_score,
        "severity": severity,
        "indicators": all_indicators,
        "email_risk": int(email_result.get("risk_score", 0.0) * 100),
        "url_risk": int(url_result.get("risk_score", 0.0) * 100),
        "audio_risk": int(media_result.get("risk_score", 0.0) * 100), # Keeping audio_risk key for frontend compatibility
        "media_risk": int(media_result.get("risk_score", 0.0) * 100)
    }
