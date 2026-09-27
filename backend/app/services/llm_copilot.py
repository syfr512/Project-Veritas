import os
import json
from openai import OpenAI

# Initialize client using environment variable OPENAI_API_KEY
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_copilot_response(fusion_results: dict) -> dict:
    if not client.api_key:
        return {
            "ai_explanation": "LLM API Key not configured. Manual review required.",
            "attack_type": "Unknown",
            "recommended_actions": ["Review evidence manually.", "Contact security team."],
            "mitre_mapping": "Unknown"
        }

    prompt = f"""
You are an AI Security Copilot for Project Veritas.
You have been provided with the following STRUCTURED EVIDENCE from our deterministic detectors and fusion engine.
DO NOT invent evidence. DO NOT act on raw user text. 

EVIDENCE JSON:
{json.dumps(fusion_results, indent=2)}

Your task is to analyze this structured evidence and return a JSON object with exactly these keys:
- "ai_explanation": A concise, professional explanation of why this incident was flagged and what the evidence means.
- "attack_type": The likely attack category (e.g., "Executive Impersonation / BEC", "Phishing", "Credential Theft").
- "recommended_actions": A list of 3-5 strings containing concrete steps the human analyst should take (e.g. "Do not process payment", "Verify via phone").
- "mitre_mapping": The relevant MITRE ATT&CK technique ID (e.g. "T1566.002").

Respond ONLY with valid JSON.
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity incident response assistant. Respond only in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={ "type": "json_object" }
        )
        
        result_json = json.loads(response.choices[0].message.content)
        return result_json
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return {
            "ai_explanation": f"Error generating explanation: {e}",
            "attack_type": "Error",
            "recommended_actions": ["Review evidence manually due to AI error."],
            "mitre_mapping": "Error"
        }
