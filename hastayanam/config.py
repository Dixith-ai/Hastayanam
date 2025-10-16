from dataclasses import dataclass


@dataclass
class Thresholds:
	# Distances are in normalized coordinates [0,1]
	fist_closed_distance: float = 0.08
	thumbs_up_angle_deg: float = 35.0
	thumbs_down_angle_deg: float = 35.0
	palm_open_distance: float = 0.18
	finger_extended_cos_threshold: float = 0.7
	swipe_min_displacement_px: int = 160
	hold_min_duration_s: float = 2.0
	gesture_cooldown_s: float = 0.9
	confidence_min: float = 0.85
	stability_frames: int = 5
	mode_switch_hold_s: float = 3.0
	pinch_distance_threshold: float = 0.05


@dataclass
class VideoConfig:
	camera_index: int = 0
	width: int = 1280
	height: int = 720
	fps_smoothing: float = 0.9
	swap_handedness: bool = True  # Flip Left/Right labels for mirrored webcams


@dataclass
class OverlayConfig:
	font_scale: float = 0.7
	thickness: int = 2
	padding: int = 10
	row_gap: int = 28
	bg_alpha: float = 0.35


THRESHOLDS = Thresholds()
VIDEO = VideoConfig()
OVERLAY = OverlayConfig()
