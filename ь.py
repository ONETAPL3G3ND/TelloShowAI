import cv2
from djitellopy import Tello

tello = Tello()
tello.connect()
tello.streamon()
tello.takeoff()
tello.move_up(100)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_face(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) > 0:
        return faces[0]
    return None


while True:
    frame = tello.get_frame_read().frame
    frame = cv2.resize(frame, (640, 480))
    face = detect_face(frame)

    if face is not None:
        (x, y, w, h) = face
        x_center = x + w // 2
        y_center = y + h // 2

        frame_center_x = 320
        frame_center_y = 240

        if x_center < frame_center_x - 10:
            tello.send_rc_control(-40, 0, 0, 0)
        elif x_center > frame_center_x + 10:
            tello.send_rc_control(40, 0, 0, 0)
        else:
            tello.send_rc_control(0, 0, 0, 0)

        if y_center < frame_center_y - 10:
            tello.send_rc_control(0, 0, 40, 0)
        elif y_center > frame_center_y + 10:
            tello.send_rc_control(0, 0, -40, 0)
        else:
            tello.send_rc_control(0, 0, 0, 0)

        face_area = w * h
        frame_area = 640 * 480
        face_ratio = face_area / frame_area

        if face_ratio < 0.1:
            tello.send_rc_control(0, 40, 0, 0)
        else:
            tello.send_rc_control(0, 0, 0, 0)

    cv2.imshow("Tello Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.land()
cv2.destroyAllWindows()
