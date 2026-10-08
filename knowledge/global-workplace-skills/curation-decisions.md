---
status: phase-1-complete-with-bounded-holds
runtime_authority: false
reviewed_on: 2026-10-07
---

# บันทึกการคัดเลือกแหล่งอ้างอิง

คัด **93 รายการจาก 11 source records**: include 11, adapt 70, hold 6, exclude 6 รายการเหล่านี้เป็น topic/method/design candidates รวมถึงรายการที่ตัดออก ไม่ใช่ competency dictionary สำเร็จรูป ข้ออ้างและ locator รายรายการอยู่ใน [curation-candidates.json](curation-candidates.json)

## บทบาทที่ให้แต่ละแหล่ง

| แหล่ง | ขอบเขตที่ตรวจ | บทบาทใน Lumei |
|---|---|---|
| Harvard FY14 | 31 หัวข้อ หน้า 4–34 ของไฟล์ผู้ใช้; ตรวจชื่อหัวข้อกับเลขหน้า | Behavioral anchors; ลดภาษาเฉพาะองค์กรและหัวข้อซ้ำ |
| NZ LSP July 2016 | ภาพรวม 16 capabilities และ descriptors ที่เลือก; role context ที่เกี่ยวข้อง | แรงเสริมเรื่องทิศทาง ระบบ การส่งมอบและการเรียนรู้ โดยจำกัดตามอำนาจและบริบทผู้ใช้ |
| Finland Career Professionals 2024 proposal | 7 online descriptors ตาม code/URL | รูปแบบ coaching, agency, ethical boundaries และการเลือกเครื่องมือ |
| FiNQF | วัตถุประสงค์กรอบคุณวุฒิ | Context only; ตัด qualification levels ออกจากการประเมินผู้ใช้ |
| iCD V4 | S4 ทั้ง 12 labels และ 5 knowledge items ที่เลือก; แยก task matrices | Method pointers; ต้องมีคำอธิบายที่ตรวจแล้วจากแหล่งอื่นก่อนสอนรายละเอียด |
| WEF 2025 / WEF Maker 2026 | ส่วน skills outlook / physical work / learning pathways | Strategic foresight lens สำหรับคัดและทดสอบ coverage |
| McKinsey July 2026 | knowledge management, role design, practice, human coaching | Learning design lens พร้อมบันทึกจุดที่ Lumei เลือกปรับต่างจากบทความ |
| van Gelder draft 2003 / published 2005 | เปรียบเทียบรุ่น; ตรวจ 6-lesson abstract ฉบับตีพิมพ์ | Published conceptual lens; พัก rewards และ efficacy claims |

## การประยุกต์ที่มีผลต่อสถาปัตยกรรมความรู้

