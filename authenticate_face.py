import cv2
import os

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)

stored_face_path = "known_faces/user_face.jpg"

if not os.path.exists(stored_face_path):
    print("No registered face found")
    exit()

stored_face = cv2.imread(stored_face_path, cv2.IMREAD_GRAYSCALE)
stored_face = cv2.resize(stored_face, (200, 200))

cap = cv2.VideoCapture(0)

print("Authenticating... Press 'q' to quit")

authenticated = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    for (x, y, w, h) in faces:
        live_face = gray[y:y+h, x:x+w]
        live_face = cv2.resize(live_face, (200, 200))

        difference = cv2.absdiff(stored_face, live_face)
        score = difference.mean()

        if score < 60:
            authenticated = True
            cv2.putText(
                frame, "ACCESS GRANTED",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2
            )
        else:
            cv2.putText(
                frame, "ACCESS DENIED",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2
            )

        cv2.rectangle(
            frame, (x, y), (x+w, y+h),
            (255, 0, 0), 2
        )

    cv2.imshow("Face Authentication", frame)

    if authenticated:
        print("User authenticated successfully")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
