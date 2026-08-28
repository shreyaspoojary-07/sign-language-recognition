# Sign Language recognition
 
**Intern ID:** CITS8352
**NAME:** SHREYAS
**Number of Weeks:** 4
**Project Name:** Sign language Recognition

A real-time hand gesture recognition web app using **Google's pretrained MediaPipe
Gesture Recognizer** model. No data collection, no training — it works the moment
you download the model file.

## What it recognizes

Out of the box, the model detects:
- Closed Fist
- Open Palm
- Pointing Up
- Thumbs Up
- Thumbs Down
- Victory / Peace sign
- **ILoveYou** — the ASL "I Love You" handshape

## Project structure

```
sign-language-pretrained/
├── app.py               # Flask app - live webcam demo
├── download_model.py     # One-time download of the pretrained model
├── requirements.txt
├── models/
│   └── gesture_recognizer.task   # Downloaded, not written by hand
└── templates/
    └── index.html
```

## Important: Python version

MediaPipe only publishes wheels for **Python 3.9–3.12**. If your system Python is
3.13/3.14, create the virtual environment below using 3.10–3.12 specifically —
your system default doesn't need to change.

## Setup (VS Code)

1. **Open the folder in VS Code**: `File > Open Folder`.

2. **Create a virtual environment with Python 3.10–3.12**:
   ```bash
   # Windows
   py -3.12 -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3.12 -m venv venv
   source venv/bin/activate
   ```
   Then `Ctrl+Shift+P` → "Python: Select Interpreter" → pick the one inside `venv`.

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the pretrained model** (one-time, ~8MB):
   ```bash
   python download_model.py
   ```

5. **Run the app**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser. Show gestures to your webcam and
   watch the label update live.

## If the webcam doesn't open

`app.py` already uses `cv2.VideoCapture(0, cv2.CAP_DSHOW)` for better Windows
compatibility. If it still fails:
- Check Windows Settings > Privacy & security > Camera → allow desktop apps.
- Close any other app (Zoom, Teams, browser tabs) using the camera.
- Try changing the `0` in `cv2.VideoCapture(0, cv2.CAP_DSHOW)` to `1` if you have
  more than one camera.

## Deploying the code to GitHub

```bash
git init
git add .
git commit -m "Initial commit: pretrained gesture recognition app"
git branch -M main
git remote add origin https://github.com/<your-username>/sign-language-pretrained.git
git push -u origin main
```

The `.task` model file (~8MB) is small enough to commit directly, so it isn't
gitignored — this means anyone who clones your repo can run `app.py` immediately
after `pip install -r requirements.txt`, without a separate download step, as long
as you commit it after running `download_model.py` once locally.

Since this needs a live webcam, it runs locally rather than as a static GitHub
Pages site. For your portfolio, link the repo and add a short screen-recording
GIF to the README so recruiters can see it working without running it themselves.

## Extending this project
- Add custom gestures on top of this by training a *second* lightweight classifier
  using MediaPipe's raw hand landmarks (see the trainable version of this project),
  and fall back to the pretrained model for the built-in gestures.
- Map recognized gestures to actions (e.g., trigger a sound, control a slideshow,
  send a message) to turn this into a more interactive demo.
