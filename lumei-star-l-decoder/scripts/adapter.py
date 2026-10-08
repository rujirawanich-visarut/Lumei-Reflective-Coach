"""
adapter.py - Backward Compatibility Adapter for lumei-star-l-decoder

Converts legacy candidate.json payloads (v4.2) into canonical NarrativeDecodeResult (v5.0).
Silently logs deprecated fields without exposing internal deprecation noise to end users.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger("lumei.decoder.adapter")


def adapt_legacy_candidate_to_narrative_decode_result(legacy_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms a v4.2 candidate payload into a v5.0 NarrativeDecodeResult.
    """
    deprecated_fields_found = []
    
    # Check deprecated root keys
    for dep_key in ("target_role", "democratized_role_guidance", "socratic_questions", "uncited_claims"):
        if dep_key in legacy_payload:
            deprecated_fields_found.append(dep_key)

    structured = legacy_payload.get("structured_output", {})
    if not isinstance(structured, dict):
        structured = {}

    # Check deprecated structured keys
    for dep_sub in ("araya_level", "mfrc_audit", "bani_profile", "future_back_horizon"):
        if dep_sub in structured:
            deprecated_fields_found.append(f"structured_output.{dep_sub}")

    if deprecated_fields_found:
        logger.info("Migrated legacy fields to NarrativeDecodeResult v5.0: %s", ", ".join(deprecated_fields_found))

    # Reconstruct actions list
    raw_action = structured.get("action")
    actions: List[str] = []
    if isinstance(raw_action, list):
        actions = [str(a) for a in raw_action]
    elif isinstance(raw_action, str) and raw_action.strip():
        actions = [raw_action.strip()]

    # Reconstruct results list
    raw_result = structured.get("result")
    results: List[str] = []
    if isinstance(raw_result, list):
        results = [str(r) for r in raw_result]
    elif isinstance(raw_result, str) and raw_result.strip():
        results = [raw_result.strip()]

    # Friction signal mapping
    friction_bool = legacy_payload.get("authentic_friction_signal")
    if friction_bool is True:
        friction_signal = "sufficient"
    elif friction_bool is False:
        friction_signal = "low"
    else:
        friction_signal = "unknown"

    # Assemble canonical v5.0 NarrativeDecodeResult
    canonical_result: Dict[str, Any] = {
        "episode_scope": structured.get("situation", "Legacy Bounded Workplace Episode")[:120],
        "evidence": {
            "verbatim": [],
            "observable_actions": actions,
            "documented_outputs": [],
            "reported_claims": [],
            "source_refs": []
        },
        "p_star_l": {
            "perspective": structured.get("perspective"),
            "situation": structured.get("situation"),
            "task": structured.get("task"),
            "actions": actions,
            "results": results,
            "learning_stated": structured.get("learned"),
            "learning_interpretation": None
        },
        "unknowns": legacy_payload.get("uncited_claims", []),
        "contradictions": [],
        "alternative_explanation": None,
        "friction_signal": friction_signal,
        "calming_anchor_observations": {
            "clarity_created": None,
            "dissent_enabled": None,
            "pressure_amplified": None
        },
        "prohibited": [
            "scores",
            "stable_traits",
            "inferred_motives",
            "personnel_recommendations"
        ]
    }

    return canonical_result
