"""Offline full schema + referential checks for proposed contracts; no host execution."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except (ImportError, ModuleNotFoundError):
    sys.path.insert(0, str(ROOT / '.dependencies/phase3'))
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

HERE = Path(__file__).resolve().parent
BUNDLE = json.loads((HERE / 'contracts.schema.json').read_text(encoding='utf-8'))
Draft202012Validator.check_schema(BUNDLE)
SCHEMAS = Registry().with_resource(BUNDLE['$id'], Resource.from_contents(BUNDLE))

class ContractError(ValueError):
    def __init__(self, code, path, message):
        self.code, self.path = code, path
        super().__init__(f'{code} at {path}: {message}')

def read(path): return json.loads(path.read_text(encoding='utf-8'))

def card_catalog():
    # Active RC projections live with knowledge; Phase 3 file stays historical.
    path = ROOT / 'knowledge/global-workplace-skills/contract-cards.json'
    if not path.exists():
        if (ROOT / 'release/phase5/active-runtime-manifest.json').exists():
            raise ContractError('ACTIVE_CATALOG_MISSING', '/contract-cards', 'RC inventory requires its active catalog; no silent pilot downgrade')
        path = ROOT / 'release/phase3/projected-cards.json'
    return read(path)

def validate_schema(name, payload):
    if name not in BUNDLE['$defs']:
        raise ContractError('UNKNOWN_CONTRACT', '/', name)
    schema = {'$schema': BUNDLE['$schema'], '$ref': BUNDLE['$id'] + '#/$defs/' + name}
    validator = Draft202012Validator(schema, registry=SCHEMAS)
    errors = sorted(validator.iter_errors(payload), key=lambda e: str(list(e.path)))
    if errors:
        error = errors[0]
        raise ContractError('SCHEMA_INVALID', '/' + '/'.join(map(str, error.path)), error.message)

def knowledge_ref(r):
    review = {c['candidate_id']: c for c in read(ROOT / 'knowledge/global-workplace-skills/curation-candidates.json')['candidates']}
    sources = {s['source_id']: s for s in read(ROOT / 'knowledge/global-workplace-skills/source-registry.json')['sources']}
    original = review.get(r['candidate_id'])
    if original is None or original['decision'] not in {'include', 'adapt'}:
        raise ContractError('SOURCE_NOT_CLEARED', '/knowledge_refs', r['candidate_id'])
    if (r['source_id'] != original['source_id'] or r['version'] != sources[original['source_id']]['version']
        or r['supported_claim'] != original['source_claim'] or r['adaptation_status'] != original['decision']):
        raise ContractError('SOURCE_DRIFT', '/knowledge_refs', r['candidate_id'])
    try:
        locator = json.loads(r['locator']['reference'])
    except (ValueError, TypeError) as error:
        raise ContractError('LOCATOR_INVALID', '/locator/reference', str(error)) from error
    if locator != original['locator'] or r['locator']['kind'] != original['locator']['type']:
        raise ContractError('LOCATOR_DRIFT', '/locator', r['candidate_id'])
    if r['support_role'] == 'behavior_support' and (original['kind'] != 'behavior' or original['source_id'] == 'ICD-V4-SKILL'):
        raise ContractError('LENS_AS_BEHAVIOR', '/support_role', r['candidate_id'])

def validate(name, payload, episode=None):
    validate_schema(name, payload)
    cards = {c['skill_id']: c for c in card_catalog()}
    def card_for(sid):
        if sid not in cards:
            raise ContractError('UNKNOWN_SKILL', '/skill_id', sid)
        return cards[sid]
    def evidence_store(store):
        validate_schema('EpisodeEvidenceStore', store)
        ids = [e['evidence_id'] for e in store['items']]
        if len(ids) != len(set(ids)):
            raise ContractError('DUPLICATE_EVIDENCE_ID', '/episode_evidence/items', 'IDs must be unique')
        return {e['evidence_id']: e for e in store['items']}
    def resolve(ids, action_only=False):
        if episode is None:
            raise ContractError('EPISODE_REQUIRED', '/episode_evidence_ids', 'Supply canonical store')
        items = evidence_store(episode)
        for eid in ids:
            if eid not in items:
                raise ContractError('UNKNOWN_EVIDENCE', '/episode_evidence_ids', eid)
            if action_only and (items[eid]['kind'] != 'action' or items[eid]['verification'] == 'unverified'):
                raise ContractError('INELIGIBLE_ACTION_EVIDENCE', '/episode_evidence_ids', eid)
    if name == 'KnowledgeSourceRef': knowledge_ref(payload)
    elif name == 'WorkplaceSkillCard':
        original = read(ROOT / 'knowledge/global-workplace-skills/cards' / (payload['skill_id'] + '.json')) if payload['skill_id'] in cards else None
        if not original or payload['display_name'] != original['title_th']:
            raise ContractError('CARD_DRIFT', '/display_name', payload['skill_id'])
        for r in payload['knowledge_refs']: knowledge_ref(r)
        ids = [a['action_id'] for a in payload['observable_actions']]
        if len(ids) != len(set(ids)):
            raise ContractError('DUPLICATE_ACTION_ID', '/observable_actions', 'IDs must be unique')
        if set(ids) != {a['action_id'] for a in original['observable_actions']}:
            raise ContractError('INCOMPLETE_CARD', '/observable_actions', 'Projection must preserve reviewed actions')
        if payload['practice']['skill_id'] != payload['skill_id']:
            raise ContractError('PRACTICE_SKILL_MISMATCH', '/practice/skill_id', 'Practice must belong to card')
        for a in payload['observable_actions']:
            expected = next((x for x in original['observable_actions'] if x['action_id'] == a['action_id']), None)
            if not expected or a['text'] != expected['action']:
                raise ContractError('ACTION_DRIFT', '/observable_actions', a['action_id'])
            if {r['candidate_id'] for r in a['knowledge_refs']} != set(expected['supporting_candidate_ids']):
                raise ContractError('ACTION_SOURCE_DRIFT', '/observable_actions', a['action_id'])
            for r in a['knowledge_refs']:
                knowledge_ref(r)
                if r['support_role'] != 'behavior_support':
                    raise ContractError('LENS_AS_BEHAVIOR', '/observable_actions', r['candidate_id'])
        validate('PracticePlan', payload['practice'])
    elif name == 'EpisodeEvidenceStore': evidence_store(payload)
    elif name == 'CapabilityAnchor':
        c = card_for(payload['skill_id'])
        if payload['display_name'] != c['display_name']:
            raise ContractError('DISPLAY_NAME_DRIFT', '/display_name', payload['skill_id'])
        action = next((a for a in c['observable_actions'] if a['action_id'] == payload['action_id']), None)
        if action is None:
            raise ContractError('UNKNOWN_ACTION', '/action_id', payload['action_id'])
        resolve(payload['episode_evidence_ids'], action_only=True)
        allowed = {r['candidate_id'] for r in action['knowledge_refs']}
        for r in payload['knowledge_refs']:
            knowledge_ref(r)
            if r['candidate_id'] not in allowed or r['support_role'] != 'behavior_support':
                raise ContractError('UNSUPPORTED_ANCHOR_SOURCE', '/knowledge_refs', r['candidate_id'])
    elif name == 'PracticePlan': card_for(payload['skill_id'])
    elif name == 'ReasoningMap': resolve(payload['supporting_evidence_ids'])
    elif name == 'DevelopmentSession':
        store = payload['episode_evidence']
        evidence_store(store)
        if payload['session_id'] != store['session_id']:
            raise ContractError('SESSION_MISMATCH', '/session_id', 'Evidence owner must match session')
        for anchor in payload['anchors']: validate('CapabilityAnchor', anchor, store)
        if payload['practice_plan'] is not None: validate('PracticePlan', payload['practice_plan'])
        if payload['reasoning_map'] is not None: validate('ReasoningMap', payload['reasoning_map'], store)
        if payload['state'] == 'EXPERIMENT' and (not payload['practice_plan'] or not payload['practice_plan']['user_opt_in']):
            raise ContractError('CONSENT_REQUIRED', '/practice_plan', 'EXPERIMENT requires explicit opt in')
    elif name in {'RehearsalInput', 'MakerInput'}:
        card_for(payload['skill_id'])
        resolve(payload['episode_evidence_ids'])
        if payload['session_id'] != episode['session_id']:
            raise ContractError('SESSION_MISMATCH', '/session_id', 'Activity cannot use another session evidence')
    elif name == 'RetrievalRequest':
        if episode is None or payload['episode_id'] != episode['episode_id']:
            raise ContractError('EPISODE_MISMATCH', '/episode_id', 'Request must use canonical store')
        resolve(payload['eligible_action_evidence_ids'], action_only=True)
        known = {s['situation_id'] for s in read(ROOT / 'knowledge/global-workplace-skills/situation-index.json')['situations']}
        if not set(payload['situation_ids']) <= known:
            raise ContractError('UNKNOWN_SITUATION', '/situation_ids', 'Use reviewed situation index')
        if payload['role'] == 'contributor' and payload['managerial_authority_confirmed']:
            raise ContractError('ROLE_AUTHORITY_CONFLICT', '/managerial_authority_confirmed', 'Contributor request cannot open manager branch')
    elif name == 'RetrievalResult':
        for sid in payload['card_ids']: card_for(sid)
        if payload['status'] != 'candidates' and (payload['card_ids'] or payload['anchor_limit']):
            raise ContractError('FALLBACK_HAS_CANDIDATES', '/', 'Fallback must not fabricate anchors/cards')
        expected_states = {'candidates':'MAP_WORKPLACE_SKILLS', 'needs_evidence':'TARGETED_QUESTION',
                           'no_match':'QUICK_REFLECT', 'boundary_stop':'ESCALATE_TO_AUTHORIZED_PROCESS'}
        if payload['fallback_state'] != expected_states[payload['status']]:
            raise ContractError('FALLBACK_STATE_CONFLICT', '/fallback_state', 'Status and state must agree')
        if payload['status'] == 'candidates' and (not payload['card_ids'] or not payload['anchor_limit']
             or len(payload['card_ids']) > payload['anchor_limit']):
            raise ContractError('RETRIEVAL_BOUND_EXCEEDED', '/card_ids', 'Candidates need a nonzero bound and respect it')
    return payload

def retrieve(request, episode, boundary_stop=False):
    """Deterministic reference selection, not an LLM mapper or competence evaluator."""
    validate('RetrievalRequest', request, episode)
    status, state, missing, ids, limit = 'candidates', 'MAP_WORKPLACE_SKILLS', [], [], request['max_anchors']
    if boundary_stop:
        status, state, limit = 'boundary_stop', 'ESCALATE_TO_AUTHORIZED_PROCESS', 0
    elif not request['eligible_action_evidence_ids']:
        status, state, limit, missing = 'needs_evidence', 'TARGETED_QUESTION', 0, ['reported action linked to this episode']
    elif not limit:
        status, state = 'no_match', 'QUICK_REFLECT'
    else:
        index = read(ROOT / 'knowledge/global-workplace-skills/situation-index.json')
        ids = [s['primary_card_id'] for s in index['situations'] if s['situation_id'] in request['situation_ids']][:limit]
    result = {'schema_version': '1.0.0', 'episode_id': episode['episode_id'], 'status': status, 'card_ids': ids,
      'anchor_limit': limit, 'missing_evidence': missing, 'fallback_state': state,
      'selection_rationale': 'Select reviewed situation candidates in index order; mapping still needs bounded episode/action correspondence.'}
    return validate('RetrievalResult', result)
