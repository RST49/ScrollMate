import cv2
import mediapipe as mp
import asyncio
import websockets
from pynput.keyboard import Controller

# Initialize Mediapipe and keyboard controller
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
keyboard = Controller()

# Gesture Mapping
def detect_gesture(landmarks):
    if landmarks:
        thumb_tip = landmarks[4].y
        index_tip = landmarks[8].y
        if thumb_tip < index_tip:  # Thumbs Up
            return "page_up"
        elif thumb_tip > index_tip:  # Thumbs Down
            return "page_down"
    return None

# WebSocket Handler
async def gesture_server(websocket, path):
    cap = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break

            # Flip the frame for a mirror effect
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)

            # Detect gestures
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    gesture = detect_gesture(hand_landmarks.landmark)
                    if gesture:
                        await websocket.send(gesture)

            # Show the frame (optional for debugging)
            cv2.imshow("Gesture Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Start WebSocket Server
start_server = websockets.serve(gesture_server, "localhost", 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
