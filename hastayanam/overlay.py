import cv2
from .config import OVERLAY, THRESHOLDS


def draw_hud(frame, *, mode: str, gesture: str, action: str, confidence: float, fps: float, mode_progress: float = 0.0, cooldown_hint: str = "", per_hand: list | None = None):
	h, w = frame.shape[:2]
	pad = OVERLAY.padding
	row = OVERLAY.row_gap
	alpha = OVERLAY.bg_alpha

	# Background for text area
	rows = 6 + (len(per_hand) if per_hand else 0)
	box_w = 560
	box_h = pad * 2 + row * rows
	overlay = frame.copy()
	cv2.rectangle(overlay, (0, 0), (box_w, box_h), (0, 0, 0), -1)
	cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

	# Text lines
	org_y = pad + 20
	font = cv2.FONT_HERSHEY_SIMPLEX
	cv2.putText(frame, f"Mode: {mode}", (pad, org_y + row * 0), font, OVERLAY.font_scale, (0, 255, 255), OVERLAY.thickness, cv2.LINE_AA)
	cv2.putText(frame, f"Gesture: {gesture}", (pad, org_y + row * 1), font, OVERLAY.font_scale, (255, 255, 255), OVERLAY.thickness, cv2.LINE_AA)
	cv2.putText(frame, f"Action: {action}", (pad, org_y + row * 2), font, OVERLAY.font_scale, (0, 255, 0), OVERLAY.thickness, cv2.LINE_AA)
	cv2.putText(frame, f"Conf: {confidence:.2f} (min {THRESHOLDS.confidence_min:.2f})", (pad, org_y + row * 3), font, OVERLAY.font_scale, (200, 200, 200), OVERLAY.thickness, cv2.LINE_AA)
	cv2.putText(frame, f"FPS: {fps:.1f}", (pad, org_y + row * 4), font, OVERLAY.font_scale, (200, 200, 200), OVERLAY.thickness, cv2.LINE_AA)
	if cooldown_hint:
		cv2.putText(frame, cooldown_hint, (pad, org_y + row * 5), font, OVERLAY.font_scale, (0, 165, 255), OVERLAY.thickness, cv2.LINE_AA)

	# Per hand lines
	if per_hand:
		start = 6
		for i, item in enumerate(per_hand):
			text = f"{item['label']}: {item['gesture']} ({item['conf']:.2f})"
			cv2.putText(frame, text, (pad, org_y + row * (start + i)), font, OVERLAY.font_scale, (180, 220, 255), OVERLAY.thickness, cv2.LINE_AA)

	# Mode switch progress bar
	if mode_progress > 0.0:
		bar_x, bar_y = pad, box_h + 6
		bar_w, bar_h = 240, 10
		cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_w, bar_y + bar_h), (80, 80, 80), 1)
		fill_w = int(bar_w * max(0.0, min(1.0, mode_progress)))
		cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_h), (0, 255, 255), -1)
