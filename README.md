# Hastāyanam

Gesture-Based Human–Computer Interaction for Windows (Webcam + MediaPipe + OpenCV)

Hastāyanam lets you control your PC using hand movements in real time. It supports a global mode switch (System, Media, Browser), left/right hand handling, a clear on-screen HUD, and a detailed gesture guide.

## Highlights
- Real-time hand tracking with MediaPipe Hands
- Global mode switching across System, Media, and Browser
- Left/Right hand handling with optional handedness swap for mirrored webcams
- On-screen HUD: active mode, per-hand detection summary, last action, confidence, cooldown, FPS, mode-switch progress
- Modular codebase; easy to extend actions and thresholds

## Quick Start (Windows)
```powershell
# Clone or download this repo
# git clone https://github.com/Dixith-ai/Hastayanam.git
cd Hastayanam
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
- Use the mode-switch gesture to cycle the global mode (System → Media → Browser). See the gesture guide for details.
- Perform movements for the active mode only; actions from other modes won’t run.
- Press `q` to quit.

## Modes and Hand Handling
- A single global mode (System, Media, Browser) is active at a time.
- Either hand can be used; only the current mode’s actions will execute.
- The HUD shows each detected hand and the current mode.
- Mirrored webcam? Toggle handedness in `hastayanam/config.py`: `VIDEO.swap_handedness = True`.

## Gesture Guide
For all gestures and their actions per mode, see:
- `GESTURE_GUIDE.md`

## Configuration
Tune thresholds and behavior in `hastayanam/config.py`:
- `THRESHOLDS.confidence_min` — minimum confidence to trigger
- `THRESHOLDS.stability_frames` — frames required for a stable pose
- `THRESHOLDS.gesture_cooldown_s` — default cooldown between repeats
- `THRESHOLDS.mode_switch_hold_s` — hold time for switching modes
- `THRESHOLDS.pinch_distance_threshold` — pinch sensitivity
- `THRESHOLDS.swipe_min_displacement_px` — swipe displacement
- `VIDEO.swap_handedness` — flip Left/Right labels if mirrored

## Tech Stack
- Python, OpenCV, MediaPipe Hands, NumPy
- Hotkeys via `pyautogui` (and system ops via Windows tools)

## Project Structure
```
hand_recognition_ver_5/
  app.py                  # Entry point: camera loop, HUD, mode gating, action dispatch
  requirements.txt        # Python dependencies
  run.ps1 | run.bat       # Windows convenience scripts
  README.md               # This file
  GESTURE_GUIDE.md        # Detailed gesture reference
  LICENSE                 # MIT license

  hastayanam/             # Core package
    __init__.py
    config.py             # Tunable thresholds, video/overlay settings
    utils.py              # FPS meter, cooldowns, geometry helpers
    tracking.py           # MediaPipe Hands wrapper, draw helpers, handedness
    gestures.py           # Rule-based classifier (poses, swipes, holds, pinch)
    modes.py              # Global mode manager (System ↔ Media ↔ Browser)
    overlay.py            # HUD renderer (mode, per-hand, action, FPS, progress)

    actions_system.py     # Desktop actions (show desktop, volume, lock, etc.)
    actions_media.py      # Media/presentation actions (play/pause, next/prev, volume)
    actions_browser.py    # Browser actions (tabs, new/close, reload, nav)
```

## Troubleshooting
- Movements trigger too often: increase `confidence_min`, `stability_frames`, or cooldowns.
- Horizontal movements unreliable: raise `swipe_min_displacement_px`.
- Left/Right labels reversed: set `VIDEO.swap_handedness = True`.
- Some apps ignore hotkeys: run as Administrator or share the app name for tailored mappings.

## License
MIT — see `LICENSE`.
