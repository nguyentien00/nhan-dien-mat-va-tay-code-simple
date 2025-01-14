import cv2
import mediapipe as mp


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
mp_drawing_util = mp.solutions.drawing_utils
mp_drawing_style = mp.solutions.drawing_styles

mp_hand = mp.solutions.hands
hands = mp_hand.Hands(
    model_complexity = 0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1,4)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y),(x+w, y+h), (255,0,0),2)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for idx, hand in enumerate(result.multi_hand_landmarks):

            mp_drawing_util.draw_landmarks(
                img,
                hand,
                mp_hand.HAND_CONNECTIONS,
                mp_drawing_style.get_default_hand_landmarks_style(),
                mp_drawing_style.get_default_hand_connections_style()
                
            )
            lbl = result.multi_handedness[idx].classification[0].label
            if lbl == "left":
                for id, lm in enumerate(hand.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if id == 8:
                        cv2.circle(img, (cx, cy), 10, (0,255,0), cv2.FILLED)
                    
                
    cv2.imshow("nhan dien ban tay bang python", img)
    key = cv2.waitKey(1)
    
    if key == 27:
        break

cap.release()