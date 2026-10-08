"""Local contract integration and activity gates; host LLM/tool invocation is external."""
import importlib
import json
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if 'lumei_gws_contracts' not in sys.modules:
    package = types.ModuleType('lumei_gws_contracts')
    package.__path__ = [str(ROOT / 'shared/contracts/global-workplace-skills/v1')]
    sys.modules['lumei_gws_contracts'] = package
V = importlib.import_module('lumei_gws_contracts.validation')
ContractError = V.ContractError
BUNDLE = V.read(ROOT / 'shared/contracts/global-workplace-skills/runtime-v1/results.schema.json')
V.Draft202012Validator.check_schema(BUNDLE)
SCHEMAS = V.SCHEMAS.with_resource(BUNDLE['$id'], V.Resource.from_contents(BUNDLE))

def check_shape(name, payload):
    if name not in BUNDLE['$defs']: raise ContractError('UNKNOWN_RUNTIME_CONTRACT', '/', name)
    schema = {'$ref': BUNDLE['$id'] + '#/$defs/' + name}
    errors = list(V.Draft202012Validator(schema, registry=SCHEMAS).iter_errors(payload))
    if errors:
        e = errors[0]
        raise ContractError('SCHEMA_INVALID', '/' + '/'.join(map(str, e.path)), e.message)

def question(text):
    # Controlled field/layout check, not a claim of natural-language semantic validation.
    if text.count('?') != 1 or not text.strip().endswith('?') or '\n' in text:
        raise ContractError('QUESTION_FORM_INVALID', '/socratic_question', 'Use one final single-line question')

def validate_context(context):
    check_shape('RuntimeContext', context)
    V.validate('DevelopmentSession', context['session'])
    if context['evidence_context'] != 'workplace' and context['session']['anchors']:
        raise ContractError('PRACTICE_AS_WORKPLACE_ANCHOR', '/session/anchors', 'Practice observations do not demonstrate real-work skills')
    return context['session']['episode_evidence']

def resolve(ids, store, kinds=None):
    items = {e['evidence_id']: e for e in store['items']}
    for eid in ids:
        if eid not in items: raise ContractError('UNKNOWN_EVIDENCE', '/evidence_ids', eid)
        if kinds is not None and items[eid]['kind'] not in kinds:
            raise ContractError('WRONG_EVIDENCE_KIND', '/evidence_ids', eid)

def validate_result(name, payload):
    check_shape(name, payload)
    if name == 'RuntimeContext': return validate_context(payload)
    if name == 'NarrativeDecodeResult':
        store = payload['episode_evidence']; V.validate('EpisodeEvidenceStore', store)
        resolve(payload['p_star_l']['action_evidence_ids'], store, {'action'})
        resolve(payload['p_star_l']['result_evidence_ids'], store, {'outcome', 'reported_claim'})
        for ids in payload['calming_anchor_observations'].values(): resolve(ids, store, {'action', 'quote'})
        return payload
    store = validate_context(payload['context'])
    if name == 'WorkplaceSkillsResult':
        if payload['context']['evidence_context'] != 'workplace' and payload['candidate_anchors']:
            raise ContractError('PRACTICE_AS_WORKPLACE_ANCHOR', '/candidate_anchors', 'Separate practice scope')
        V.validate('RetrievalResult', payload['retrieval_result'])
        if payload['retrieval_result']['episode_id'] != store['episode_id']:
            raise ContractError('EPISODE_MISMATCH', '/retrieval_result', 'Different episode')
        if len(payload['candidate_anchors']) > payload['retrieval_result']['anchor_limit']:
            raise ContractError('RETRIEVAL_BOUND_EXCEEDED', '/candidate_anchors', 'Respect retrieval bound/fallback')
        for anchor in payload['candidate_anchors']:
            V.validate('CapabilityAnchor', anchor, store)
            if anchor['skill_id'] not in payload['retrieval_result']['card_ids']:
                raise ContractError('ANCHOR_OUTSIDE_RETRIEVAL', '/candidate_anchors', anchor['skill_id'])
    elif name == 'LearningLoopResult':
        question(payload['socratic_question'])
        state = payload['context']['session']['state']
        if state in {'QUICK_REFLECT', 'TARGETED_QUESTION'} and payload['context']['session']['anchors']:
            raise ContractError('QUICK_REFLECT_HAS_ANCHORS', '/session/anchors', 'Clarify before mapping')
    elif name in {'RehearsalDebrief', 'MakerCoachResult'}:
        expected = 'rehearsal' if name == 'RehearsalDebrief' else 'prototype'
        if payload['context']['evidence_context'] != expected:
            raise ContractError('PRACTICE_SCOPE_REQUIRED', '/evidence_context', expected)
        if payload['skill_id'] not in {c['skill_id'] for c in V.card_catalog()}:
            raise ContractError('UNKNOWN_SKILL', '/skill_id', payload['skill_id'])
        if payload['next_practice_plan'] is not None:
            V.validate('PracticePlan', payload['next_practice_plan'])
            if payload['next_practice_plan']['skill_id'] != payload['skill_id']:
                raise ContractError('PRACTICE_SKILL_MISMATCH', '/next_practice_plan', payload['skill_id'])
        if name == 'RehearsalDebrief':
            resolve(payload['traceable_moment_evidence_ids'], store, {'action', 'quote'})
            question(payload['socratic_question'])
        else:
            resolve(payload['verification_evidence_ids'], store)
            resolve(payload['learning_evidence_ids'], store)
    return payload

