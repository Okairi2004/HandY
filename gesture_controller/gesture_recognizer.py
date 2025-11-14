# gesture_controller/gesture_recognizer.py

from . import media_control
import pyautogui

# Get screen resolution once
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


class GestureRecognizer:
    def __init__(self):
        self.last_action = None
        self.action_delay_frames = 15  # Cooldown for non-cursor actions
        self.action_counter = 0
        self.is_cursor_mode = False
        self.cursor_index_tip = None

    def recognize_and_act(self, fingers, lm_list):
        """Recognizes the gesture and executes the corresponding action."""
        current_action = None

        # Get the normalized coordinates (x, y) of the Index Finger Tip (Landmark 8)
        if lm_list and len(lm_list) > 8:
            self.cursor_index_tip = (lm_list[8][1], lm_list[8][2])

        # --- Gesture Definitions ---

        # 1. CURSOR MODE: Only Index Finger Up -> [0, 1, 0, 0, 0]
        if fingers == [0, 1, 0, 0, 0] and self.cursor_index_tip:
            self.is_cursor_mode = True

            media_control.move_cursor(
                self.cursor_index_tip[0],
                self.cursor_index_tip[1],
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            )
            return  # Skip debouncing for continuous movement

        # 2. CLICK ACTION: Fist while in Cursor Mode
        elif fingers == [0, 0, 0, 0, 0] and self.is_cursor_mode:
            current_action = "MOUSE_CLICK"
            self.is_cursor_mode = False

            # 3. PLAY/PAUSE: All Five Fingers Up
        elif fingers == [1, 1, 1, 1, 1]:
            current_action = "PLAY_PAUSE"
            self.is_cursor_mode = False

            # 4. SEEK FORWARD (Middle Finger Up) -> [0, 0, 1, 0, 0]
        elif fingers == [0, 0, 1, 0, 0]:
            current_action = "SEEK_FORWARD"
            self.is_cursor_mode = False

        # 5. SEEK BACKWARD (Index and Middle Fingers Up) -> [0, 1, 1, 0, 0]
        elif fingers == [0, 1, 1, 0, 0]:
            current_action = "SEEK_BACKWARD"
            self.is_cursor_mode = False

        # 6. VOLUME UP (Middle and Ring Fingers Up) -> [0, 0, 1, 1, 0]
        elif fingers == [0, 0, 1, 1, 0]:
            current_action = "VOLUME_UP"
            self.is_cursor_mode = False

        # 7. VOLUME DOWN (Only Ring Finger Up) -> [0, 0, 0, 1, 0]
        elif fingers == [0, 0, 0, 1, 0]:
            current_action = "VOLUME_DOWN"
            self.is_cursor_mode = False

        # Default: Reset
        else:
            self.is_cursor_mode = False
            self.last_action = None
            self.action_counter = 0

        # --- Debounce/Cooldown Logic (For non-cursor actions) ---
        if current_action:
            # THIS LINE IS FIXED: Correctly uses self.last_action
            if current_action != self.last_action or self.action_counter >= self.action_delay_frames:
                self.execute_action(current_action)
                self.last_action = current_action
                self.action_counter = 0
            else:
                self.action_counter += 1

    def execute_action(self, action_name):
        """Maps the recognized gesture name to the actual control function."""
        if action_name == "MOUSE_CLICK":
            media_control.mouse_click()
        elif action_name == "PLAY_PAUSE":
            media_control.play_pause()
        elif action_name == "VOLUME_UP":
            media_control.volume_up()
        elif action_name == "VOLUME_DOWN":
            media_control.volume_down()
        elif action_name == "SEEK_FORWARD":
            media_control.seek_forward()
        elif action_name == "SEEK_BACKWARD":
            media_control.seek_backward()