#!/usr/bin/env python3
"""
Deterministic Pragmatics / TMR VETO Gate for Tactical Empathy Debrief.
Enforces:
1. Zero-Scoring Authority (Strict ban on numbers, %, ratings, scores, maturity levels)
2. Single Socratic Question Rule (Exactly one question in debrief)
3. Traceable Moments presence (No ungrounded mind-reading claims)
4. No requirement for forced 'That's Right' verbal triggers
Exit 0 = PASS, Exit 2 = VETO, Exit 1 = ERROR.
"""
import sys
import json
import re

# Ensure UTF-8 output across all platforms
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

SCORING_KEYWORDS = [
    r"\bscore\b", r"\brating\b", r"\bgrade\b", r"\bpoints\b",
    r"\bmaturity_level\b", r"\bperformance_rating\b",
    r"คะแนน", r"เกรด", r"ระดับ\s*\d+/\d+", r"\d+\s*%", r"\d+\s*เปอร์เซ็นต์",
    r"จัดอันดับ", r"ระดับวุฒิภาวะ"
]


def audit_candidate(candidate_data: dict) -> dict:
    text_content = json.dumps(candidate_data, ensure_ascii=False)
    violations = []
    
    # 1. Zero-Scoring Audit
    for pattern in SCORING_KEYWORDS:
        if re.search(pattern, text_content, re.IGNORECASE):
            violations.append(f"SCORING_VIOLATION_DETECTED: {pattern}")
            
    # 2. Single Question Audit
    if "socratic_question" in candidate_data and isinstance(candidate_data["socratic_question"], str):
        # Single string property in v2.0
        if not candidate_data["socratic_question"].strip():
            violations.append("QUESTION_COUNT_VIOLATION: socratic_question cannot be empty")
    elif "socratic_questions" in candidate_data:
        # Array property in legacy
        socratic_questions = candidate_data.get("socratic_questions", [])
        if len(socratic_questions) != 1:
            violations.append(f"QUESTION_COUNT_VIOLATION: Expected 1, found {len(socratic_questions)}")
    else:
        violations.append("QUESTION_COUNT_VIOLATION: Missing socratic_question")
        
    # 3. Behavioral / Traceable Moments Audit
    moments = candidate_data.get("traceable_moments", [])
    legacy_markers = candidate_data.get("observed_markers", {})
    if not moments and not legacy_markers.get("tactics_identified"):
        violations.append("MISSING_TRACEABLE_MOMENTS")

    is_veto = len(violations) > 0
    return {
        "decision": "VETO" if is_veto else "PASS",
        "violations": violations,
        "failure_class": "human_required" if any("SCORING" in v for v in violations) else ("implementation" if is_veto else "none"),
        "rehearsal_verified": not is_veto
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"decision": "ERROR", "message": "Usage: empathy_marker_gate.py <debrief.json>"}))
        sys.exit(1)
        
    candidate_path = sys.argv[1]
    try:
        with open(candidate_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        result = audit_candidate(data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(2 if result["decision"] == "VETO" else 0)
    except Exception as e:
        print(json.dumps({"decision": "ERROR", "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
