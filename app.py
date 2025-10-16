import time
from typing import Tuple
import cv2
import numpy as np

from hastayanam.config import VIDEO, THRESHOLDS
from hastayanam.tracking import HandTracker, open_camera
from hastayanam.gestures import GestureClassifier
from hastayanam.modes import ModeManager, Mode
from hastayanam.overlay import draw_hud
from hastayanam.utils import FpsMeter, CooldownManager

from hastayanam import actions_system as sys_actions
from hastayanam import actions_media as media_actions
from hastayanam import actions_browser as browser_actions


def map_action_system(gesture_name: str, is_hold: bool):
	if gesture_name == "open_palm":
		return "Show Desktop", sys_actions.show_desktop, 1.0
	if gesture_name == "point_up":
		return "Volume Up", lambda: sys_actions.volume_up(steps=1), 0.25
	if gesture_name == "point_down":
		return "Volume Down", lambda: sys_actions.volume_down(steps=1), 0.25
	if gesture_name == "swipe_right":
		return "Next Window", sys_actions.next_window, 0.9
	if gesture_name == "swipe_left":
		return "Previous Window", sys_actions.prev_window, 0.9
	if gesture_name == "fist":
		return ("Lock Screen" if not is_hold else "Sleep"), (sys_actions.lock_screen if not is_hold else sys_actions.sleep_computer), 1.5
	if gesture_name == "thumbs_up":
		return "Confirm / Enter", sys_actions.confirm_enter, 0.9
	return "", None, 0.9


def map_action_media(gesture_name: str, is_hold: bool):
	if gesture_name == "swipe_right":
		return "Next Slide/Video/Track", media_actions.next_slide, 0.8
	if gesture_name == "swipe_left":
		return "Previous Slide/Video/Track", media_actions.prev_slide, 0.8
	if gesture_name == "open_palm":
		return "Start/Resume", media_actions.start_presentation, 1.0
	if gesture_name == "fist":
		return "Pause", media_actions.play_pause, 0.9
	if gesture_name == "two_fingers":
		return "Play/Pause", media_actions.play_pause, 0.9
	if gesture_name == "thumbs_up":
		return "Volume Up", media_actions.volume_up, 0.25
	if gesture_name == "thumbs_down":
		return "Volume Down", media_actions.volume_down, 0.25
	return "", None, 0.9


def map_action_browser(gesture_name: str, is_hold: bool):
	if gesture_name == "swipe_right":
		return "Next Tab", browser_actions.next_tab, 0.8
	if gesture_name == "swipe_left":
		return "Previous Tab", browser_actions.prev_tab, 0.8
	if gesture_name == "open_palm":
		return "New Tab", browser_actions.new_tab, 1.0
	if gesture_name == "fist":
		return "Close Tab", browser_actions.close_tab, 0.9
	if gesture_name == "thumbs_up":
		return "Reload Page", browser_actions.reload_page, 1.0
	if gesture_name == "thumbs_down":
		return "Go Back", browser_actions.go_back, 0.8
	if gesture_name == "two_fingers":
		return "Go Forward", browser_actions.go_forward, 0.9
	if gesture_name == "open_palm" and is_hold:
		return "Incognito Window", browser_actions.open_incognito, 1.5
	return "", None, 0.9


def main():
	cap = open_camera()
	tracker = HandTracker()
	classifier_right = GestureClassifier()
	classifier_left = GestureClassifier()
	modes = ModeManager()  # Global mode: System ↔ Media ↔ Browser
	fpsm = FpsMeter(smoothing=VIDEO.fps_smoothing)
	cooldown = CooldownManager(default_seconds=THRESHOLDS.gesture_cooldown_s)

	last_executed_action = ""

	while True:
		ok, frame = cap.read()
		if not ok:
			break

		h, w = frame.shape[:2]
		proc = tracker.process(frame)
		hands = proc["hands"]
		handed = proc["handedness"]

		per_hand_info = []
		right_gesture = ("unknown", 0.0, False)
		left_gesture = ("unknown", 0.0, False)

		pairs = tracker.extract_normalized(frame)
		for item in pairs:
			lab = item["label"]
			if lab == "Right":
				res = classifier_right.infer(item["pts"], (w, h))
				right_gesture = (res.name, res.confidence, res.is_hold)
				per_hand_info.append({"label": "Right", "gesture": res.name, "conf": res.confidence})
			elif lab == "Left":
				res = classifier_left.infer(item["pts"], (w, h))
				left_gesture = (res.name, res.confidence, res.is_hold)
				per_hand_info.append({"label": "Left", "gesture": res.name, "conf": res.confidence})

		# Draw hands
		tracker.draw(frame, proc)

		# Global mode switch by pinch (either hand)
		if right_gesture[0] == "pinch" or left_gesture[0] == "pinch":
			modes.maybe_cycle_on_gesture("pinch")
		mode = modes.get()
		progress = modes.mode_switch_progress()

		# Determine the active gesture for this frame (prioritize Right if both present)
		active_gesture = right_gesture if right_gesture[1] >= left_gesture[1] else left_gesture

		# Map only within the active global mode
		if active_gesture[1] >= THRESHOLDS.confidence_min:
			if mode == Mode.SYSTEM:
				action_text, action_fn, cd = map_action_system(active_gesture[0], active_gesture[2])
			elif mode == Mode.MEDIA:
				action_text, action_fn, cd = map_action_media(active_gesture[0], active_gesture[2])
			else:
				action_text, action_fn, cd = map_action_browser(active_gesture[0], active_gesture[2])
		else:
			action_text, action_fn, cd = "", None, 0.0

		cooldown_hint = ""
		if action_fn is not None:
			g = f"{mode.name}:{active_gesture[0]}"
			if cooldown.ready(g):
				try:
					action_fn()
					last_executed_action = action_text
					cooldown.trigger(g, seconds=cd)
				except Exception:
					last_executed_action = f"Failed: {action_text}"
			else:
				cooldown_hint = f"Cooling down: {g}"

		fps = fpsm.tick()
		both_g = f"R:{right_gesture[0]} L:{left_gesture[0]}"
		draw_hud(frame, mode=mode.name.title(), gesture=both_g, action=last_executed_action, confidence=max(right_gesture[1], left_gesture[1]), fps=fps, mode_progress=progress, cooldown_hint=cooldown_hint, per_hand=per_hand_info)

		cv2.imshow("Hastayanam", frame)
		key = cv2.waitKey(1) & 0xFF
		if key == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()


if __name__ == "__main__":
	main()
