#!/usr/bin/env python3
"""
Deterministic Epistemic VETO Gate for Lumei STAR-L Decoder Skill.
Supports both native NarrativeDecodeResult (v5.0) and legacy candidate.json (v4.2).
Executes in Microsoft 365 Copilot Code Interpreter Air-Gapped Sandbox.
Enforces zero external network dependencies (Python stdlib only).
"""
import json
import os
import re
import sys

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

TRIGGER_PRIORITY = (
    "ZERO_SCORING_VIOLATION",
    "MULTIPLE_QUESTIONS_DETECTED",
    "MISSING_AUTHENTIC_FRICTION_SIGNAL",
    "MISSING_ROLE_GUIDANCE",
    "UNANCHORED_CLAIMS",
)

DEFAULT_CONFIG = {
    "prohibited_scoring_words": [
        "score", "points", "grade", "rating", "marks", "percentile",
        "maturity_level", "araya_level", "potential_level", "performance_rating",
        "คะแนน", "เกรด", "การตัดเกรด", "จัดอันดับ", "ระดับวุฒิภาวะ"
    ],
    "max_socratic_questions": 1,
    "hard_trigger_codes": [
        "ZERO_SCORING_VIOLATION",
        "MULTIPLE_QUESTIONS_DETECTED"
    ]
}


class CandidateValidationError(ValueError):
    """Raised when candidate input schema is invalid."""


def is_v5_narrative_decode_result(payload: dict) -> bool:
    """Checks if payload adheres to NarrativeDecodeResult schema."""
    return "episode_scope" in payload and "p_star_l" in payload and "evidence" in payload


def validate_schema(candidate: dict) -> None:
    if not isinstance(candidate, dict):
        raise CandidateValidationError("Candidate payload must be a JSON object.")
    
    if is_v5_narrative_decode_result(candidate):
        required_keys = ("episode_scope", "evidence", "p_star_l", "unknowns", "friction_signal")
        for key in required_keys:
            if key not in candidate:
                raise CandidateValidationError(f"Missing mandatory v5.0 key: '{key}'")
        return

    # Legacy v4.2 validation
    required_keys = ("structured_output", "target_role", "socratic_questions")
    for key in required_keys:
        if key not in candidate:
            raise CandidateValidationError(f"Missing mandatory root key: '{key}'")

    if not isinstance(candidate["socratic_questions"], list):
        raise CandidateValidationError("'socratic_questions' must be an array of strings.")