1. **ชื่อเดียวกันไม่ได้แปลว่าบทบาทเดียวกัน**: Finland ใช้ออกแบบกระบวนการช่วยผู้ใช้ ไม่ใช้เป็นมาตรฐานประเมินคนทำงานทุกอาชีพ; FiNQF เป็นกรอบคุณวุฒิคนละชุด แหล่งออนไลน์เรียกกรอบอาชีพนี้ว่า proposal ของสถาบันวิจัยการศึกษา ไม่อ้างว่าเป็นข้อบังคับพนักงานระดับชาติ ([project bibliography](https://peda.net/careerprof), [qualifications framework](https://www.oph.fi/en/education-and-qualifications/qualifications-frameworks))
2. **จำกัดภาระหน้าที่ตามบทบาท**: การบริหารคน จ้างงาน จัดสรรงบและ delegation ไม่ใช่สิ่งที่ทุกคนต้องทำ NZ มี role-complexity levels 1–10 ไม่ใช่ universal levels 1–5 และบาง capability ไม่เกี่ยวกับ non-management roles เก็บเป็น Lumei synthesis พร้อม scope เฉพาะ ไม่มี readiness/potential rating ([Expanded Guide](https://www.publicservice.govt.nz/assets/DirectoryFile/LSP_Expanded_guide_July_2016.pdf), PDF หน้า 7–9, 21–22)
3. **iCD label ไม่ใช่ behavioral definition**: S4 ในไฟล์ผู้ใช้มี Knowledge Item เป็น `-` ทุกแถว การตรวจ code ไม่อนุญาตให้เราแต่งพฤติกรรมแล้วอ้างว่า IPA กล่าวไว้ รายการ adapt เป็น cross-reference เท่านั้น; หากทำ card ต้องมีหลักฐานรายละเอียดจากแหล่งอื่น ([IPA download/version page](https://www.ipa.go.jp/en/it-talents/skill-standard/icd.html))
4. **Foresight ไม่ใช่หลักฐานส่วนบุคคล**: WEF ใช้ตรวจความเกี่ยวข้องและความหลากหลายของตัวอย่าง ไม่ใช้บอกว่าผู้ใช้ขาดทักษะเพราะ skill อยู่ในอันดับสูง WEF 2026 เน้น physical economy จึงช่วยเปิดมุมงานหน้างาน ไม่เปลี่ยน Lumei เป็นหลักสูตรวิชาชีพเฉพาะ (ไฟล์ผู้ใช้ WEF 2025 หน้า 34–44; WEF 2026 หน้า 3, 17, 20, 24–27)
5. **Human judgment อยู่กับผู้ใช้**: McKinsey มี AI grading ใน answer-key model; Lumei เลือกปรับเป็นลองเอง–เปรียบเทียบ–ตรวจหลักฐานแบบสมัครใจ โดยไม่ถือ AI เป็นเฉลยหรือผู้ให้คะแนน (ไฟล์ผู้ใช้ McKinsey หน้า 5–6)
6. **แยกแนวคิดออกจากผลลัพธ์ที่พิสูจน์แล้ว**: van Gelder ฉบับตีพิมพ์ตรวจได้ระดับ abstract และมี 6 บทเรียน ใช้เสนอวิธีฝึกเชิงแนวคิดได้ แต่รายละเอียด body ยังไม่ครบและยังไม่มี contemporary efficacy review สำหรับการอ้างผลของ Lumei ร่าง 2003 มี 7 บทเรียนและขอไม่ให้ quote/cite จึงไม่ใช้ร่างแทนฉบับตีพิมพ์ ([published article copy](https://www.aku.edu/qtl/resources/Documents/Teaching%20Critical%20Thinking%20Some%20Lessons%20From%20Cognitive%20Science.pdf), PDF หน้า 2 / journal หน้า 41; DOI 10.3200/CTCH.53.1.41-48)

## การรวมและขอบเขตที่ส่งต่อ Phase 2

- Applied Learning / Continuous Learning / Finland A3.2 อาจเป็นหนึ่งชุด learning-in-action; เก็บ source roles แยกกัน
- Ability to Influence / Persuasiveness / NZ-02 อาจรวมเป็น ethical influence โดยไม่ใช้ pressure/reward เป็นตัวชี้วัด
- Planning and Organizing / Time Management / NZ-11 อาจรวมเป็น priorities and commitments
- Teamwork / Partnerships / system dependencies ต้องแยกจาก people management ที่ต้องมี authority
- Decision Making / Problem Analysis / NZ-13 / iCD hypothesis labels เสริมกันได้ แต่ต้องไม่หลอม claim ของคนละแหล่งให้กลายเป็นคำกล่าวร่วม
- Practice / transfer / argument structure เป็น coaching-method overlay ไม่ต้องบังคับแสดงทุกครั้งที่ mapping skill

ชื่อชุดข้างบนเป็นข้อเสนอการรวม ไม่ใช่ taxonomy ที่อนุมัติแล้ว สำหรับ pilot ให้ตรวจทั้ง knowledge work, service/frontline, physical work, งานข้ามทีม และผู้ไม่มีอำนาจสั่งการ เลือก 0–3 anchors ตามหลักฐาน และหนึ่ง development edge; narrative evidence กับ knowledge provenance ต้องแยกกัน

## Hold ที่ไม่ขวางรายการอื่น

| Candidate ID | เหตุผล | สิ่งที่ต้องได้ก่อนใช้ |
|---|---|---|
| ICD-S410020020 | คำแปล deep-plowing คลุมเครือ ไม่มี definition | คำอธิบายต้นฉบับที่ตรวจได้และความหมายในบริบท |
| ICD-S410020030 | continue ไม่มีขอบเขตพฤติกรรม | นิยามที่แยก persistence ออกจากการฝืนข้อจำกัด/ความปลอดภัย |
| ICD-S410030030 | evoke sympathy เสี่ยงตีความเป็น manipulation | definition และกรอบการใช้อย่างเคารพ agency |
| ICD-M-2246 | ภาษา risk-response item แปลคลุมเครือ | terminology ต้นฉบับหรือ primary method source ที่ตรวจแยกแล้ว |
| VG-DRAFT-REWARDS | มีในร่าง ไม่อยู่ใน six-lesson synopsis | แหล่งตีพิมพ์แยก หากต้องใช้; มิฉะนั้นละไว้ |
| VG-EFFICACY | แนวคิดเชิงประวัติศาสตร์ไม่พิสูจน์ผลของ Lumei | contemporary primary studies พร้อมข้อจำกัด ก่อนกล่าวอ้างประสิทธิผล |

## สิทธิและการเก็บข้อมูล

NZ เว็บไซต์ระบุ default CC BY 4.0 โดยมีข้อยกเว้นและต้อง attribution; registry เก็บ URL เงื่อนไขไว้ การประยุกต์ของ Lumei ไม่ใช่การรับรองจากรัฐบาล ([terms](https://www.publicservice.govt.nz/terms-and-conditions-copyright)) Finland online pages ใช้ Peda.net general licence ซึ่งคำอธิบายระบุลักษณะ all rights reserved ยกเว้นการดำเนินงานแพลตฟอร์ม ([licence explanation](https://peda.net/info/lisenssit))

สำหรับ Harvard, iCD, WEF, McKinsey และ van Gelder ยังไม่ยืนยันสิทธิเผยแพร่ต้นฉบับ/คำแปลทั้งชุด การคัดเลือกนี้จึงบันทึก concise original synthesis, identifiers และ locators ไม่ทำ bulk source ingestion สิทธิที่ยังไม่ชัดไม่ทำให้ factual review เป็น verified permission หากอนาคตต้องนำข้อความ ตาราง ภาพ หรือคำแปลใกล้ต้นฉบับเข้า package ต้องตรวจสิทธิของ item/use นั้นก่อน

## ข้อจำกัดของการตรวจครั้งนี้

ตรวจเฉพาะ candidate ที่บันทึก ไม่ได้ตรวจทุก item ของทุก framework: Finland หมวดอื่นรวมถึง C/systemic descriptors ยังไม่ cleared; iCD ไม่ได้ตรวจ ~10,000 knowledge items หรือ standards ที่ถูกเอ่ยชื่อ; van Gelder detailed body ยังต้องตรวจเมื่อใช้เกิน abstract-level concept; ยังไม่เลือก deployment host

Source registry เก็บ SHA-256 ของ 9 local files เพื่อ pin รุ่น ไม่อ้างว่า local hash เท่ากับ remote download หากไม่มี byte comparison ออนไลน์เก็บ dated URL/locator และขอบเขตที่อ่าน ไม่เก็บ full webpage cache; ตัว validator ตรวจโครงสร้าง/ไฟล์ในเครื่อง ไม่ re-fetch เว็บหรือพิสูจน์คุณภาพทางวิชาการ
