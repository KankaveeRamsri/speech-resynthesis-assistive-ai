SAMPLE_RATE = 16000

AUGMENTATIONS = {
    "lowpass": [5000, 4000, 3000, 2500],
    "timestretch": [0.98, 0.95, 0.92, 0.88],
    "pitch_compression": [0.90, 0.75, 0.60, 0.50],
    "noise": [0.001, 0.003, 0.005, 0.008],
    "pause_insertion": [
        {"pause_prob": 0.05, "pause_ms": (60, 120)},
        {"pause_prob": 0.10, "pause_ms": (100, 200)},
        {"pause_prob": 0.15, "pause_ms": (150, 300)},
        {"pause_prob": 0.20, "pause_ms": (150, 300)},
    ],
}