def load_config(config_path: str | None) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if config_path and os.path.isfile(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                override = json.load(f)
                cfg.update(override)
        except (OSError, json.JSONDecodeError) as e:
            raise CandidateValidationError(f"Failed to parse gate config: {str(e)}")
    return cfg


def extract_string_values(obj) -> list[str]:
    """Recursively extracts all string values from a dict or list."""
    extracted = []
    if isinstance(obj, str):
        extracted.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            extracted.extend(extract_string_values(v))
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            extracted.extend(extract_string_values(item))
    return extracted


def scan_zero_scoring_violations(candidate: dict, prohibited_words: list[str]) -> list[str]:
    strings = extract_string_values(candidate)
    combined_text = " ".join(strings).lower()
    found = []

    for word in prohibited_words:
        word_lower = word.lower()
        if all(ord(c) < 128 for c in word_lower):
            pattern = r"\b" + re.escape(word_lower) + r"\b"
        else:
            pattern = re.escape(word_lower)

        if re.search(pattern, combined_text):
            found.append(word)

    return list(dict.fromkeys(found))


def classify_failure(triggers: list[str], hard_trigger_codes: list[str]) -> str:
    if not triggers:
        return "none"
    if any(t in hard_trigger_codes for t in triggers):
        return "specification"
    return "implementation"


def evaluate_candidate(candidate: dict, config: dict) -> dict:
    prohibited = config.get("prohibited_scoring_words", DEFAULT_CONFIG["prohibited_scoring_words"])
    hard_triggers = config.get("hard_trigger_codes", DEFAULT_CONFIG["hard_trigger_codes"])
    scoring_matches = scan_zero_scoring_violations(candidate, prohibited)

    is_v5 = is_v5_narrative_decode_result(candidate)
    triggers = []
    if scoring_matches:
        triggers.append("ZERO_SCORING_VIOLATION")

    if is_v5:
        # In v5 pure decoder, questions are moved out to coach layer
        # Authenticate friction signal
        friction_signal = candidate.get("friction_signal")
        if friction_signal not in ("sufficient", "low", "unknown"):
            triggers.append("MISSING_AUTHENTIC_FRICTION_SIGNAL")
        elif friction_signal == "low":
            triggers.append("LOW_FRICTION_SIGNAL")
        
        sorted_triggers = [t for t in TRIGGER_PRIORITY if t in triggers]
        veto_triggered = any(t in ("ZERO_SCORING_VIOLATION",) for t in triggers)
        primary_trigger = sorted_triggers[0] if sorted_triggers else None
        failure_class = classify_failure(sorted_triggers, hard_triggers)

        return {
            "decision": "VETO" if veto_triggered else "PASS",
            "version": "v5.0",
            "failure_class": failure_class,
            "primary_trigger": primary_trigger,
            "all_triggers": triggers,
            "scoring_violations_found": scoring_matches,
            "friction_signal": friction_signal,
        }

    # Legacy v4.2 evaluation
    questions = candidate.get("socratic_questions", [])
    max_q = config.get("max_socratic_questions", 1)
    has_friction = bool(candidate.get("authentic_friction_signal"))
    has_role_guidance = bool(candidate.get("democratized_role_guidance"))
    uncited_claims = candidate.get("uncited_claims", [])

    if len(questions) > max_q:
        triggers.append("MULTIPLE_QUESTIONS_DETECTED")
    if not has_friction:
        triggers.append("MISSING_AUTHENTIC_FRICTION_SIGNAL")
    if not has_role_guidance:
        triggers.append("MISSING_ROLE_GUIDANCE")
    if uncited_claims:
        triggers.append("UNANCHORED_CLAIMS")

    sorted_triggers = [t for t in TRIGGER_PRIORITY if t in triggers]
    veto_triggered = len(sorted_triggers) > 0
    primary_trigger = sorted_triggers[0] if veto_triggered else None
    failure_class = classify_failure(sorted_triggers, hard_triggers)

    return {
        "decision": "VETO" if veto_triggered else "PASS",
        "version": "v4.2-legacy",
        "failure_class": failure_class,
        "primary_trigger": primary_trigger,
        "all_triggers": sorted_triggers,
        "scoring_violations_found": scoring_matches,
        "socratic_question_count": len(questions),
        "authentic_friction_present": has_friction,
        "role_guidance_present": has_role_guidance,
        "uncited_claims_count": len(uncited_claims),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"decision": "ERROR", "error": "Usage: star_l_veto_gate.py <payload.json> [--config <config.json>]"}))
        sys.exit(1)

    candidate_file = sys.argv[1]
    config_file = None
    if "--config" in sys.argv:
        try:
            idx = sys.argv.index("--config") + 1
            config_file = sys.argv[idx]
        except IndexError:
            pass

    try:
        if not os.path.exists(candidate_file):
            raise FileNotFoundError(f"Candidate file not found: {candidate_file}")

        with open(candidate_file, "r", encoding="utf-8") as f:
            candidate_data = json.load(f)

        validate_schema(candidate_data)
        config = load_config(config_file)
        result = evaluate_candidate(candidate_data, config)

        print(json.dumps(result, indent=2, ensure_ascii=False))
        if result["decision"] == "PASS":
            sys.exit(0)
        else:
            sys.exit(2)

    except (CandidateValidationError, OSError, json.JSONDecodeError) as err:
        error_payload = {
            "decision": "ERROR",
            "error_type": err.__class__.__name__,
            "message": str(err),
        }
        print(json.dumps(error_payload, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
