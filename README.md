# Hastāyanam – Gesture-Based Human–Computer Interaction System

Hastāyanam is a real-time hand-gesture control system for Windows. It uses a webcam, MediaPipe Hands, and OpenCV to detect gestures and map them to desktop, media/presentation, and browser actions. It provides an on-screen HUD with the active mode, detected gesture, action performed, confidence, and FPS.

## Features
- Real-time hand tracking with MediaPipe Hands
- 10+ gestures: Open Palm, Fist, Thumbs Up, Thumbs Down, Two Fingers, Point Up, Point Down, Swipe Left, Swipe Right, Hold Palm/Fist, etc.
- Three modes with dedicated actions:
  - System Control
  - Media Control (music, video players, and presentations)
  - Browser Control
- Gesture to switch modes (Pinch 🤏 hold)
- On-screen overlay with gesture, action, mode, confidence, and FPS

## Installation (Windows)
```powershell
# In PowerShell
cd A:\py_prj\hand_recognition_ver_5
./run.ps1
```
This script creates a virtual environment, installs dependencies, and launches the app.

Manual steps if preferred:
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Usage
- Ensure a webcam is connected.
- Run the app; a window with the camera feed and HUD will open.
- Perform gestures to trigger actions. Use 🤏 (pinch) held ~3s to cycle through modes.
- Press `q` in the window to quit, or use ✊ (Fist) depending on configuration.

## How It Works
- MediaPipe Hands detects hand landmarks (21 points).
- Landmarks are normalized and passed to a rule-based gesture classifier.
- The classifier detects static poses (e.g., Palm, Fist, Thumbs) and temporal motions (Swipes, Holds).
- A ModeManager tracks the active mode (System/Media/Browser).
- An action mapper executes the OS/browser/media actions using pyautogui and Windows shortcuts.
- The HUD renders the current mode, gesture, action, confidence, and FPS.

## Detailed Gesture Guide
See `GESTURE_GUIDE.md` for full instructions.

## Project Structure
```
hand_recognition_ver_5/
  app.py
  requirements.txt
  run.ps1
  README.md
  GESTURE_GUIDE.md
  hastayanam/
    __init__.py
    config.py
    utils.py
    tracking.py
    gestures.py
    modes.py
    overlay.py
    actions_system.py
    actions_media.py
    actions_browser.py
```

## Notes
- Media mode targets common controls for music players, video (including web video), and presentations. Play/Pause uses the Space key; Next/Prev uses Left/Right arrows which most slide/video players support.
- Some native music apps require dedicated media keys for Next/Prev Track; if your app ignores arrow keys, let us know which player so we can add enhanced support.
- Sensitivity and thresholds can be tuned in `hastayanam/config.py`.
- If volume control via pycaw is unavailable, the app falls back to keyboard volume keys.

## License
MIT
