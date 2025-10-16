from enum import Enum
import time
from .config import THRESHOLDS


class Mode(Enum):
	SYSTEM = 0
	MEDIA = 1
	BROWSER = 2


class ModeManager:
	def __init__(self):
		self.mode = Mode.SYSTEM
		self._switch_start: float | None = None
		self._cooldown_until = 0.0

	def get(self) -> Mode:
		return self.mode

	def cycle(self):
		self.mode = Mode((self.mode.value + 1) % 3)

	def mode_switch_progress(self) -> float:
		if self._switch_start is None:
			return 0.0
		return min(1.0, (time.time() - self._switch_start) / THRESHOLDS.mode_switch_hold_s)

	def maybe_cycle_on_gesture(self, gesture_name: str):
		now = time.time()
		if now < self._cooldown_until:
			return
		if gesture_name == "pinch":
			if self._switch_start is None:
				self._switch_start = now
			elif (now - self._switch_start) >= THRESHOLDS.mode_switch_hold_s:
				self.cycle()
				self._cooldown_until = now + 1.2
				self._switch_start = None
		else:
			self._switch_start = None
