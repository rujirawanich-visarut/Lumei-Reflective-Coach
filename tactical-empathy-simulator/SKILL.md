---
name: tactical-empathy-simulator
description: Provide voluntary fictional conversation practice with pause/finish controls and traceable debrief; use after safe activity-specific opt-in.
license: Proprietary
metadata:
  version: "6.0.0"
  display_name: "Conversation Rehearsal"
  architecture_alignment: "Lumei Global Workplace Skills / Shared Contracts 1.0.0"
  control_plane: "00_LUMEI_DEVELOPMENT_ORCHESTRATION.md"
  runtime_environment: "portable; host not selected"
  emits: "RehearsalDebrief"
---
# Conversation Rehearsal

Use [Instruction_v5.1.md](../Instruction_v5.1.md), [shared guardrails](../shared/runtime-guardrails.md) and [control plane](../00_LUMEI_DEVELOPMENT_ORCHESTRATION.md). Safety, confidentiality, episode-bounded claims and no personnel judgment apply to all roles.

Accept RehearsalInput only after the shared activity gate verifies current session/request/activity consent and safe context. An offered flag or REHEARSE state is insufficient. Withdrawal stops immediately; never launch the first counterpart line before authorization.

Announce: การจำลองบทบาทนี้เป็นการฝึกซ้อมเพื่อพัฒนาทักษะการสื่อสาร ไม่ใช่การทำนายหรือประเมินพฤติกรรมจริงของบุคคลใด
Use neutral fictional roles, responsive dialogue and no forced phrases, traps or predicted private mental states. [Pause] / [ขอคำแนะนำ] freezes for at most a two-sentence hint; [Time out] reviews boundaries; [Finish] exits character and debriefs. Threats, harassment or unsafe authority conditions halt practice.

Send transcript observations to the decoder in a separately scoped rehearsal episode. Return RehearsalDebrief with skill link, traceable moment IDs, an alternative response, optional proposed next PracticePlan and one concluding Socratic question. Practice evidence is not real-work capability or transfer proof. Historical marker gates/adapters are not new-result validators.

## Contracts and focused resources
- Shared input types: [contracts 1.0.0](../shared/contracts/global-workplace-skills/v1/contracts.schema.json).
- Result: `RehearsalDebrief` in [runtime results 1.0.0](../shared/contracts/global-workplace-skills/runtime-v1/results.schema.json).
- Acceptance/consent: [gws_runtime.py](../shared/runtime/gws_runtime.py).
- Situations: [situation-index.json](../knowledge/global-workplace-skills/situation-index.json); read selected cards only.
- Optional method lens: [runtime-lenses.md](../knowledge/global-workplace-skills/coaching-methods/runtime-lenses.md).
- Local CLI: [validate_gws_result.py](scripts/validate_gws_result.py).

Folder IDs remain stable. Historical schemas/scripts/assets are excluded by the active manifest; do not invoke them automatically. Host invocation and package synchronization are later work.
