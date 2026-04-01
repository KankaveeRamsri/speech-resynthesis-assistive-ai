import os
import pandas as pd

from config import SAMPLE_RATE, AUGMENTATIONS
from utils import load_audio, save_audio, make_output_filename
from augment import apply_augmentation
from evaluate import transcribe_audio, compute_wer, compute_cer

RAW_DIR = "../data/raw"
OUTPUT_DIR = "../data/augmented"
TRANSCRIPT_PATH = "../data/transcripts/transcripts.csv"

results = []

metadata = pd.read_csv(TRANSCRIPT_PATH)

for _, row in metadata.iterrows():
    filename = row["filename"]
    reference_text = row["text"]

    audio_path = os.path.join(RAW_DIR, filename)

    audio, sr = load_audio(audio_path, sr=SAMPLE_RATE)

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

            results.append(
                {
                    "filename": filename,
                    "aug_type": aug_type,
                    "param": param,
                    "output_path": output_path,
                    "reference": reference_text,
                    "prediction": predicted_text,
                    "wer": wer_score,
                    "cer": cer_score,
                }
            )

results_df = pd.DataFrame(results)
results_df.to_csv("../results/metrics.csv", index=False)

print("Finished experiment.")
