def analyze_audio(filename: str) -> dict:
    if not filename:
        return {"risk_score": 0.0, "indicators": []}
        
    indicators = []
    risk_score = 0.0
    
    filename_lower = filename.lower()
    
    # Mocking: if the file name has 'urgent', 'ceo', 'fake', or 'deepfake' we simulate a detection
    if any(keyword in filename_lower for keyword in ["urgent", "ceo", "fake", "deepfake"]):
        if filename_lower.endswith(".mp4") or filename_lower.endswith(".mov") or filename_lower.endswith(".avi"):
             indicators.append("synthetic_video_anomalies_detected")
             indicators.append("facial_artifact_mismatch")
             risk_score = 0.90
        else:
             indicators.append("synthetic_voice_anomalies_detected")
             indicators.append("audio_frequency_mismatch")
             risk_score = 0.85
    else:
        risk_score = 0.1
        
    return {"risk_score": risk_score, "indicators": indicators}
