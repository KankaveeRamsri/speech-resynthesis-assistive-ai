import os
import pandas as pd
from tqdm import tqdm

from config import SAMPLE_RATE, AUGMENTATIONS
from utils import load_audio, save_audio, make_output_filename
from augment import apply_augmentation
from evaluate import (
    transcribe_audio,
    compute_wer,
    compute_cer,
    get_duration,
    get_spectral_centroid,
    get_rms,
    get_peak,
    count_pauses,
    get_f0_std,
)

RAW_DIR = "../data/raw"
OUTPUT_DIR = "../data/augmented"
TRANSCRIPT_PATH = "../data/transcripts/transcripts.csv"
RESULT_DIR = "../results"
RESULT_PATH = os.path.join(RESULT_DIR, "metrics.csv")

results = []

metadata = pd.read_csv(TRANSCRIPT_PATH)

total_tasks = len(metadata) * sum(len(params) for params in AUGMENTATIONS.values())

os.makedirs(RESULT_DIR, exist_ok=True)

with tqdm(total=total_tasks, desc="Running augmentations", unit="aug") as pbar:
    for _, row in metadata.iterrows():
        filename = row["filename"]
        reference_text = row["text"]

        audio_path = os.path.join(RAW_DIR, filename)
        audio, sr = load_audio(audio_path, sr=SAMPLE_RATE)

        # ===== baseline metrics =====
        duration_before = get_duration(audio, sr)
        spectral_centroid_before = get_spectral_centroid(audio, sr)
        rms_before = get_rms(audio)
        peak_before = get_peak(audio)
        pause_count_before = count_pauses(audio, sr)
        f0_std_before = get_f0_std(audio_path)

        for aug_type, param_list in AUGMENTATIONS.items():
            for param in param_list:
                augmented_audio = apply_augmentation(audio, sr, aug_type, param)

                output_filename = make_output_filename(filename, aug_type, param)
                output_folder = os.path.join(OUTPUT_DIR, aug_type)
                output_path = os.path.join(output_folder, output_filename)

                save_audio(augmented_audio, sr, output_path)

                predicted_text = transcribe_audio(output_path)

                wer_score = compute_wer(reference_text, predicted_text)
                cer_score = compute_cer(reference_text, predicted_text)

                # ===== augmented metrics =====
                duration_after = get_duration(augmented_audio, sr)
                spectral_centroid_after = get_spectral_centroid(augmented_audio, sr)
                rms_after = get_rms(augmented_audio)
                peak_after = get_peak(augmented_audio)
                pause_count_after = count_pauses(augmented_audio, sr)
                f0_std_after = get_f0_std(output_path)

                results.append(
                    {
                        "filename": filename,
                        "aug_type": aug_type,
                        "param": str(param),
                        "output_path": output_path,
                        "reference": reference_text,
                        "prediction": predicted_text,
                        "wer": wer_score,
                        "cer": cer_score,
                        "duration_before": duration_before,
                        "duration_after": duration_after,
                        "duration_increase": duration_after - duration_before,
                        "spectral_centroid_before": spectral_centroid_before,
                        "spectral_centroid_after": spectral_centroid_after,
                        "spectral_centroid_diff": spectral_centroid_after
                        - spectral_centroid_before,
                        "rms_before": rms_before,
                        "rms_after": rms_after,
                        "rms_diff": rms_after - rms_before,
                        "peak_before": peak_before,
                        "peak_after": peak_after,
                        "peak_diff": peak_after - peak_before,
                        "pause_count_before": pause_count_before,
                        "pause_count_after": pause_count_after,
                        "pause_count_diff": pause_count_after - pause_count_before,
                        "f0_std_before": f0_std_before,
                        "f0_std_after": f0_std_after,
                        "f0_std_diff": f0_std_after - f0_std_before,
                    }
                )

                pbar.update(1)
                pbar.set_postfix(file=filename, aug=aug_type, param=str(param))

results_df = pd.DataFrame(results)
results_df.to_csv(RESULT_PATH, index=False)

print(f"Finished experiment. Results saved to: {RESULT_PATH}")
