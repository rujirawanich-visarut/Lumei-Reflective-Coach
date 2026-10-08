---
status: phase-2-editorial-pilot
runtime_authority: false
version: 0.1.0
---

# Global Workplace Skills — Pilot

ชุดนำร่องมี **10 cards ใน 4 กลุ่มเสนอ** เริ่มจากสถานการณ์ที่คนทำงานเจอ จำนวนนี้ไม่ใช่ taxonomy ถาวรหรือ competency levels ทุก card ใช้ได้กับ contributor/manager โดยไม่ต้องมีอำนาจบริหารคน; ส่วนมอบหมายงานใน handoff ใช้เฉพาะผู้มีอำนาจจริง

## เลือกตามสิ่งที่เกิดในงาน

| กลุ่มเสนอ | สถานการณ์ | Pilot card | สิ่งที่ฝึกให้ต่างกัน |
|---|---|---|---|
| เข้าใจและตัดสินใจ | ความคาดหวังยังไม่ชัด | [ทำความเข้าใจงาน](cards/GWS-clarify-work.md) | ถามช่องว่างและยืนยันความเข้าใจ |
| เข้าใจและตัดสินใจ | ข้อมูลหรือข้ออ้างขัดกัน | [ตรวจข้อมูล](cards/GWS-check-evidence.md) | ตรวจที่มา ขอบเขต และสิ่งที่ยังสรุปไม่ได้ |
| เข้าใจและตัดสินใจ | ต้องเลือกทางแม้ข้อมูลไม่ครบ | [เลือกการกระทำ](cards/GWS-choose-action.md) | เปรียบเทียบทางเลือกด้วยเกณฑ์และข้อจำกัด |
| สื่อสารและประสานงาน | เห็นต่างในประเด็นที่คุยได้ปลอดภัย | [คุยความเห็นต่าง](cards/GWS-work-through-disagreement.md) | เปิดประเด็น ฟัง และสรุปข้อตกลง |
| สื่อสารและประสานงาน | พึ่งคนต่างทีมโดยไม่มีอำนาจสั่ง | [ประสานข้ามขอบเขต](cards/GWS-coordinate-across-boundaries.md) | ขอความร่วมมือที่ต่อรองได้ |
| จัดการและปรับปรุงงาน | งานแย่งเวลาและทรัพยากร | [จัดลำดับงาน](cards/GWS-manage-priorities.md) | ระบุ tradeoff และขอปรับข้อตกลง |
| จัดการและปรับปรุงงาน | เปลี่ยนคนทำ/กะ/ทีม | [ส่งต่องาน](cards/GWS-handoff-and-follow-through.md) | ตรวจผู้รับ สถานะ และความรับผิดชอบ |
| จัดการและปรับปรุงงาน | ปัญหาคุณภาพหรือกระบวนการซ้ำ | [ทดลองปรับปรุง](cards/GWS-improve-with-small-experiments.md) | เปลี่ยนหนึ่งจุดอย่างได้รับสิทธิและเก็บผล |
| เรียนรู้และทำงานกับ AI | มี feedback หรือบทเรียนจากการลอง | [เรียนรู้และนำไปใช้](cards/GWS-learn-and-transfer.md) | ปรับการกระทำหนึ่งอย่างและลองต่างบริบท |
| เรียนรู้และทำงานกับ AI | ต้องตรวจชิ้นงานที่ AI ช่วย | [ตรวจงาน AI](cards/GWS-verify-ai-work.md) | ตรวจหลักฐานและคงเจ้าของการตัดสินใจ |

ตารางนี้เป็น compact situation index สำหรับอ่าน; [situation-index.json](situation-index.json) เก็บ ID, card ข้างเคียงและ coverage ของสถานการณ์ตั้งต้นทั้ง 8 ข้อ ยังไม่มี retrieval engine หรือ ranking algorithm ใน Phase 2

## หลักการใช้ชุดนำร่อง

เริ่มจากเหตุการณ์ ไม่เริ่มจากชื่อทักษะ ถ้าหลักฐานยังไม่พอใช้ **0 anchors** และขอข้อมูลเฉพาะที่จำเป็น หากจับคู่ได้ให้คง **0–3 anchors และหนึ่ง development edge** คำขอในอนาคต ความตั้งใจ ชื่อ framework และข้อเสนอการฝึกไม่ใช่หลักฐานว่าผู้ใช้เคยทำแล้ว

