# gesture_controller/media_control.py

import pyautogui
import numpy as np

# Set the safety pause to 0 for instantaneous cursor movement
pyautogui.PAUSE = 0


def move_cursor(x, y, screen_width, screen_height):
    """Maps normalized hand coordinates (x, y) to screen resolution."""
    # Use a slightly restricted input range (e.g., 0.1 to 0.9) for better sensitivity and edge avoidance
    target_x = np.interp(x, [0.1, 0.9], [0, screen_width]).astype(int)
    target_y = np.interp(y, [0.1, 0.9], [0, screen_height]).astype(int)

    pyautogui.moveTo(target_x, target_y)


def mouse_click():
    """Simulates a left mouse click."""
    print("ACTION: Mouse Click")
    pyautogui.click()


def play_pause():
    """Simulates pressing the spacebar to Play/Pause media."""
    print("ACTION: Play/Pause")
    pyautogui.press('space')


def volume_up():
    """Simulates pressing the Up arrow key to increase volume."""
    print("ACTION: Volume Up")
    pyautogui.press('up')


def volume_down():
    """Simulates pressing the Down arrow key to decrease volume."""
    print("ACTION: Volume Down")
    pyautogui.press('down')


def seek_forward():
    """Simulates pressing 'l' for YouTube seek forward (10s)."""
    print("ACTION: Seek Forward (L)")
    pyautogui.press('l')


def seek_backward():
    """Simulates pressing 'j' for YouTube seek backward (10s)."""
    print("ACTION: Seek Backward (J)")
    pyautogui.press('j')