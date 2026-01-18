import cv2

face_cascade = cv2.CascadeClassifier(
    "haarcascade_frontalface_default.xml"
)
eye_cascade = cv2.CascadeClassifier(
    "haarcascade_eye.xml"
)

cap = cv2.VideoCapture(0)

blink_detected = False
no_eye_frames = 0

print("Please blink to prove liveness")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        if len(eyes) == 0:
            no_eye_frames += 1
        else:
            no_eye_frames = 0

        if no_eye_frames > 3:
            blink_detected = True
            cv2.putText(
                frame, "LIVENESS VERIFIED",
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2
            )
            break

    cv2.imshow("Liveness Check", frame)

    if blink_detected:
        print("Blink detected. Liveness verified.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
