"""Explicit staged adapters. Never infer GWS anchors, source authority, or consent."""
import hashlib
from .validation import ContractError, ROOT, read, validate, Draft202012Validator

STATE_ALIASES = {'ONE_TARGETED_QUESTION': 'TARGETED_QUESTION',
                 'MAP_COMPETENCY': 'MAP_WORKPLACE_SKILLS', 'MAP_FUNCTIONAL_COMPETENCY': 'MAP_WORKPLACE_SKILLS'}

def normalize_state(state):
    from .validation import BUNDLE
    normalized = STATE_ALIASES.get(state, state) if isinstance(state, str) else None
    if normalized not in BUNDLE['$defs']['DevelopmentSession']['properties']['state']['enum']:
        raise ContractError('LEGACY_STATE_UNSUPPORTED', '/state', str(state))
    return normalized

def adapt_legacy(contract_name, payload, **context):
    if contract_name == 'NarrativeDecodeResult':
        return adapt_narrative_v5(payload, context.get('episode_id'), context.get('session_id'))
    if contract_name == 'LearningLoopResult': return adapt_learning_loop_v5(payload)
    if contract_name in {'RehearsalHandoff', 'MakerCoachInput'}:
        return adapt_activity_v5('rehearsal' if contract_name == 'RehearsalHandoff' else 'maker', payload, context)
    raise ContractError('LEGACY_CONTRACT_UNSUPPORTED', '/', 'Explicit adapter unavailable: ' + str(contract_name))

def adapt_narrative_v5(payload, episode_id, session_id):
    old = read(ROOT / 'lumei-star-l-decoder/schemas/narrative-decode-result.schema.json')
    errors = list(Draft202012Validator(old).iter_errors(payload))
    if errors:
        raise ContractError('LEGACY_INVALID', '/narrative', errors[0].message)
    if not isinstance(episode_id, str) or not episode_id or not isinstance(session_id, str) or not session_id:
        raise ContractError('CONTEXT_REQUIRED', '/', 'Explicit episode/session IDs required')
    store = {'schema_version': '1.0.0', 'session_id': session_id, 'episode_id': episode_id, 'episode_scope': payload['episode_scope'],
       'items': [], 'unknowns': payload['unknowns'][:], 'contradictions': payload['contradictions'][:],
       'alternative_explanations': [payload['alternative_explanation']] if payload.get('alternative_explanation') else []}
    by_key, mapping = {}, {}
    def add(text, kind, path):
        if not text.strip():
            raise ContractError('LEGACY_EMPTY_EVIDENCE', path, 'Empty statements are not coerced')
        key = (kind, text)
        if key not in by_key:
            digest = hashlib.sha256((episode_id + '\0' + kind + '\0' + text).encode()).hexdigest()[:24]
            item = {'evidence_id': 'EV-' + digest, 'kind': kind, 'statement': text,
              'verification': 'user_reported', 'source_ref': None, 'origin_paths': []}
            by_key[key] = item
            store['items'].append(item)
        item = by_key[key]
        item['origin_paths'].append(path)
        mapping[path] = item['evidence_id']
    for field, kind in [('verbatim', 'quote'), ('observable_actions', 'action'),
                        ('documented_outputs', 'artifact'), ('reported_claims', 'reported_claim')]:
        for i, text in enumerate(payload['evidence'][field]): add(text, kind, f'/evidence/{field}/{i}')
    for field, kind in [('actions', 'action'), ('results', 'outcome')]:
        for i, text in enumerate(payload['p_star_l'][field]): add(text, kind, f'/p_star_l/{field}/{i}')
    session = {'schema_version': '1.0.0', 'session_id': session_id, 'state': 'TARGETED_QUESTION',
      'episode_evidence': store, 'anchors': [], 'selected_development_edge': None,
      'practice_plan': None, 'reasoning_map': None}
    validate('DevelopmentSession', session)
    return {'session': session, 'compatibility_map': mapping,
      'retained_legacy_context': {'p_star_l': {k: v for k, v in payload['p_star_l'].items() if k not in {'actions', 'results'}},
        'source_pointers': payload['evidence']['source_refs'][:], 'friction_signal': payload['friction_signal'],
        'calming_anchor_observations': payload['calming_anchor_observations'], 'prohibited': payload['prohibited']},
      'migration_note': 'Old narrative values retained; source pointers and interpretations are not knowledge refs or verified action evidence. Re-map from canonical episode.'}

def adapt_learning_loop_v5(payload):
    old = read(ROOT / 'lumei-star-learning-loop-coach/schemas/learning-loop-result.schema.json')
    errors = list(Draft202012Validator(old).iter_errors(payload))
    if errors: raise ContractError('LEGACY_INVALID', '/learning_loop', errors[0].message)
    raise ContractError('REMAP_REQUIRED', '/capability_anchors',
        'Lumei pillar/competency names have no automatic GWS equivalence. Preserve legacy record separately and map canonical evidence again.')

def adapt_activity_v5(kind, payload, context):
    name = 'RehearsalInput' if kind == 'rehearsal' else 'MakerInput' if kind == 'maker' else None
    if name is None: raise ContractError('UNKNOWN_ACTIVITY', '/', str(kind))
    path = 'tactical-empathy-simulator/schemas/rehearsal-handoff.schema.json' if kind == 'rehearsal' else 'lumei-human-ai-operational-maker-coach/schemas/maker-coach-input.schema.json'
    errors = list(Draft202012Validator(read(ROOT / path)).iter_errors(payload))
    if errors: raise ContractError('LEGACY_INVALID', '/activity', errors[0].message)
    if not isinstance(context, dict) or any(k not in context for k in ['session_id', 'skill_id', 'consent', 'episode_evidence', 'episode_evidence_ids', 'command']):
        raise ContractError('CONSENT_CONTEXT_REQUIRED', '/', 'Caller must supply canonical IDs and explicit activity consent; offered/accepted legacy flags are insufficient')
    out = {'schema_version': '1.0.0', 'session_id': context['session_id'], 'skill_id': context['skill_id'],
       'development_edge': payload['selected_development_edge'] if kind == 'rehearsal' else context.get('development_edge'),
       'consent': context['consent'], 'command': context['command'], 'known_constraints': payload['known_constraints'],
       'explicit_unknowns': payload['explicit_unknowns'] if kind == 'rehearsal' else [],
       'episode_evidence_ids': context['episode_evidence_ids']}
    if kind == 'rehearsal':
        out.update(fictional_counterpart_role=payload['fictional_counterpart_role'], conversation_goal=payload['intended_conversation_outcome'])
    else:
        out.update({k: payload[k] for k in ['work_problem', 'intended_value', 'users_or_stakeholders', 'decision_rights', 'prohibited_actions', 'consequence_level']})
    validate(name, out, context['episode_evidence'])
    return {'input': out, 'retained_legacy_context': {'authorised_evidence': payload.get('authorised_evidence', []),
            'prohibited_transfers': payload.get('prohibited_transfers', [])},
      'migration_note': 'Legacy source labels retained separately. Consent and evidence IDs supplied explicitly, not inferred.'}
