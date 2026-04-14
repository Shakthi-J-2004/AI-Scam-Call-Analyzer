import re

# Extensive lists for detecting specific intents and types
SCAM_KEYWORDS = {
    "phishing": ["password", "otp", "pin", "verify your identity", "social security", "ssn", "login details", "click the link"],
    "bank_fraud": ["bank", "account suspended", "unauthorized transaction", "credit card", "blocked", "fraud department"],
    "lottery_scam": ["lottery", "prize", "won", "claim your reward", "sweepstakes", "fee to claim"],
    "job_scam": ["work from home", "easy money", "guaranteed income", "recruiter", "upfront payment", "telegram", "whatsapp group"],
    "crypto_scam": ["bitcoin", "crypto", "investment", "double your money", "wallet"]
}

URGENCY_KEYWORDS = ["urgent", "immediately", "now", "within 24 hours", "fail to", "consequences", "arrested", "police", "legal action"]

def sentence_split(text: str) -> list:
    """Basic sentence splitting using regex."""
    sentences = re.split(r'(?<=[.!?]) +', text.strip())
    return [s for s in sentences if s]

def analyze_transcript(transcript: str) -> dict:
    """
    Analyzes the transcribed text using a hybrid approach (rule-based heuristic representing an LLM backend).
    """
    sentences = sentence_split(transcript)
    
    flagged_sentences = []
    total_risk_score = 0
    urgency_count = 0
    detected_types = {k: 0 for k in SCAM_KEYWORDS.keys()}
    
    for sentence in sentences:
        s_lower = sentence.lower()
        risk_level = "Green"
        reason = ""
        score_bump = 0
        
        # Check urgency
        if any(u in s_lower for u in URGENCY_KEYWORDS):
            urgency_count += 1
            score_bump += 15
            risk_level = "Yellow"
            reason += "Urgent/pressuring tone detected. "
            
        # Check specific scam keywords
        for scam_type, keywords in SCAM_KEYWORDS.items():
            found = [k for k in keywords if k in s_lower]
            if found:
                detected_types[scam_type] += len(found)
                score_bump += 20 * len(found)
                risk_level = "Red"
                reason += f"Suspicious keyword(s) found: {', '.join(found)}. "
        
        # Determine sentence final status
        if risk_level == "Green" and score_bump == 0:
            reason = "Looks normal."
            
        flagged_sentences.append({
            "text": sentence,
            "risk_level": risk_level,
            "reason": reason.strip()
        })
        
        total_risk_score += score_bump

    # Normalize risk score to 0-100
    base_score = min(total_risk_score, 100)
    
    # Determine the predominant scam type
    most_likely_type = "unknown"
    max_hits = 0
    for stype, hits in detected_types.items():
        if hits > max_hits:
            max_hits = hits
            most_likely_type = stype.replace("_", " ").title()
            
    if base_score > 70:
        recommendation = "High Risk: Do not share any information. Block the number and report."
        summary = "This caller is trying to scare you into giving them money or secrets. They seem to be pretending to be an authority."
        confidence = min(base_score + 10, 99)
    elif base_score > 30:
        recommendation = "Medium Risk: Proceed with extreme caution. Verify their identity independently."
        summary = "This call sounds a bit suspicious. They are asking for unusual things. It's safer to hang up and call the real company yourself."
        confidence = 75
    else:
        most_likely_type = "None"
        recommendation = "Low Risk: Looks safe, but always stay alert."
        summary = "This looks like a normal, everyday conversation. No obvious tricks found."
        confidence = 90
        
    return {
        "risk_score": int(base_score),
        "scam_type": most_likely_type,
        "confidence_score": confidence,
        "recommendation": recommendation,
        "summary_for_10_yr_old": summary,
        "flagged_sentences": flagged_sentences
    }
