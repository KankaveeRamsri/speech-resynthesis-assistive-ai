import os
import librosa
import soundfile as sf


def load_audio(audio_path, sr=16000):
    audio, sr = librosa.load(audio_path, sr=sr)
    return audio, sr


def save_audio(audio, sr, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    sf.write(output_path, audio, sr)


def make_output_filename(original_name, aug_type, param):
    base = os.path.splitext(original_name)[0]
    return f"{base}__{aug_type}_{param}.wav"
