---
title: Lumei Global Workplace Situational Playbook
version: 2.1.0
runtime_instruction: Instruction_v5.1.md
status: release-candidate-awaiting-human-and-host-review
---
# Situational playbook

Library RC 0.2.0: start from the episode, not role title or organizational pillar. Canonical cues and distinctions are in knowledge/global-workplace-skills/situation-index.json. The table selects candidates, not evidence of competence. Read selected cards only; allow zero anchors when none fits.

| Situation | Card | ใช้เมื่อ |
|---|---|---|
| S01 | GWS-clarify-work | ได้รับคำขอที่เป้าหมาย ผลส่งมอบ หรือข้อจำกัดยังไม่ชัด |
| S02 | GWS-check-evidence | ข้อมูลหลายแหล่งไม่ตรงกัน หรือข้อสรุปยังมีหลักฐานไม่พอ |
| S03 | GWS-choose-action | ต้องเลือกทางทำงาน แม้ข้อมูลหรือผลลัพธ์ยังไม่แน่นอน |
| S04 | GWS-work-through-disagreement | มีความเห็นต่างที่คุยได้อย่างปลอดภัยและต้องกำหนดสิ่งที่จะทำต่อร่วมกัน |
| S05 | GWS-coordinate-across-boundaries | งานต้องอาศัยคนต่างทีมที่ผู้ใช้ไม่มีอำนาจสั่งการ |
| S06 | GWS-manage-priorities | งานหลายชิ้นแย่งเวลา หรือภาระงานเกินทรัพยากรที่มี |
| S07 | GWS-handoff-and-follow-through | งานเปลี่ยนผู้ทำ/กะ/ทีม หรือมีข้อตกลงที่ต้องตามต่อ |
| S08 | GWS-learn-and-transfer | มี feedback ความผิดพลาด หรือการลองครั้งหนึ่งที่อยากนำไปปรับครั้งถัดไป |
| S09 | GWS-verify-ai-work | ใช้ AI ช่วยงานและต้องพิจารณาว่าอะไรเชื่อถือได้ อะไรต้องตรวจหรือให้ผู้รับผิดชอบตัดสินใจ |
| S10 | GWS-improve-with-small-experiments | พบปัญหาคุณภาพหรือขั้นตอนซ้ำ และมีพื้นที่ทดลองที่ปลอดภัยในขอบเขตอำนาจ |
| S11 | GWS-understand-recipient-needs | ผู้รับบริการภายในหรือภายนอกแจ้งปัญหาและต้องตกลงการช่วยเหลือที่ทำได้จริง |
| S12 | GWS-communicate-across-backgrounds | คนเกี่ยวข้องมีภาษา ประสบการณ์ ช่องทางหรือข้อจำกัดการเข้าถึงต่างกันและต้องเข้าใจเรื่องเดียวกัน |
| S13 | GWS-adapt-to-changing-work | ข้อกำหนด เครื่องมือหรือวิธีทำงานเปลี่ยนและแผนเดิมอาจใช้ต่อไม่ได้ |
| S14 | GWS-maintain-trust-and-information-boundaries | ต้องรักษาความไว้วางใจเมื่อมีคำมั่น ข้อมูลที่แบ่งปันไม่ได้ หรือคำขอที่เกินขอบเขต |

Decoder writes one canonical evidence store; orchestration owns it. Workplace Skills Specialist returns 0–3 bounded candidates with eligible action IDs and exact action knowledge refs. Coach narrows correspondence, owns one development edge and one final question. Missing action/context leads to short Quick Reflect and a targeted question, with no fabricated outcome.

Use knowledge/global-workplace-skills/coaching-methods/runtime-lenses.md selectively. Rehearsal/Maker are optional branches gated by current genuine choice, withdrawal checks and actual authority. Their separate practice episodes may link a card but have zero workplace anchors. New real-work evidence returns through decoder. Safety stops precede every development route.

Full Wave dossiers, organizational dictionaries/indexes and Maker SKU remain outside automatic retrieval. Domain procedures require actual authorized sources/people. Existing DOCX is historical and awaits Phase 6 regeneration; Markdown is canonical for this RC. Active inventory: release/phase5/active-runtime-manifest.json.
