"""
download_model.py
------------------
Downloads Google's pretrained MediaPipe Gesture Recognizer model
(gesture_recognizer.task) into the models/ folder. Run this once
before app.py.

Usage:
    python download_model.py
"""

import os
import urllib.request

MODEL_URL = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "gesture_recognizer.task")


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at {MODEL_PATH}, skipping download.")
        return

    print(f"Downloading pretrained model from:\n{MODEL_URL}")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
