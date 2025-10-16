from dataclasses import dataclass
from typing import Optional, Tuple
import time
import numpy as np
from .config import THRESHOLDS
from .utils import distance, RingBuffer


# MediaPipe Hands indices for convenience
WRIST = 0
THUMB_TIP = 4
INDEX_TIP = 8
MIDDLE_TIP = 12
RING_TIP = 16
PINKY_TIP = 20
INDEX_PIP = 6
MIDDLE_PIP = 10
RING_PIP = 14
PINKY_PIP = 18
THUMB_IP = 3


@dataclass
class GestureResult:
	name: str
	confidence: float
	is_hold: bool = False
	hold_seconds: float = 0.0


class TemporalState:
	def __init__(self):
		self.last_gesture: Optional[str] = None
		self.last_change_time: float = time.time()
		self.cooldown_until: float = 0.0
		self.wrist_history = RingBuffer(size=8)
		self.stability_buffer = RingBuffer(size=THRESHOLDS.stability_frames)

	def update_wrist(self, wrist_xy: Tuple[float, float]):
		self.wrist_history.append((time.time(), wrist_xy))

	def check_swipe(self, width_px: int) -> Optional[str]:
		hist = self.wrist_history.items()
		if len(hist) < 2:
			return None
		# Compare earliest vs latest
		t0, p0 = hist[0]
		_, p1 = hist[-1]
		dx = (p1[0] - p0[0]) * width_px
		if abs(dx) >= THRESHOLDS.swipe_min_displacement_px:
			return "swipe_right" if dx > 0 else "swipe_left"
		return None

	def stable_label(self, label: str) -> Optional[str]:
		self.stability_buffer.append(label)
		buf = self.stability_buffer.items()
		if len(buf) < self.stability_buffer.size:
			return None
		if all(x == label for x in buf):
			return label
		return None


def _is_finger_extended(tip, pip, wrist) -> bool:
	# Finger extended if tip is further from wrist than pip in Euclidean distance
	return distance(tip, wrist) - distance(pip, wrist) > 0.02


def _count_extended(pts: np.ndarray) -> int:
	w = pts[WRIST]
	ext = 0
	if _is_finger_extended(pts[THUMB_TIP], pts[THUMB_IP], w):
		ext += 1
	if _is_finger_extended(pts[INDEX_TIP], pts[INDEX_PIP], w):
		ext += 1
	if _is_finger_extended(pts[MIDDLE_TIP], pts[MIDDLE_PIP], w):
		ext += 1
	if _is_finger_extended(pts[RING_TIP], pts[RING_PIP], w):
		ext += 1
	if _is_finger_extended(pts[PINKY_TIP], pts[PINKY_PIP], w):
		ext += 1
	return ext


def classify_static(pts: np.ndarray) -> Tuple[str, float]:
	w = pts[WRIST]
	thumb_ext = _is_finger_extended(pts[THUMB_TIP], pts[THUMB_IP], w)
	index_ext = _is_finger_extended(pts[INDEX_TIP], pts[INDEX_PIP], w)
	middle_ext = _is_finger_extended(pts[MIDDLE_TIP], pts[MIDDLE_PIP], w)
	ring_ext = _is_finger_extended(pts[RING_TIP], pts[RING_PIP], w)
	pinky_ext = _is_finger_extended(pts[PINKY_TIP], pts[PINKY_PIP], w)

	# Pinch: thumb tip close to index tip
	pinch_dist = distance(pts[THUMB_TIP], pts[INDEX_TIP])
	if pinch_dist <= THRESHOLDS.pinch_distance_threshold:
		return "pinch", 0.95

	extended = sum([thumb_ext, index_ext, middle_ext, ring_ext, pinky_ext])

	# Fist: none extended
	if extended == 0:
		return "fist", 0.95

	# Open palm: all extended
	if extended == 5:
		return "open_palm", 0.95

	# Two fingers (index + middle)
	if index_ext and middle_ext and not ring_ext and not pinky_ext and not thumb_ext:
		return "two_fingers", 0.9

	# Thumbs up / down based on thumb extended and its y relative to wrist
	if thumb_ext and not index_ext and not middle_ext and not ring_ext and not pinky_ext:
		if pts[THUMB_TIP][1] < w[1]:
			return "thumbs_up", 0.9
		else:
			return "thumbs_down", 0.9

	# Point up / down: only index extended
	if index_ext and not middle_ext and not ring_ext and not pinky_ext:
		if pts[INDEX_TIP][1] < w[1]:
			return "point_up", 0.85
		else:
			return "point_down", 0.85

	# Default unknown
	return "unknown", 0.3


class GestureClassifier:
	def __init__(self):
		self.state = TemporalState()

	def infer(self, pts: np.ndarray, frame_size: Tuple[int, int]) -> GestureResult:
		width_px, height_px = frame_size
		wrist_xy = (pts[WRIST][0], pts[WRIST][1])
		self.state.update_wrist(wrist_xy)

		name, conf = classify_static(pts)

		# Require stability
		stable = self.state.stable_label(name)
		if stable is not None:
			name = stable
		else:
			# Not stable yet; emit low confidence unknown to avoid flapping
			return GestureResult(name="unknown", confidence=0.0, is_hold=False, hold_seconds=0.0)

		# Temporal swipes override for strong movement
		swipe = self.state.check_swipe(width_px)
		if swipe is not None and name in ("open_palm", "two_fingers", "unknown"):
			name = swipe
			conf = 0.9

		# Hold detection
		now = time.time()
		is_hold = False
		hold_seconds = 0.0
		if name == self.state.last_gesture:
			hold_seconds = now - self.state.last_change_time
			if hold_seconds >= THRESHOLDS.hold_min_duration_s:
				is_hold = True
		else:
			self.state.last_gesture = name
			self.state.last_change_time = now

		return GestureResult(name=name, confidence=conf, is_hold=is_hold, hold_seconds=hold_seconds)
