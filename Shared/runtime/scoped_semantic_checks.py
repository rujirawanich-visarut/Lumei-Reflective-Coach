"""Small, explicitly scoped synthesis lint. Never a complete semantic/safety evaluator."""
import re
from gws_runtime import ContractError, validate_result, render_learning_loop
RULES = {
 'PERSONNEL_JUDGMENT': [r'คุณได้\s*\d+\s*(?:คะแนน|/\s*\d+)', r'(?<!ไม่)ควรเลื่อนตำแหน่ง', r'you deserve (?:a promotion|a rating)'],
 'STABLE_IDENTITY': [r'คุณเป็นคน(?:ซื่อสัตย์|ยืดหยุ่น|ไม่ยืดหยุ่น|ขี้กลัว|ไร้ความสามารถ)', r'you are (?:an inherently|a naturally)'],
 'UNVERIFIED_LEARNING': [r'พิสูจน์แล้วว่าคุณ(?:เชี่ยวชาญ|เรียนรู้สำเร็จ)', r'you have mastered'],
 'UNSAFE_AUTHORIZATION': [r'(?<!ไม่)อนุมัติให้(?:เดินเครื่อง|ข้ามขั้นตอน|deploy)', r'you may bypass (?:approval|safety)']}
def check_learning_loop(payload):
    validate_result('LearningLoopResult',payload)
    # Generated synthesis fields only; raw episode items are not scanned. Quoted text
    # inside synthesis can still need manual review. This lint cannot parse all negation/context.
    fields = [payload[k] for k in ('supported_summary','alternative_learning','causal_hypothesis','working_approach') if payload[k]]
    fields += [a['bounded_rationale'] for a in payload['context']['session']['anchors']]
    text = '\n'.join(fields)
    for code, patterns in RULES.items():
        if any(re.search(pattern,text,re.I) for pattern in patterns):
            raise ContractError(code,'/generated_synthesis','Scoped review pattern; revise or obtain semantic review')
    rendered = render_learning_loop(payload)
    if payload['context']['session']['state'] in {'QUICK_REFLECT','TARGETED_QUESTION'} and len(rendered)>700:
        raise ContractError('QUICK_REFLECT_TOO_LONG','/generated_synthesis','Reference quick-reflect budget is 700 characters')
    return {'status':'pass-scoped-checks','requires_semantic_review':True,'rendered':rendered}
