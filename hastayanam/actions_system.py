import subprocess
import ctypes
import pyautogui as pag


def show_desktop():
	pag.hotkey('winleft', 'd')


def volume_up(steps: int = 2):
	for _ in range(steps):
		pag.press('volumeup')


def volume_down(steps: int = 2):
	for _ in range(steps):
		pag.press('volumedown')


def next_window():
	pag.hotkey('alt', 'tab')


def prev_window():
	pag.hotkey('alt', 'shift', 'tab')


def lock_screen():
	ctypes.windll.user32.LockWorkStation()


def confirm_enter():
	pag.press('enter')


def sleep_computer():
	# Hibernate (sleep) – requires hibernation enabled
	subprocess.run(["shutdown", "/h"], shell=True)


def shutdown_now():
	subprocess.run(["shutdown", "/s", "/t", "0"], shell=True)
