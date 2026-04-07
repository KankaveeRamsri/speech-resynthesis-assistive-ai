import numpy as np
import librosa
from scipy.signal import butter, lfilter


def apply_lowpass(audio, sr, cutoff):
    """
    low-pass filter:
    ตัดความถี่สูงออก ทำให้เสียงอู้อี้ / พยัญชนะคมน้อยลง
    """
    nyquist = 0.5 * sr
    normal_cutoff = cutoff / nyquist
    b, a = butter(4, normal_cutoff, btype="low", analog=False)
    filtered = lfilter(b, a, audio)
    return filtered.astype(np.float32)


def apply_timestretch(audio, rate):
    """
    time-stretch:
    ยืดหรือบีบเวลาโดยไม่เปลี่ยน pitch
    rate < 1 = ช้าลง
    rate > 1 = เร็วขึ้น
    """
    stretched = librosa.effects.time_stretch(audio, rate=rate)
    return stretched.astype(np.float32)


def apply_pitch_compression(audio, sr, factor):
    """
    pitch compression แบบง่าย:
    factor < 1 ทำให้ pitch ต่ำลง / ฟังแบนขึ้นบางส่วน
    เช่น 0.90, 0.75, 0.60, 0.50

    หมายเหตุ:
    อันนี้จริง ๆ ยังเป็น pitch shift แบบง่าย
    ยังไม่ใช่ prosody compression ระดับ research-grade
    แค่ใช้ทดลอง phase แรก
    """
    n_steps = (factor - 1.0) * 12
    shifted = librosa.effects.pitch_shift(audio, sr=sr, n_steps=n_steps)
    shifted = np.clip(shifted, -1.0, 1.0)
    return shifted.astype(np.float32)


def apply_noise(audio, noise_level):
    """
    noise injection:
    เติม Gaussian noise เล็กน้อย
    ใช้จำลองความ rough / breathy แบบหยาบ ๆ
    """
    noise = np.random.randn(len(audio)).astype(np.float32)
    noisy = audio + noise_level * noise
    noisy = np.clip(noisy, -1.0, 1.0)
    return noisy.astype(np.float32)


def apply_pause_insertion(audio, sr, pause_prob, pause_ms_range, frame_ms=50):
    """
    pause insertion:
    แทรก silence เป็นช่วง ๆ แบบ frame-based

    pause_prob: ความน่าจะเป็นที่จะเพิ่ม pause หลังแต่ละ frame
    pause_ms_range: tuple เช่น (60, 120)
    frame_ms: ขนาด frame ที่ใช้เดินทีละช่วง
    """
    frame_len = int(sr * frame_ms / 1000)
    out = []

    i = 0
    while i < len(audio):
        chunk = audio[i : i + frame_len]
        out.append(chunk)

        if np.random.rand() < pause_prob:
            pause_ms = np.random.randint(pause_ms_range[0], pause_ms_range[1] + 1)
            pause_len = int(sr * pause_ms / 1000)
            pause = np.zeros(pause_len, dtype=np.float32)
            out.append(pause)

        i += frame_len

    augmented = np.concatenate(out)
    augmented = np.clip(augmented, -1.0, 1.0)
    return augmented.astype(np.float32)


def apply_augmentation(audio, sr, aug_type, param):
    """
    ฟังก์ชันหลักสำหรับเลือก augmentation ตามประเภท
    """
    if aug_type == "lowpass":
        return apply_lowpass(audio, sr, param)

    elif aug_type == "timestretch":
        return apply_timestretch(audio, param)

    elif aug_type == "pitch":
        return apply_pitch_compression(audio, sr, param)

    elif aug_type == "noise":
        return apply_noise(audio, param)

    elif aug_type == "pause":
        return apply_pause_insertion(
            audio,
            sr,
            pause_prob=param["pause_prob"],
            pause_ms_range=param["pause_ms_range"],
        )

    else:
        raise ValueError(f"Unknown augmentation type: {aug_type}")
