import numpy as np
import jiwer
import whisper
import librosa
import parselmouth

model = whisper.load_model("base")


def transcribe_audio(audio_path):
    """
    ใช้โมเดล Whisper ถอดเสียงจากไฟล์เสียง
    """
    result = model.transcribe(audio_path, language="en")
    return result["text"].strip()


def compute_wer(reference, hypothesis):
    """
    คำนวณ Word Error Rate (WER)
    """
    return jiwer.wer(reference, hypothesis)


def compute_cer(reference, hypothesis):
    """
    คำนวณ Character Error Rate (CER)
    """
    return jiwer.cer(reference, hypothesis)


def get_duration(audio, sr):
    """
    คำนวณความยาวเสียงเป็นวินาที
    """
    return len(audio) / sr


def get_spectral_centroid(audio, sr):
    """
    คำนวณค่า spectral centroid เฉลี่ย
    ใช้ดูว่าเสียงโดยรวมทึบ/อู้อี้ลงไหม
    """
    centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)
    return float(np.mean(centroid))


def get_rms(audio):
    """
    คำนวณค่า RMS เฉลี่ยของสัญญาณ
    ใช้ดูพลังงานของเสียงโดยรวม
    """
    rms = librosa.feature.rms(y=audio)
    return float(np.mean(rms))


def get_peak(audio):
    """
    คำนวณ peak amplitude สูงสุด
    """
    return float(np.max(np.abs(audio)))


def count_pauses(audio, sr, silence_thresh=0.01, min_pause_ms=50):
    """
    นับจำนวนช่วง pause/silence แบบคร่าว ๆ

    silence_thresh: ค่าที่ต่ำกว่านี้ถือว่าเงียบ
    min_pause_ms: ต้องเงียบต่อเนื่องอย่างน้อยกี่ ms จึงนับเป็น 1 pause
    """
    abs_audio = np.abs(audio)
    silent = abs_audio < silence_thresh

    min_len = int(sr * min_pause_ms / 1000)

    pause_count = 0
    current_silence = 0

    for s in silent:
        if s:
            current_silence += 1
        else:
            if current_silence >= min_len:
                pause_count += 1
            current_silence = 0

    if current_silence >= min_len:
        pause_count += 1

    return pause_count


def get_f0_std(audio_path):
    """
    คำนวณส่วนเบี่ยงเบนมาตรฐานของ F0
    ใช้ดูว่า pitch variation แคบลงไหม
    """
    try:
        snd = parselmouth.Sound(audio_path)
        pitch = snd.to_pitch()
        f0_values = pitch.selected_array["frequency"]
        f0_values = f0_values[f0_values > 0]

        if len(f0_values) == 0:
            return 0.0

        return float(np.std(f0_values))

    except Exception:
        return 0.0
