import time
import numpy as np


class FpsMeter:
	def __init__(self, smoothing: float = 0.9):
		self.prev_time = None
		self.smoothing = smoothing
		self.fps = 0.0

	def tick(self) -> float:
		now = time.time()
		if self.prev_time is None:
			self.prev_time = now
			return 0.0
		dt = now - self.prev_time
		self.prev_time = now
		if dt > 0:
			inst = 1.0 / dt
			self.fps = self.smoothing * self.fps + (1 - self.smoothing) * inst if self.fps > 0 else inst
		return self.fps


def normalize_landmarks(landmarks, width: int, height: int):
	# Convert to np.array of shape (21, 3), normalized to [0,1]
	pts = np.array([[lm.x, lm.y, lm.z] for lm in landmarks], dtype=np.float32)
	# Already normalized by MediaPipe in x,y; keep as-is for consistency
	return pts


def landmark_to_pixel(landmark_xy, width: int, height: int):
	x = int(landmark_xy[0] * width)
	y = int(landmark_xy[1] * height)
	return x, y


def vector_cosine(a: np.ndarray, b: np.ndarray) -> float:
	na = a / (np.linalg.norm(a) + 1e-8)
	nb = b / (np.linalg.norm(b) + 1e-8)
	return float(np.clip(np.dot(na, nb), -1.0, 1.0))


def distance(a: np.ndarray, b: np.ndarray) -> float:
	return float(np.linalg.norm(a - b))


class RingBuffer:
	def __init__(self, size: int):
		self.size = size
		self.buf = []

	def append(self, item):
		self.buf.append(item)
		if len(self.buf) > self.size:
			self.buf.pop(0)

	def items(self):
		return self.buf

	def clear(self):
		self.buf.clear()


class CooldownManager:
	def __init__(self, default_seconds: float = 0.6):
		self.default_seconds = default_seconds
		self._gesture_to_next_time = {}

	def ready(self, gesture_name: str) -> bool:
		now = time.time()
		return now >= self._gesture_to_next_time.get(gesture_name, 0.0)

	def trigger(self, gesture_name: str, seconds: float | None = None):
		now = time.time()
		interval = self.default_seconds if seconds is None else seconds
		self._gesture_to_next_time[gesture_name] = now + interval
