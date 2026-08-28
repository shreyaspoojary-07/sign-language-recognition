"""
app.py
------
Flask web app that streams your webcam and recognizes hand gestures
using Google's PRETRAINED MediaPipe Gesture Recognizer model.
No training or data collection needed.

Recognized gestures out of the box:
    Closed_Fist, Open_Palm, Pointing_Up, Thumb_Down, Thumb_Up,
    Victory, ILoveYou (the ASL "I Love You" sign)

Usage:
    python download_model.py   # one-time, downloads the model
    python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

import os
import cv2
import mediapipe as mp
from flask import Flask, render_template, Response

from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision

MODEL_PATH = os.path.join("models", "gesture_recognizer.task")

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_hands_connections = mp.solutions.hands.HAND_CONNECTIONS

# Human-friendly labels for the model's raw output categories
LABEL_MAP = {
    "Closed_Fist": "Fist",
    "Open_Palm": "Open Palm",
    "Pointing_Up": "Pointing Up",
    "Thumb_Down": "Thumbs Down",
    "Thumb_Up": "Thumbs Up",
    "Victory": "Victory / Peace",
    "ILoveYou": "I Love You (ASL)",
    "None": "No gesture",
}

recognizer = None
if os.path.exists(MODEL_PATH):
    base_options = mp_python.BaseOptions(model_asset_path=MODEL_PATH)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO,
        num_hands=2,
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)


def gen_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    timestamp_ms = 0

    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

        prediction_text = "Model not loaded — run download_model.py"

        if recognizer is not None:
            timestamp_ms += 33  # approx for ~30fps
            result = recognizer.recognize_for_video(mp_image, timestamp_ms)

            prediction_text = "No hand detected"
            if result.hand_landmarks:
                for hand_landmarks in result.hand_landmarks:
                    # Draw landmarks manually (task API returns normalized landmarks)
                    h, w, _ = frame.shape
                    points = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
                    for connection in mp_hands_connections:
                        start, end = connection
                        cv2.line(frame, points[start], points[end], (0, 255, 0), 2)
                    for point in points:
                        cv2.circle(frame, point, 3, (0, 0, 255), -1)

                if result.gestures:
                    top_gesture = result.gestures[0][0]
                    label = LABEL_MAP.get(top_gesture.category_name, top_gesture.category_name)
                    confidence = top_gesture.score
                    prediction_text = f"{label} ({confidence*100:.0f}%)"
                else:
                    prediction_text = "Hand detected, no gesture matched"

        cv2.putText(
            frame,
            prediction_text,
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 255, 0),
            2,
        )

        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        frame_bytes = buffer.tobytes()
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n")

    cap.release()


@app.route("/")
def index():
    return render_template("index.html", model_ready=recognizer is not None)


@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")


if __name__ == "__main__":
    app.run(debug=True)
