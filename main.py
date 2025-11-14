# main.py

import cv2
from gesture_controller.hand_detector import HandDetector
from gesture_controller.gesture_recognizer import GestureRecognizer


def main():
    """The main loop for the hand gesture media controller."""

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detector = HandDetector()
    recognizer = GestureRecognizer()

    print("Starting Gesture Controller...")
    print("Gestures:")
    print(" - Index Finger Up: Cursor Movement")
    print(" - Fist (while pointing): Mouse Click")
    print(" - All Five Fingers Up: Play/Pause")
    print(" - Middle Finger Up: Seek Forward (L)")
    print(" - Index & Middle Fingers Up: Seek Backward (J)")
    print(" - Middle & Ring Fingers Up: Volume Up")
    print(" - Ring Finger Up: Volume Down")
    print("---")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)

        img, lm_list = detector.find_hands(img, draw=True)

        if lm_list:
            fingers = detector.fingers_up(lm_list)

            # CRITICAL: Pass lm_list here for cursor coordinates
            recognizer.recognize_and_act(fingers, lm_list)

            # Display status
            cv2.putText(img, f"Fingers: {fingers}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f"Action: {recognizer.last_action}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0),
                        2)

        cv2.imshow("Hand Gesture Media Controller", img)

        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Gesture Controller stopped.")


if __name__ == "__main__":
    main()