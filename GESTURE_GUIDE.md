# Hastāyanam – Detailed Gesture Guide

This guide explains how to perform gestures reliably, what each gesture does in every mode, and tips for best accuracy. Use a thumb–index pinch (🤏) held for ~3 seconds with your right hand to switch between System and Media modes (watch the yellow progress bar on the HUD). The left hand controls Browser actions.

## General Tips for Reliable Detection
- Ensure your hand is fully in frame with good lighting and a simple background.
- Hold a clear pose for a brief moment; avoid mid-air transitions that resemble other gestures.
- Keep the wrist relatively steady unless performing a swipe; swipes should be deliberate.
- If the HUD shows low confidence or “Cooling down…”, hold steady or wait a moment before repeating.
- You can tune sensitivity in `hastayanam/config.py` (see “Tuning & Settings”).

## Hand Roles (Left vs Right)
- Right Hand: Controls System and Media. Pinch (🤏) and hold ~3s to toggle between System ↔ Media.
- Left Hand: Controls Browser only.
- HUD shows per-hand detections (e.g., “Right: open_palm (0.95)”, “Left: swipe_right (0.90)”). Make sure the intended hand performs the desired action.

## Mode Switching (Right Hand)
- Gesture: 🤏 Pinch (thumb and index fingertips touching) held for ~3 seconds
- HUD: Yellow progress bar fills during the hold; mode cycles between System and Media for the right-hand control path.
- Order (Right Hand): System ↔ Media (toggle)
- Browser mode is not affected by the pinch; it is always controlled by the left hand.

## Gesture Catalog
The system recognizes a mixture of static poses and temporal gestures (movement- or time-based).

### Static Poses
- ✋ Open Palm
  - How to perform: Extend all fingers straight; show the full palm to the camera.
  - Stability tip: Keep palm facing camera; avoid bending fingers.

- ✊ Fist
  - How to perform: Curl all fingers into the palm; thumb wrapped.
  - Stability tip: Keep wrist steady; avoid partial open hand.

- 👍 Thumbs Up
  - How to perform: Extend thumb upward; curl other fingers.
  - Stability tip: Keep thumb clearly higher than wrist; avoid rotating sideways too much.

- 👎 Thumbs Down
  - How to perform: Extend thumb downward; curl other fingers.
  - Stability tip: Thumb should be clearly below the wrist vertically.

- 🤏 Pinch (thumb + index touching)
  - How to perform: Bring the thumb and index fingertips together; other fingers can be relaxed.
  - Stability tip: Keep the pinch tight and steady for switching modes (right hand).

- ✌️ Two Fingers
  - How to perform: Extend index and middle fingers; curl other fingers and thumb.
  - Stability tip: Keep the two fingers clearly separated.

- 👆 Point Up
  - How to perform: Extend index finger up; keep other fingers curled.
  - Stability tip: Ensure index fingertip above the wrist level.

- 👇 Point Down
  - How to perform: Extend index finger down; keep other fingers curled.
  - Stability tip: Ensure index fingertip below the wrist level.

### Temporal Gestures
- 👉 Swipe Right
  - How to perform: With an open palm or neutral hand, move the wrist horizontally to the right across the frame.
  - Stability tip: Make a quick, clear rightward motion; avoid diagonal motion.

- 👈 Swipe Left
  - How to perform: With an open palm or neutral hand, move the wrist horizontally to the left across the frame.
  - Stability tip: Make a quick, clear leftward motion; avoid diagonal motion.

- 🕒 Hold (Fist or Palm)
  - How to perform: Keep the pose steady for ~2 seconds.
  - Stability tip: Watch HUD for confidence; don’t jiggle your hand during the hold.

## Actions by Hand

### Right Hand → System Control
- ✋ Open Palm → Show Desktop
- 👆 Point Up → Volume Up (repeated while pose holds, with cooldown)
- 👇 Point Down → Volume Down (repeated while pose holds, with cooldown)
- 👉 Swipe Right → Next Window (Alt+Tab)
- 👈 Swipe Left → Previous Window (Alt+Shift+Tab)
- ✊ Fist → Lock Screen; if held ~2s → Sleep (Hibernate)
- 👍 Thumbs Up → Confirm / Enter

### Right Hand → Media Control (music, video, slides)
- 🤏 Pinch (hold ~3s) → Toggle System ↔ Media (right-hand path)
- 👉 Swipe Right → Next Slide / Next Video / Next Track
- 👈 Swipe Left → Previous Slide / Previous Video / Previous Track
- ✋ Open Palm → Start / Resume Presentation or Video (F5 if supported)
- ✊ Fist → Pause (Space)
- ✌️ Two Fingers → Play / Pause (Space)
- 👍 Thumbs Up → Volume Up
- 👎 Thumbs Down → Volume Down

Notes:
- Play/Pause uses the Space key; most video sites and slide decks support this.
- Next/Prev use Right/Left arrows; for some music apps, you may need media keys.

### Left Hand → Browser Control
- 👉 Swipe Right → Next Tab (Ctrl+Tab)
- 👈 Swipe Left → Previous Tab (Ctrl+Shift+Tab)
- ✋ Open Palm → New Tab (Ctrl+T)
- ✊ Fist → Close Tab (Ctrl+W)
- 👍 Thumbs Up → Reload Page (Ctrl+R)
- 👎 Thumbs Down → Go Back (Alt+Left)
- ✌️ Two Fingers → Go Forward (Alt+Right)
- ✋ Open Palm (held ~2s) → Open Incognito/Private Window (Ctrl+Shift+N / Ctrl+Shift+P)

## HUD Reference
- Mode: Current right-hand mode (System / Media)
- Gesture: Most recent stable gestures (shown as “R:<gesture> L:<gesture>”)
- Per-hand lines: One line per detected hand (e.g., “Right: open_palm (0.95)”, “Left: swipe_right (0.90)”) 
- Action: Last executed action
- Conf: Current confidence and minimum threshold
- FPS: Processing speed
- Cooling down: Visible hint when a gesture is within cooldown
- Mode switch bar: Yellow fill indicates progress toward switching on 🤏 (right hand)

## Tuning & Settings (hastayanam/config.py)
- `THRESHOLDS.confidence_min` (default 0.85): Raise to reduce false positives; lower for more responsive detection.
- `THRESHOLDS.stability_frames` (default 5): Number of consecutive frames required for a stable pose; increase if gestures flap.
- `THRESHOLDS.gesture_cooldown_s` (default 0.9): Global default cooldown; larger value = fewer repeated triggers.
- `THRESHOLDS.mode_switch_hold_s` (default 3.0): Hold duration required on 🤏 to switch the right-hand mode.
- `THRESHOLDS.pinch_distance_threshold` (default 0.05): Max thumb–index distance for detecting a pinch.
- `THRESHOLDS.swipe_min_displacement_px` (default 160): Horizontal wrist displacement to detect swipes; increase if accidental swipes occur.

## Troubleshooting
- No reaction: Ensure webcam is free, your hand is in frame, and lighting is sufficient.
- Wrong action triggered: Increase `confidence_min`, `stability_frames`, or `swipe_min_displacement_px`.
- Too many repeats: Increase `gesture_cooldown_s` or per-gesture cooldowns in `app.py` mapping.
- Administrator privileges: Some hotkeys in certain apps may require running the terminal as Administrator.
