# gesture_controller/hand_detector.py

import mediapipe as mp


class HandDetector:
    """A utility class to wrap MediaPipe Hands model for easy detection."""

    def __init__(self, static_mode=False, max_hands=1, model_complexity=1, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_mode,
            max_num_hands=max_hands,
            model_complexity=model_complexity,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Tip landmark indices
        self.tip_ids = [4, 8, 12, 16, 20]

    def find_hands(self, img, draw=True):
        """Processes an image to detect hands and their landmarks."""
        img_rgb = img[:, :, ::-1]
        self.results = self.hands.process(img_rgb)

        lm_list = []
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                lm_list = [(id, landmark.x, landmark.y, landmark.z)
                           for id, landmark in enumerate(hand_landmarks.landmark)]

                if draw:
                    self.mp_drawing.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_drawing_styles.get_default_hand_landmarks_style(),
                        self.mp_drawing_styles.get_default_hand_connections_style()
                    )

        return img, lm_list

    def fingers_up(self, lm_list):
        """Checks which fingers are extended (up) based on landmark positions."""
        if not lm_list:
            return [0] * 5

        fingers = []

        # 1. Thumb: Check X position (left/right) against the joint below
        if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 2-5. Other Fingers: Check Y position (up/down) against the joint below
        for id in range(1, 5):
            # Smaller Y is higher on the screen
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers