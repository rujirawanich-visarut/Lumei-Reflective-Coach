# ปรับปรุงงานด้วยการทดลองขนาดเล็ก

Improve through small experiments · `GWS-improve-with-small-experiments` · release candidate 0.2.0 · runtime_authority: false

## ใช้เมื่อ

พบปัญหาคุณภาพหรือขั้นตอนซ้ำ และมีพื้นที่ทดลองที่ปลอดภัยในขอบเขตอำนาจ

## พฤติกรรมและหลักฐาน

- **A1** ระบุปัญหาจากเหตุการณ์และสภาพตั้งต้น รวมทั้งข้อจำกัดที่ต้องรักษา (H-27, H-07)
- **A2** เสนอการเปลี่ยนหนึ่งอย่างที่ตรวจได้ และกำหนดว่าจะสังเกตอะไรพร้อมเงื่อนไขหยุด (H-18, H-30)
- **A3** ลองเมื่อได้รับสิทธิและทบทวนผลที่สังเกต โดยไม่สรุปว่าการเปลี่ยนเป็นสาเหตุเดียว (H-28, H-30)

หลักฐานที่มองหา: สภาพตั้งต้นและปัญหาที่ระบุได้ / การเปลี่ยนที่ได้รับสิทธิและเงื่อนไขทดลอง / ผลที่สังเกตและปัจจัยอื่นที่อาจเกี่ยวข้อง

## ขอบเขตและข้อจำกัด

- ใช้เฉพาะงานและข้อมูลที่ผู้ใช้มีสิทธิ
- ไม่แทนขั้นตอนองค์กรหรือความรู้เฉพาะวิชาชีพ
- เหตุการณ์คุกคาม ความปลอดภัยหรือความเสี่ยงสูงต้องใช้ช่องทางที่เหมาะสมก่อนกิจกรรมฝึก
- ผลดีหลังทดลองไม่พิสูจน์สาเหตุโดยตัวมันเอง
- การปรับปรุงไม่อนุญาตให้ข้าม SOP safety หรือ change approval
- ข้อเสนอการฝึกไม่ใช่หลักฐานว่าผู้ใช้เคยทำหรือทำได้แล้ว
- ไม่ให้คะแนน ระดับ proficiency หรือคำตัดสินตัวตนจากเหตุการณ์

## กิจกรรมฝึกที่เลือกได้

ร่างต้นแบบหรือการเปลี่ยนขั้นตอนหนึ่งจุดในสถานการณ์สมมติ ระบุผลที่คาด สิ่งที่จะดูและเงื่อนไขหยุด

**Feedback:** การเปลี่ยนเล็กพอจะตรวจและย้อนกลับได้หรือไม่; มีข้อมูลตั้งต้นและอธิบายปัจจัยอื่นหรือไม่

**ลองต่างบริบท:** เปลี่ยนจากตรวจแบบฟอร์มเป็นติดตามข้อผิดพลาดใน handoff ระบุว่าต้องเปลี่ยนวิธีสังเกตอะไร

**หลักฐานถัดไป:** สภาพตั้งต้นและปัญหาที่ระบุได้ / ผลที่สังเกตและปัจจัยอื่นที่อาจเกี่ยวข้อง

**ขอบเขต AI:** AI ช่วยจัดโครงหรือชี้ข้อมูลที่ยังขาดได้ ผู้ใช้เป็นเจ้าของเหตุผลและปฏิเสธกิจกรรมได้; ไม่ grading

**หยุดเมื่อ:** ผู้ใช้ไม่ต้องการฝึก / งานเกินสิทธิหรือเสี่ยงกระทบคน/ระบบจริง / ต้องมีผู้รับผิดชอบเฉพาะทางแต่ยังไม่พร้อม

## ความต่างจาก card ใกล้เคียง

learning เปลี่ยนการกระทำผู้เรียนจาก feedback; improvement ทดลองเปลี่ยนกระบวนการและคุณภาพงาน; 

## Provenance

เลือกส่วนที่ใช้ข้ามงานได้จาก candidate ที่ตรวจแล้ว; ข้อความไทย พฤติกรรมเชิงปฏิบัติและกิจกรรมเป็นการประยุกต์ของ Lumei ไม่ใช่คำแปลรับรองหรือมาตรฐานสากล

- `H-27` / `HARVARD-FY14` — behavior_support; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
- `H-07` / `HARVARD-FY14` — behavior_support; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
- `H-18` / `HARVARD-FY14` — behavior_support; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
- `H-30` / `HARVARD-FY14` — behavior_support; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
- `H-28` / `HARVARD-FY14` — behavior_support; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
- `ICD-M-3586` / `ICD-V4-SKILL` — related_concept_only; locator/version/claim ใน [GWS-improve-with-small-experiments.json](GWS-improve-with-small-experiments.json)
