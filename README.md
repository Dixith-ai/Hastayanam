# Hastāyanam

Gesture-Based Human–Computer Interaction for Windows (Webcam + MediaPipe + OpenCV)

Hastāyanam lets you control your PC using hand gestures in real time. It supports a global mode switch (System, Media, Browser), left/right hand routing, clear on-screen HUD, and a detailed gesture guide.

## Highlights
- Real-time hand tracking with MediaPipe Hands
- 10+ gestures: Palm, Fist, Thumbs Up/Down, Two Fingers, Point Up/Down, Swipe Left/Right, Hold, Pinch
- Global Mode switch with pinch (🤏) hold for ~3s: System → Media → Browser
- Left/Right hand handling with optional handedness swap for mirrored webcams
- On-screen HUD: mode, gestures per hand, last action, confidence, cooldown, FPS, mode-switch progress
- Modular codebase; easy to extend actions and thresholds

## Quick Start (Windows)
```powershell
cd A:\py_prj\hand_recognition_ver_5
./run.ps1
```
Alternatively:
```powershell
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
If PowerShell blocks scripts:
```powershell
powershell -ExecutionPolicy Bypass -File .\run.ps1
```

## How to Use
- Ensure your webcam is connected and not used by other apps.
- Start the app. A window opens with your camera feed and HUD.
- Pinch (🤏) and hold for ~3s to cycle the global mode: System → Media → Browser. Watch the yellow progress bar.
- Perform the gestures shown in the guide for the active mode. Only actions from the current mode are executed.
- Press `q` to quit.

## Modes and Hand Roles
- Global Mode (pinch to switch): System ↔ Media ↔ Browser
- Either hand can perform gestures; only current mode actions run.
- The HUD shows each detected hand with a line like `Right: open_palm (0.95)` and `Left: swipe_right (0.92)`.
- Mirrored webcam? Toggle handedness in `hastayanam/config.py`: `VIDEO.swap_handedness = True`.

## Gesture Guide
See the full, constantly updated guide:
- `GESTURE_GUIDE.md` — how to perform gestures, actions per mode, HUD reference, and tuning tips.

Common examples (active mode required):
- System: Palm → Show Desktop; Point Up/Down → Volume Up/Down; Swipe Left/Right → Window switch; Fist (hold) → Sleep
- Media: Two Fingers → Play/Pause; Swipe Left/Right → Previous/Next; Palm → Start/Resume; Thumbs Up/Down → Volume
- Browser: Palm → New Tab; Fist → Close Tab; Swipe Left/Right → Tab switch; Palm (hold) → Private/Incognito

## Configuration
Tune thresholds and behavior in `hastayanam/config.py`:
- `THRESHOLDS.confidence_min` — minimum confidence to trigger
- `THRESHOLDS.stability_frames` — frames required for a stable pose
- `THRESHOLDS.gesture_cooldown_s` — default cooldown between repeats
- `THRESHOLDS.mode_switch_hold_s` — pinch hold time (default 3.0s)
- `THRESHOLDS.pinch_distance_threshold` — pinch sensitivity
- `THRESHOLDS.swipe_min_displacement_px` — swipe displacement
- `VIDEO.swap_handedness` — flip Left/Right labels if mirrored

## Tech Stack
- Python, OpenCV, MediaPipe Hands, NumPy
- Hotkeys via `pyautogui` (and system ops via Windows tools)

## Project Structure
```
hand_recognition_ver_5/
  app.py
  requirements.txt
  run.ps1
  run.bat
  README.md
  GESTURE_GUIDE.md
  LICENSE
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

## Troubleshooting
- Gestures fire too often: increase `confidence_min`, `stability_frames`, or cooldowns.
- Swipes unreliable: raise `swipe_min_displacement_px`.
- Labels reversed (Right/Left): set `VIDEO.swap_handedness = True`.
- Some apps ignore hotkeys: run as Administrator or share the app name for tailored mappings.

## License
MIT — see `LICENSE`.
