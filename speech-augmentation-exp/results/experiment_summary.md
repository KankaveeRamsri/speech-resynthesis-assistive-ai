# สรุปผลการทดลอง Augmentation เสียง

| Augmentation      | Parameter          | ลักษณะเสียงที่เปลี่ยนไป                 | ผลกระทบต่อ Whisper              | ระดับความรุนแรง |
| ----------------- | ------------------ | --------------------------------------- | ------------------------------- | --------------- |
| Low-pass Filter   | 5000 Hz            | เสียงอู้นิดหน่อย เสียงสูงหายเล็กน้อย    | WER/CER เพิ่มเล็กน้อยมาก        | 🟢 ต่ำ          |
| Low-pass Filter   | 4000 Hz            | เสียงอู้มากขึ้น พยัญชนะเริ่มไม่คม       | WER/CER เพิ่มเล็กน้อย           | 🟢 ต่ำ          |
| Low-pass Filter   | 3000 Hz            | เสียงทึบ อู้ และพยัญชนะไม่ชัดขึ้น       | WER/CER เพิ่มเล็กน้อยถึงปานกลาง | 🟡 ต่ำ-ปานกลาง  |
| Low-pass Filter   | 2500 Hz            | เสียงอู้มาก คล้ายพูดไม่ชัดหรืออมอะไรไว้ | WER/CER เพิ่มปานกลาง            | 🟠 ปานกลาง      |
| Time Stretch      | 0.98               | ความเร็วเปลี่ยนเล็กน้อย                 | แทบไม่มีผล                      | 🟢 ต่ำ          |
| Time Stretch      | 0.95               | พูดช้าลงเล็กน้อย จังหวะเปลี่ยนชัดขึ้น   | WER/CER เพิ่มปานกลาง            | 🟡 ปานกลาง      |
| Time Stretch      | 0.92               | พูดช้าลงชัดเจน เริ่มฟังผิดธรรมชาติ      | WER/CER เพิ่มค่อนข้างมาก        | 🟠 ปานกลาง-สูง  |
| Time Stretch      | 0.88               | พูดช้ามาก คล้าย slow motion             | WER/CER เพิ่มมาก                | 🔴 สูง          |
| Pitch Compression | 0.90               | เสียงต่ำลงเล็กน้อย                      | WER/CER เพิ่มปานกลาง            | 🟡 ปานกลาง      |
| Pitch Compression | 0.75               | เสียงต่ำและเพี้ยนชัดเจน                 | WER/CER เพิ่มมาก                | 🔴 สูง          |
| Pitch Compression | 0.60               | เสียงผิดธรรมชาติและ monotone มากขึ้น    | WER/CER เพิ่มมากมาก             | 🔴 สูงมาก       |
| Pitch Compression | 0.50               | เสียงเพี้ยนมาก ฟังคล้าย effect          | WER/CER เพิ่มมากที่สุด          | 🔴 สูงมาก       |
| Noise Injection   | 0.001              | มี noise เล็กน้อยแทบไม่รู้สึก           | แทบไม่มีผล                      | 🟢 ต่ำ          |
| Noise Injection   | 0.003              | เสียงหยาบขึ้นเล็กน้อย                   | WER/CER เพิ่มเล็กน้อย           | 🟢 ต่ำ          |
| Noise Injection   | 0.005              | เสียง rough และ breathy ขึ้น            | WER/CER เพิ่มเล็กน้อยถึงปานกลาง | 🟡 ต่ำ-ปานกลาง  |
| Noise Injection   | 0.008              | เสียง noisy ชัดเจน เริ่มคล้ายไมค์เสีย   | WER/CER เพิ่มปานกลาง            | 🟠 ปานกลาง      |
| Pause Insertion   | p=0.05, 60–120 ms  | มีการหยุดเว้นเล็กน้อย ฟัง hesitant ขึ้น | WER/CER เพิ่มเล็กน้อย           | 🟢 ต่ำ          |
| Pause Insertion   | p=0.10, 100–200 ms | มี pause มากขึ้น ฟังติดขัดขึ้น          | WER/CER เพิ่มปานกลาง            | 🟡 ปานกลาง      |
| Pause Insertion   | p=0.15, 150–300 ms | เว้นจังหวะบ่อย ฟังขาดตอน                | WER/CER เพิ่มมาก                | 🔴 สูง          |
| Pause Insertion   | p=0.20, 150–300 ms | เว้นจังหวะถี่มาก ฟังเหมือนเสียงตัดต่อ   | WER/CER เพิ่มมากมาก             | 🔴 สูงมาก       |

---

## ข้อสังเกตสำคัญ

- Low-pass Filter เป็น augmentation ที่กระทบ Whisper น้อยที่สุด
- Low-pass ที่ 3000–2500 Hz เริ่มให้ความรู้สึกเหมือนพูดไม่ชัดจริง
- Time Stretch ส่งผลระดับปานกลาง โดยเฉพาะเมื่อค่า rate ต่ำกว่า 0.95
- Pitch Compression เป็น augmentation ที่ส่งผลต่อ Whisper มากที่สุด
- Pitch Compression ที่ 0.60 และ 0.50 ให้ค่า WER/CER สูงมาก แต่เริ่มฟังผิดธรรมชาติ
- Noise Injection กระทบ ASR น้อยกว่าที่คาด และบางระดับยังไม่สะท้อน dysarthria-like speech ชัดเจน
- Pause Insertion เป็น augmentation ที่ส่งผลต่อ fluency และ duration ชัดเจนมาก
- Pause Insertion ที่รุนแรงเกินไปจะทำให้เสียงเหมือนถูกตัดต่อมากกว่าพูดติดขัดจริง
- Parameter ที่ดูสมดุลและเหมาะสมที่สุดสำหรับการนำไปใช้ต่อ ได้แก่:
  - Low-pass: 3000 Hz, 2500 Hz
  - Time Stretch: 0.95, 0.92
  - Pitch Compression: 0.90, 0.75
  - Noise Injection: 0.003, 0.005
  - Pause Insertion: p=0.05 / 60–120 ms และ p=0.10 / 100–200 ms

---

## เรียงลำดับจากกระทบน้อย → กระทบมาก

1. Low-pass 5000 Hz
2. Low-pass 4000 Hz
3. Noise 0.001
4. Time Stretch 0.98
5. Noise 0.003
6. Pause Insertion p=0.05, 60–120 ms
7. Low-pass 3000 Hz
8. Time Stretch 0.95
9. Pitch Compression 0.90
10. Noise 0.005
11. Pause Insertion p=0.10, 100–200 ms
12. Low-pass 2500 Hz
13. Time Stretch 0.92
14. Noise 0.008
15. Pitch Compression 0.75
16. Pause Insertion p=0.15, 150–300 ms
17. Time Stretch 0.88
18. Pitch Compression 0.60
19. Pause Insertion p=0.20, 150–300 ms
20. Pitch Compression 0.50
