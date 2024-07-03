import cv2
import numpy as np

class CamVision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def detect_ring(frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_blue = np.array([100, 150, 0])
        upper_blue = np.array([140, 255, 255])

        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        mask = cv2.GaussianBlur(mask, (5, 5), 0)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 500:
                continue

            x, y, w, h = cv2.boundingRect(contour)

            aspect_ratio = w / float(h)
            area = cv2.contourArea(contour)
            rect_area = w * h
            extent = area / float(rect_area)

            if 0.8 < aspect_ratio < 1.2 and extent > 0.5:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(f"Кольцо найдено! Позиция: ({x}, {y}), Ширина: {w}, Высота: {h}")

