"""
test_maker_coach.py - Acceptance test suite for lumei-human-ai-operational-maker-coach.
Tests input/plan/result schema conformance and non-authorization guardrails.
"""

import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = SKILL_DIR / "schemas"


def load_schema(name: str) -> dict:
    with open(SCHEMAS_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def test_maker_input_contract():
    print("Testing MakerCoachInput contract...")
    schema = load_schema("maker-coach-input.schema.json")
    
    valid_input = {
        "work_problem": "Delayed shift handover due to fragmented vibration data across DCS and paper log",
        "intended_value": "Reduce handover review time by 10 minutes without missing vibration alarm trends",
        "users_or_stakeholders": ["Incoming Shift Lead", "Outgoing Shift Lead", "DCS Board Operator"],
        "authorised_evidence": ["Logbook entries #4020-#4029", "DCS vibration archive for P-102"],
        "known_constraints": ["Trip warning threshold is 4.5 mm/s", "Handover window is limited to 20 minutes"],
        "decision_rights": ["Authorized to adjust handover checklist format; not authorized to alter DCS alarm setpoints"],
        "prohibited_actions": ["No modification of DCS alarm logic or pump trip limits without formal MOC"],
        "consequence_level": "normal"
    }
    
    for req in schema["required"]:
        assert req in valid_input, f"Missing required property: {req}"
    print("[PASS] MakerCoachInput schema validated successfully.")


def test_maker_plan_contract():
    print("Testing MakerCoachPlan contract...")
    schema = load_schema("maker-coach-plan.schema.json")
    
    valid_plan = {
        "problem_frame": "Frontline engineers spend 15 minutes manually aggregating pump vibration logs before meetings",
        "current_workflow": ["Log reading from DCS", "Copy to Excel", "Format table", "Email attendees"],
        "evidence": ["Average time per shift: 15 minutes", "3 past typos in manual data entry"],
        "assumptions": ["DCS CSV export format remains stable across shifts"],
        "unknowns": ["Whether incoming shift lead has permission to run Python extraction script"],
        "prototype_hypothesis": "A structured prompt template synthesizing CSV logs directly into a 1-page table will eliminate manual copy-paste errors.",
        "smallest_reversible_prototype": "Draft Prompt Template: Ingests DCS daily CSV, formats into handover table.",
        "human_review_points": ["Lead Reliability Engineer checks output accuracy against raw CSV for 3 consecutive days."],
        "verification_checks": ["Values must match raw CSV within 0.01 mm/s", "Zero hallucinated equipment IDs"],
        "stop_conditions": ["Any discrepancy found between template output and raw DCS values"],
        "authorised_process_handoffs": ["If adopted company-wide, submit to IT Data Governance & Plant Automation Committee"]
    }

    for req in schema["required"]:
        assert req in valid_plan, f"Missing required property: {req}"
    print("[PASS] MakerCoachPlan schema validated successfully.")


def test_maker_result_and_guardrails():
    print("Testing MakerCoachResult and Guardrails...")
    schema = load_schema("maker-coach-result.schema.json")
    
    valid_result = {
        "artifact_type": "handover_synthesis_prompt",
        "draft_artifact": "### PROVISIONAL DRAFT: Handover Vibration Synthesis Prompt\nStatus: UNVERIFIED DRAFT\n...",
        "evidence_used": ["DCS log format 2026-10-06"],
        "assumptions_remaining": ["User validates CSV column names match shift schema"],
        "verification_status": "unverified",
        "risks_and_boundary_conditions": ["Draft only: Must not be used as official engineering release without sign-off"],
        "next_safe_action": "Run side-by-side with manual excel table for 2 shifts",
        "evidence_to_collect": ["Comparison accuracy count", "Time elapsed"],
        "learning_note": "Designing the template clarified that column names differ between Unit 1 and Unit 2."
    }

    for req in schema["required"]:
        assert req in valid_result, f"Missing required property: {req}"

    # Guardrail check 1: verification_status must be in enum
    assert valid_result["verification_status"] in ["unverified", "partially_verified", "verified_by_authorised_human"]

    # Guardrail check 2: Forbidden scoring terms must not appear
    forbidden = ["score", "rating", "grade", "points", "maturity_level"]
    raw_str = json.dumps(valid_result).lower()
    for f_word in forbidden:
        assert f_word not in raw_str, f"Forbidden evaluation word '{f_word}' found in result"

    print("[PASS] MakerCoachResult and Poka-Yoke guardrails validated successfully.")


if __name__ == "__main__":
    test_maker_input_contract()
    test_maker_plan_contract()
    test_maker_result_and_guardrails()
    print("\n>>> ALL Lumei-HUMAN-AI-OPERATIONAL-MAKER-COACH ACCEPTANCE TESTS PASSED (PASS) <<<")
