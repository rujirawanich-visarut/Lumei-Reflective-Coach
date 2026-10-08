---
id: LUMEI-DEVELOPMENT-ORCHESTRATION-001
title: Lumei Development Orchestration
version: 3.0.0
status: local-integration-awaiting-host-validation
runtime_instruction: Instruction_v5.1.md
host: portable-not-selected
---
# Lumei Development Orchestration — v3.0

Instruction_v5.1.md and shared/runtime-guardrails.md govern the five roles. Active files are listed in release/phase5/active-runtime-manifest.json. This is a local integration inventory, not a deployment configuration. Library release candidate 0.2.0 contains 14 cards and its active contract projections at knowledge/global-workplace-skills/contract-cards.json; historical Phase 3 projections are regression fixtures. Editorial cards validate against shared/contracts/global-workplace-skills/editorial-v1/cards.schema.json.

## Ownership and roles
Decoder is the only canonical evidence writer; orchestration owns RuntimeContext.session. Decoder transport transfers that store into the session, rather than a second persistent store. Specialists read scoped IDs and return bounded results. New observations pass through decoder intake; old IDs and verification status remain unchanged unless actual authorized checking warrants a change.

RuntimeContext labels evidence_context=workplace, rehearsal or prototype. Practice has a separate episode_id; fictional/sandbox results do not become real-work observations or transfer proof. A linked skill does not imply an anchor is demonstrated.

| Retained folder ID | Role | Result |
|---|---|---|
| lumei-star-l-decoder | Narrative Decoder | NarrativeDecodeResult |
| lumei-star-learning-loop-coach | Learning Loop Coach | LearningLoopResult |
| tactical-empathy-simulator | Conversation Rehearsal | RehearsalDebrief |
| lumei-functional-competency-development-coach | Workplace Skills Specialist | WorkplaceSkillsResult |
| lumei-human-ai-operational-maker-coach | Human–AI Maker Coach | MakerCoachResult |

Shared contracts are shared/contracts/global-workplace-skills/v1/contracts.schema.json (1.0.0). Consumer results are shared/contracts/global-workplace-skills/runtime-v1/results.schema.json (1.0.0). Validate through shared/runtime/gws_runtime.py. Legacy adapters are explicit at shared/contracts/global-workplace-skills/v1/legacy_adapter.py; no Lumei pillar/code conversion into global sources.

Host acceptance calls accept_decode for decoder intake and validate_handoff for every consumer result against the current authoritative context. Self-contained validate_result and skill CLIs check shape/references; they cannot authenticate an output's context. accept_mapping binds specialist output before accepting candidates; the coach still narrows correspondence. Call authorize_activity before any activity invocation. A passed CLI or rendered example is not permission to execute.

## Routing and canonical states
INTAKE is a control event, not a persisted state. Safety/high-consequence boundaries precede all development routes.
- Supplied safety stop → ESCALATE_TO_AUTHORIZED_PROCESS; no practice.
- Missing action or material decision context → QUICK_REFLECT → TARGETED_QUESTION; zero anchors.
- Supported workplace episode → DECODE_P_STAR_L → INTERPRET → MAP_WORKPLACE_SKILLS → SELECT_ONE_DEVELOPMENT_EDGE.
- One chosen edge → optional EXPERIMENT, REHEARSE or MAKER_CO_CREATE after scoped consent and authority checks.
- Rehearsal → DEBRIEF; maker → ARTIFACT; return to reflection or NEW_EVIDENCE_LOOP.
- New workplace evidence → decoder intake again. Preserve separate rehearsal/prototype scope.

A reported result is useful but not mandatory for reflection. Never fabricate outcome, mechanism or alternative learning to fill a template. The reference route helper uses structured controller flags, not natural-language inference; host must supply trustworthy context and safety decisions.

## Knowledge and mapping
Read knowledge/global-workplace-skills/situation-index.json, selected cards and exact source registry/curation references. Mappings have 0–3 anchors with current episode IDs, reviewed action and that action's behavioral support. Card selection is only a candidate; coach accepts or narrows according to actual correspondence, then owns one development edge and one concluding question.

iCD pointers are not definitions; Finland overlays guide coaching; WEF foresight guides curation, not individual assessment. Specialty procedures are out of scope. Kernel RI-01..RI-13 is an optional epistemic lens. The portable situational playbook and coaching-methods/runtime-lenses.md replace automatic retrieval of full legacy Wave dossiers. No active route requires old organizational dictionary PDFs, historical indexes or every scouting PDF.

## Consent, safety and host interface
Offer is not execute. Activity input requires consent.user_opt_in, activity, request_id and user_statement_ref. Execute requires a genuine current user choice bound to session/request/activity, no withdrawal and safe authorized sandbox conditions. Shared runtime authorizes against caller-supplied trusted choice records and the controller's current_request_id; schemas cannot authenticate a human click. Host must enforce withdrawal, actual access rights and organizational permission before tools.

Maker high consequence never executes. Simulator announces fictional practice and preserves pause/time-out/finish controls. Maker produces PROVISIONAL DRAFT with explicit assumptions, human review, reversible sandbox trials and stop conditions. User opt-in is separate from operational authorization. No network probe proves isolation.

## Synthesis
Quick Reflect is short: visible facts, material gap and one question, with no forced behavioral signal. Golden Hybrid scales with evidence. working_approach describes a next strategy, never identity. Preserve reported/inspected distinctions, uncertainty and optional transfer. Reasoning maps are not causal proof; artifact quality is not learning evidence.

Reflective answers and debriefs end with exactly one question. The renderer enforces a final question field and single question-mark form; semantic review remains necessary. Safety escalations and standalone artifacts have their own format.

## Release boundaries
The active manifest excludes old schemas/gates/adapters and dictionary indexes from automatic loading. Legacy instruction and original ZIP/DOCX files remain for rollback; package synchronization is Phase 6. No host has been selected or smoke-tested. Phase 5 provides the curated release candidate and scoped semantic/tabletop review; it does not establish live LLM behavior or learning efficacy.