หนึ่ง anchor อาจรองรับเพียง fragment ของการกระทำ ต้องระบุสิ่งที่ยังไม่ยืนยัน ไม่สรุปว่าทำครบ card หรือมีความสามารถถาวร แยกสิ่งที่ผู้ใช้รายงานจาก artifact ที่ตรวจจริง และแยก episode evidence ออกจาก source provenance

การฝึกเป็นข้อเสนอที่ผู้ใช้เลือกและหยุดได้ ใช้กระดาษ บทสนทนา หรือเครื่องมือที่มีสิทธิได้ ไม่ต้องใช้ AI ทุกครั้ง จุดเน้นคือ learner attempt, feedback basis, สิ่งที่เปลี่ยนเมื่อย้ายบริบท และหลักฐานจากการลองครั้งถัดไป ไม่ให้คะแนนบุคคลหรือรับรองผลเรียนรู้

## ชั้นความรู้ที่แยกกัน

- **Cards:** การประยุกต์พฤติกรรมในสถานการณ์ โดยมี Harvard เป็นฐานรายละเอียดที่ตรวจแล้ว และ NZ เป็นส่วนเสริมตามขอบเขต
- **Coaching overlays:** [4 วิธีประกอบการโค้ช](coaching-methods/pilot-overlays.json) ใช้ Finland เป็นกระบวนการ และ McKinsey/van Gelder เป็นเลนส์ฝึก ไม่ใช้ประเมิน professionalism หรือระดับคน
- **iCD references:** เป็น related concepts/method pointers ใน cards ไม่ใช่ behavioral definitions; source refs ไม่รองรับกิจกรรมทั้งชุดโดยอัตโนมัติ
- **Foresight:** [คำถามตรวจการออกแบบ](foresight/pilot-design-lenses.json) เชื่อม WEF เพื่อ coverage และความเกี่ยวข้อง ไม่สร้าง skill gap ของผู้ใช้

JSON ของแต่ละ card เป็น canonical editorial data; Markdown เป็นฉบับอ่านที่สร้างจาก JSON รูปแบบข้อมูลนี้ยังไม่ใช่ shared runtime schema ซึ่งจะกำหนดใน Phase 3

## การรวมและสิ่งที่ยังไม่รวม

[proposed-taxonomy.json](proposed-taxonomy.json) บันทึกการรวมและการแยกพร้อมเหตุผล ส่วน [pilot-candidate-disposition.json](pilot-candidate-disposition.json) อธิบายสถานะครบ 93 candidates: ใช้ตามบทบาทใน pilot 55, ยังเลื่อนไว้หลัง pilot 26, คง exclude 6 และ hold 6

คำว่าใช้ใน pilot รวม behavior, pointer, overlay และ foresight ไม่ได้หมายถึง 55 ทักษะหรือการ import runtime ตัวอย่าง H-25 ถูกพิจารณาเป็นหัวข้อซ้ำกับ influence; card ใช้ H-04 เป็นหลักฐานโดยตรงและไม่ได้เพิ่ม H-25 เป็น source support ซ้ำอีก

ยังไม่สร้างชุด people management, talent assessment, specialty instruction หรือระดับ proficiency การ defer ไม่ใช่ตัดความรู้นั้นออกจากคลังถาวร ใช้ coverage gaps และสถานการณ์จริงเลือกสิ่งที่จะเพิ่มใน Phase 5

## การตรวจชุดนำร่อง

[Scenario fixtures](../../release/phase2/scenario-fixtures.json) มี 40 เรื่องเล่าสมมติ ครบ desk/frontline × contributor/manager สำหรับทุก card, 12 boundary cases และ 6 distinction reviews การจับคู่ที่คาดเป็น editorial tabletop review ไม่ใช่ผลที่ agent สร้างบน host จริง

อ่านผลและข้อจำกัดใน [Phase 2 report](../../release/phase2/PHASE_2_PILOT_REPORT.md) เฟสนี้ไม่เปลี่ยน runtime instruction, routing, schemas หรือ packages เดิม
