import cv2
import os

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

print("Press 's' to save your face, 'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in faces:
        face_img = gray[y:y+h, x:x+w]
        cv2.rectangle(
            frame, (x, y), (x+w, y+h), (0, 255, 0), 2
        )

    cv2.imshow("Register Face", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and len(faces) == 1:
        os.makedirs("known_faces", exist_ok=True)
        cv2.imwrite("known_faces/user_face.jpg", face_img)
        print("Face registered successfully")
        break

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
