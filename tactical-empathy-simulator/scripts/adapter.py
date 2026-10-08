"""
adapter.py - Backward Compatibility Adapter for tactical-empathy-simulator

Converts legacy simulator outputs (v1.0) into canonical RehearsalDebrief (v2.0).
Removes requirements for forced 'That's Right' anchors, private emotion guesses, or scoring labels.
"""

import logging
from typing import Any, Dict, List

logger = logging.getLogger("lumei.simulator.adapter")


def adapt_legacy_simulation_to_rehearsal_debrief(legacy_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Transforms a v1.0 simulator candidate payload into a canonical RehearsalDebrief v2.0.
    """
    deprecated_fields = []
    for dep in ("thats_right_achieved", "observed_markers", "executive_summary", "persona_anger_level"):
        if dep in legacy_payload:
            deprecated_fields.append(dep)
            
    if deprecated_fields:
        logger.info("Migrated legacy simulation fields to RehearsalDebrief v2.0: %s", ", ".join(deprecated_fields))

    # Extract traceable moments
    traceable_moments = legacy_payload.get("traceable_moments", [])
    if not traceable_moments:
        raw_transcript = legacy_payload.get("transcript", [])
        for idx, turn in enumerate(raw_transcript, start=1):
            if isinstance(turn, dict):
                traceable_moments.append({
                    "turn_index": idx,
                    "verbatim_user_utterance": turn.get("user", ""),
                    "observed_counterpart_reaction": turn.get("counterpart", ""),
                    "behavioral_tag": turn.get("tag", "Observable Turn")
                })

    # Dialogue openers & closers
    openers = legacy_payload.get("dialogue_openers", [])
    if not openers and legacy_payload.get("observed_behavioral_strengths"):
        strengths = legacy_payload["observed_behavioral_strengths"]
        openers = strengths if isinstance(strengths, list) else [str(strengths)]

    closers = legacy_payload.get("dialogue_closers", [])
    if not closers and legacy_payload.get("development_blind_spots"):
        spots = legacy_payload["development_blind_spots"]
        closers = spots if isinstance(spots, list) else [str(spots)]

    # Socratic question
    socratic_questions = legacy_payload.get("socratic_questions", [])
    if isinstance(socratic_questions, list) and socratic_questions:
        socratic_q = str(socratic_questions[0])
    elif isinstance(legacy_payload.get("single_socratic_question"), str):
        socratic_q = legacy_payload["single_socratic_question"]
    else:
        socratic_q = "เมื่อคุณนำสิ่งที่ซ้อมไปใช้ในการพูดคุยจริง สัญญาณใดจากคู่สนทนาที่จะบอกว่าการรับฟังและการตั้งคำถามช่วยเปิดพื้นที่ความร่วมมือได้ดีขึ้น?"

    canonical_debrief: Dict[str, Any] = {
        "traceable_moments": traceable_moments,
        "dialogue_openers": openers,
        "dialogue_closers": closers,
        "alternative_response": legacy_payload.get("alternative_response", "ลองใช้ Dynamic Silence หรือ Mirroring คำสำคัญแทนการชี้แจงด้วยข้อเท็จจริงทันที"),
        "real_world_experiment": legacy_payload.get("real_world_experiment", "เริ่มการสนทนาด้วยคำถามเปิด 1 ข้อก่อนระบุข้อจำกัด"),
        "evidence_to_collect": legacy_payload.get("evidence_to_collect", ["ปฏิกิริยาของคู่สนทนา", "ความชัดเจนของข้อตกลง"]),
        "optional_leadership_development_links": legacy_payload.get("optional_leadership_development_links", ["Strategic Influence"]),
        "socratic_question": socratic_q
    }

    return canonical_debrief