def accept_decode(context, decoded):
    """Caller transfers decoder store, retaining one authoritative session owner."""
    validate_context(context); validate_result('NarrativeDecodeResult', decoded)
    if decoded['episode_evidence']['session_id'] != context['session']['session_id']:
        raise ContractError('SESSION_MISMATCH', '/episode_evidence', 'Decoder cannot write another session')
    old = context['session']['episode_evidence']
    new = decoded['episode_evidence']
    if old['episode_id'] == new['episode_id']:
        if context['evidence_context'] != decoded['evidence_context'] or old['episode_scope'] != new['episode_scope']:
            raise ContractError('EPISODE_SCOPE_CHANGE', '/episode_evidence', 'Create a separate episode for practice or scope changes')
        existing = {e['evidence_id']: e for e in new['items']}
        if any(e['evidence_id'] not in existing or existing[e['evidence_id']] != e for e in old['items']):
            raise ContractError('EVIDENCE_REWRITE', '/episode_evidence', 'Use explicit verified revision workflow; do not silently rewrite')
    updated = {**context, 'evidence_context': decoded['evidence_context'],
      'session': {**context['session'], 'state': 'INTERPRET', 'episode_evidence': new, 'anchors': [],
                  'reasoning_map': None, 'practice_plan': None,
                  'selected_development_edge': context['session']['selected_development_edge']
                    if old['episode_id'] == new['episode_id'] or decoded['evidence_context'] != 'workplace' else None}}
    validate_context(updated)
    return updated

def validate_handoff(name, payload, current_context):
    """Bind consumer output to authoritative host context, not its self-reported store."""
    validate_context(current_context); validate_result(name, payload)
    if name not in {'LearningLoopResult', 'WorkplaceSkillsResult', 'RehearsalDebrief', 'MakerCoachResult'}:
        raise ContractError('UNKNOWN_CONSUMER', '/', name)
    output = payload['context']
    if (output['session']['session_id'] != current_context['session']['session_id']
        or output['session']['episode_evidence'] != current_context['session']['episode_evidence']
        or any(output[k] != current_context[k] for k in ('evidence_context', 'language', 'personnel_use_plausible', 'consequence_level', 'current_request_id'))):
        raise ContractError('CONTEXT_REWRITE', '/context', 'Consumer cannot replace evidence or trusted controller flags')
    if name != 'LearningLoopResult' and output['session'] != current_context['session']:
        raise ContractError('SESSION_REWRITE', '/context/session', 'Specialists are read-only consumers')
    return payload

def accept_mapping(context, result):
    validate_handoff('WorkplaceSkillsResult', result, context)
    updated = {**context, 'session': {**context['session'], 'anchors': result['candidate_anchors'],
               'state': 'SELECT_ONE_DEVELOPMENT_EDGE'}}
    validate_context(updated)
    return updated

