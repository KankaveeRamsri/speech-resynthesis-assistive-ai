import jiwer
import whisper

model = whisper.load_model("base")


def transcribe_audio(audio_path):  # ใช้โมเดล Whisper ในการถอดเสียงจากไฟล์เสียงที่กำหนด
    result = model.transcribe(audio_path)
    return result["text"].strip()


def compute_wer(
    reference, hypothesis
):  # ใช้ jiwer ในการคำนวณ Word Error Rate (WER) ว่าคำผิดไปกี่เปอร์เซ็นต์เมื่อเทียบกับข้อความอ้างอิง
    return jiwer.wer(reference, hypothesis)


def compute_cer(
    reference, hypothesis
):  # ใช้ jiwer ในการคำนวณ Character Error Rate (CER) ว่าตัวอักษรผิดไปกี่เปอร์เซ็นต์เมื่อเทียบกับข้อความอ้างอิง
    return jiwer.cer(reference, hypothesis)
