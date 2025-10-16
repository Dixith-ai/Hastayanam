import time
import pyautogui as pag


def next_tab():
	pag.hotkey('ctrl', 'tab')


def prev_tab():
	pag.hotkey('ctrl', 'shift', 'tab')


def new_tab():
	pag.hotkey('ctrl', 't')


def close_tab():
	pag.hotkey('ctrl', 'w')


def reload_page():
	pag.hotkey('ctrl', 'r')


def go_back():
	pag.hotkey('alt', 'left')


def go_forward():
	pag.hotkey('alt', 'right')


def open_incognito():
	# Try Chrome/Edge private window
	pag.hotkey('ctrl', 'shift', 'n')
	time.sleep(0.15)
	# Also try Firefox private window in case the active browser is Firefox
	pag.hotkey('ctrl', 'shift', 'p')