def authorize_activity(name, payload, context, trusted_choices, withdrawn_requests=(), operational_authorized=False, boundary_stop=False):
    """Host supplies genuine current user choices and permissions; no inference from prose."""
    if name not in {'RehearsalInput', 'MakerInput'}:
        raise ContractError('UNKNOWN_ACTIVITY', '/', name)
    store = validate_context(context)
    V.validate(name, payload, store)
    if boundary_stop or context['consequence_level'] == 'high':
        raise ContractError('SAFETY_STOP', '/', 'Development activity halted')
    if payload['command'] == 'offer': return {'status': 'offered', 'execute_allowed': False}
    consent = payload['consent']
    if consent['request_id'] in withdrawn_requests:
        raise ContractError('CONSENT_WITHDRAWN', '/consent/request_id', 'Stop activity')
    if consent['request_id'] != context['current_request_id']:
        raise ContractError('STALE_CONSENT', '/consent/request_id', 'Different current request')
    choice = trusted_choices.get(consent['user_statement_ref'])
    expected = {'session_id': payload['session_id'], 'request_id': consent['request_id'],
                'activity': consent['activity'], 'user_opt_in': True}
    if not isinstance(choice, dict) or any(choice.get(k) != v for k, v in expected.items()):
        raise ContractError('CONSENT_NOT_CONFIRMED', '/consent/user_statement_ref', 'No matching genuine user-choice record')
    if not operational_authorized:
        raise ContractError('AUTHORITY_REQUIRED', '/', 'Opt in does not establish sandbox authority')
    return {'status': 'authorized', 'execute_allowed': True}

def route(context, intent='reflect', decision_context_known=True, boundary_stop=False):
    validate_context(context)
    if boundary_stop or context['consequence_level'] == 'high': return 'ESCALATE_TO_AUTHORIZED_PROCESS'
    store = context['session']['episode_evidence']
    action = any(e['kind'] == 'action' and e['verification'] != 'unverified' for e in store['items'])
    if not action or not decision_context_known: return 'TARGETED_QUESTION'
    if context['evidence_context'] != 'workplace': return 'DEBRIEF' if context['evidence_context'] == 'rehearsal' else 'ARTIFACT'
    return 'MAP_WORKPLACE_SKILLS'  # practice intents still need an activity input and authorization gate

def render_learning_loop(payload):
    validate_result('LearningLoopResult', payload)
    context = payload['context']; session = context['session']
    lines = [payload['supported_summary']]
    if session['state'] not in {'QUICK_REFLECT', 'TARGETED_QUESTION'}:
        for anchor in session['anchors']:
            lines.append(anchor['display_name'] + ': ' + anchor['bounded_rationale'])
        if payload['causal_hypothesis']: lines.append('สมมติฐานที่ยังต้องตรวจ: ' + payload['causal_hypothesis'])
        if payload['alternative_learning']: lines.append(payload['alternative_learning'])
        if payload['working_approach']: lines.append('แนวทางที่ลองได้: ' + payload['working_approach'])
        if session['selected_development_edge']: lines.append('จุดพัฒนาหนึ่งเรื่อง: ' + session['selected_development_edge'])
        if session['practice_plan']:
            lines.append('แนวทางฝึกที่เลือกได้: ' + session['practice_plan']['learner_attempt'])
            lines.append('หลักฐานสำหรับ feedback: ' + session['practice_plan']['feedback_basis'])
        if payload['rehearsal_offered']: lines.append('เลือกซ้อมบทสนทนาได้เมื่อคุณยินยอม')
        if payload['maker_offered']: lines.append('เลือกทำต้นแบบด้วยข้อมูลที่ได้รับอนุญาตได้เมื่อคุณยินยอม')
    if context['personnel_use_plausible']:
        lines.append('ข้อสะท้อนนี้อ้างอิงเฉพาะเรื่องเล่าและหลักฐานที่ให้มา ไม่ควรใช้เป็นหลักฐานเดี่ยวสำหรับการประเมินบุคคล')
    if any('?' in line for line in lines):
        raise ContractError('EXTRA_VISIBLE_QUESTION', '/', 'Keep questions in the final question field')
    lines.append(payload['socratic_question'])
    return '\n\n'.join(lines)

def cli(expected_contract):
    import argparse
    parser = argparse.ArgumentParser(description='Validate a versioned Lumei result locally; does not invoke an agent')
    parser.add_argument('payload', type=Path)
    args = parser.parse_args()
    try:
        validate_result(expected_contract, V.read(args.payload))
    except (ContractError, ValueError, OSError) as error:
        print(str(error)); return 2
    print('PASS ' + expected_contract); return 0
