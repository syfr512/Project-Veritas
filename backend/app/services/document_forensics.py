import os
import base64
import json
import fitz  # PyMuPDF
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_document_image(file_path: str) -> str:
    """Converts a PDF page or image to a base64 JPEG string."""
    try:
        # If it's already an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            with open(file_path, "rb") as f:
                return base64.b64encode(f.read()).decode('utf-8')
                
        # If it's a PDF, render the first page
        if file_path.lower().endswith('.pdf'):
            doc = fitz.open(file_path)
            if len(doc) > 0:
                page = doc.load_page(0)
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom for better OCR resolution
                img_data = pix.tobytes("jpeg")
                return base64.b64encode(img_data).decode('utf-8')
    except Exception as e:
        print(f"Document extraction error: {e}")
    return ""

def analyze_document(file_path: str) -> dict:
    """
    Uses OpenAI's vision model to act as a Document Forensics tool.
    Extracts text (OCR) and looks for digital manipulation (forged invoices, mismatched fonts).
    """
    if not file_path or not os.path.exists(file_path):
        return {"risk_score": 0.0, "indicators": []}

    base64_img = extract_document_image(file_path)
    if not base64_img:
        return {"risk_score": 0.0, "indicators": ["document_unreadable"]}

    content = [
        {
            "type": "text", 
            "text": "You are a cyber forensics AI. Analyze this document (invoice, receipt, or letter). Look for signs of tampering, inconsistent fonts, mismatched alignments, blurred text artifacts indicating edits, or suspicious urgent payment instructions. Respond ONLY in valid JSON format like: {\"risk_score\": 0.90, \"indicators\": [\"mismatched_font\", \"urgent_wire_transfer\"]}. The risk_score must be a float between 0.0 and 1.0."
        },
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_img}",
                "detail": "high"
            }
        }
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": content}],
            response_format={"type": "json_object"},
            max_tokens=200
        )
        
        result = json.loads(response.choices[0].message.content)
        return {
            "risk_score": float(result.get("risk_score", 0.0)),
            "indicators": result.get("indicators", [])
        }
    except Exception as e:
        print(f"Document Vision API Error: {e}")
        return {"risk_score": 0.2, "indicators": ["analysis_failed"]}
