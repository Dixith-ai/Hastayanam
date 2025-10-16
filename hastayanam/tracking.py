from typing import Optional, Tuple, List, Dict, Any
import cv2
import mediapipe as mp
from .config import VIDEO
from .utils import normalize_landmarks


class HandTracker:
	def __init__(self):
		self.mp_hands = mp.solutions.hands
		self.hands = self.mp_hands.Hands(
			static_image_mode=False,
			max_num_hands=2,
			min_detection_confidence=0.5,
			min_tracking_confidence=0.5,
		)
		self.drawer = mp.solutions.drawing_utils

	def process(self, frame_bgr) -> Dict[str, Any]:
		# Convert to RGB for MediaPipe
		rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
		result = self.hands.process(rgb)
		return {
			"result": result,
			"hands": result.multi_hand_landmarks or [],
			"handedness": result.multi_handedness or [],
		}

	def extract_normalized(self, frame_bgr) -> List[Dict[str, Any]]:
		"""Returns list of dicts: { 'pts': np.ndarray(21,3), 'label': 'Left'|'Right' }"""
		out = []
		proc = self.process(frame_bgr)
		hands = proc["hands"]
		hness = proc["handedness"]
		if not hands:
			return out
		h, w = frame_bgr.shape[:2]
		for i, hand_lms in enumerate(hands):
			label = "Unknown"
			if i < len(hness) and hness[i].classification:
				label = hness[i].classification[0].label
				if VIDEO.swap_handedness:
					label = "Right" if label == "Left" else ("Left" if label == "Right" else label)
			pts = normalize_landmarks(hand_lms.landmark, w, h)
			out.append({"pts": pts, "label": label})
		return out

	def draw(self, frame_bgr, proc_dict: Dict[str, Any]):
		result = proc_dict.get("result") if isinstance(proc_dict, dict) else proc_dict
		if result and result.multi_hand_landmarks:
			for i, hand_landmarks in enumerate(result.multi_hand_landmarks):
				self.drawer.draw_landmarks(frame_bgr, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)


def open_camera(index: int = VIDEO.camera_index, width: int = VIDEO.width, height: int = VIDEO.height):
	cap = cv2.VideoCapture(index)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
	return cap
