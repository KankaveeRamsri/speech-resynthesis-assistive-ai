import numpy as np
import librosa
from scipy.signal import butter, lfilter


def apply_lowpass(audio, sr, cutoff):  # low-pass filter ตัดควาทถี่สูงออก เสียงอู้อี้มากขึ้น
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(4, normal_cutoff, btype="low", analog=False)
    return lfilter(b, a, audio)


def apply_timestretch(
    audio, rate
):  # ยืดหรือบีบเวลาโดยไม่เปลี่ยนความถี่ (เช่น ทำให้เสียงช้าลงหรือเร็วขึ้น)
    return librosa.effects.time_stretch(audio, rate=rate)


def apply_pitch_compression(
    audio, sr, factor
):  # ลด pitch ของเสียงให้ทุ้มลง (เช่น ทำให้เสียงเหมือนคนพูดที่มีเสียงทุ้มมากขึ้น)
    n_steps = (factor - 1.0) * 12
    return librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)


def apply_augmentation(
    audio, sr, aug_type, param
):  # ฟังก์ชันหลักที่เรียกใช้การเพิ่มเสียงตามประเภทและพารามิเตอร์ที่กำหนด
    if aug_type == "lowpass":
        return apply_lowpass(audio, sr, param)

    elif aug_type == "timestretch":
        return apply_timestretch(audio, param)

    elif aug_type == "pitch":
        return apply_pitch_compression(audio, sr, param)

    else:
        raise ValueError(f"Unknown augmentation type: {aug_type}")
