import pyautogui as pag


def play_pause():
	pag.press('space')


def next_slide():
	pag.press('right')


def prev_slide():
	pag.press('left')


def volume_up():
	pag.press('volumeup')


def volume_down():
	pag.press('volumedown')


def start_presentation():
	# For PowerPoint, F5 starts; fallback to Enter/Space
	pag.press('f5')
