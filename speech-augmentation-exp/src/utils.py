import os
import librosa
import soundfile as sf


def load_audio(audio_path, sr=16000):
    audio, sr = librosa.load(audio_path, sr=sr)
    return audio, sr


def save_audio(audio, sr, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, audio, sr)


def format_param_for_filename(param):
    """
    แปลง param ให้เหมาะกับการเอาไปใส่ชื่อไฟล์
    """
    if isinstance(param, dict):
        pause_prob = str(param["pause_prob"]).replace(".", "_")
        pause_range = param["pause_ms_range"]
        return f"p{pause_prob}_d{pause_range[0]}-{pause_range[1]}"

    elif isinstance(param, float):
        return str(param).replace(".", "_")

    else:
        return str(param)


def make_output_filename(original_name, aug_type, param):
    base = os.path.splitext(original_name)[0]
    param_str = format_param_for_filename(param)
    return f"{base}__{aug_type}_{param_str}.wav"
