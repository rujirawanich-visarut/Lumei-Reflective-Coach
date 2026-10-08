# Proposed Global Workplace Skills Contracts — 1.0.0

Phase 3 contract set; **not connected to legacy consumers**. Runtime instruction, orchestration,
old schemas and packages remain unchanged until integration in Phase 4.

`contracts.schema.json` defines 15 types under `$defs`, using JSON Schema Draft 2020-12.
`urn:lumei:gws:contracts:1.0.0` is an offline identifier. The local registry resolves every
contract reference without accessing a schema server.

Core types: KnowledgeSourceRef, WorkplaceSkillCard, CapabilityAnchor, PracticePlan,
ReasoningMap. Supporting types: Locator, EvidenceItem, EpisodeEvidenceStore,
ObservableAction, DevelopmentSession, Consent, RehearsalInput, MakerInput,
RetrievalRequest and RetrievalResult.

Every versioned contract requires `schema_version: "1.0.0"`. Nested value types inherit
the enclosing version. No old contract is re-labelled as a new contract.

`validation.py` uses a real Draft202012Validator and then checks evidence/card/source IDs,
versions, locators, support roles and session ownership. Schema-only checks cannot prove
reference existence or source truth. `validate(name, payload, episode)` is the entry point.
`retrieve(request, episode)` is a deterministic reference selector for the specification;
it returns candidates, never generated competency anchors or skill scores.

`legacy_adapter.py` accepts explicit legacy contract names. Narrative v5 retains arrays
through stable IDs and a compatibility map. Lumei learning-loop anchors return REMAP_REQUIRED.
Activity adaptation requires canonical evidence, IDs and fresh explicit consent context.
Unsupported v4.2/session/functional/result contracts return a typed error; they are not
silently coerced. The proposed adapter does not replace the old adapter yet.

Install the pinned [requirements](../../../../release/phase3/requirements.txt) into
`.dependencies/phase3` using the selected Python environment and `pip install --target`.
Run `python release/phase3/test_contracts.py` from the project root. Tests use local data;
no network access is needed after dependency installation. Local dependency binaries must
be reinstalled for the destination environment, not copied across hosts.

See [retrieval specification](../../../../release/phase3/RETRIEVAL_CONTRACT.md),
[migration table](../../../../release/phase3/FIELD_MIGRATION_TABLE.md) and
[Phase 3 report](../../../../release/phase3/PHASE_3_CONTRACT_REPORT.md).
