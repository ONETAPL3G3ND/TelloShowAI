import cv2
import numpy as np
from djitellopy import Tello


def detect_shapes(frame, lower_color, upper_color):
    find = False
    x = None
    y = None
    w = None
    h = None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Создаем маску для заданного цвета
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Применяем размытие, чтобы уменьшить шумы
    mask = cv2.GaussianBlur(mask, (5, 5), 0)

    # Применяем морфологические операции для улучшения маски
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Находим контуры в маске
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 2000:
            continue

        # Находим ограничивающий прямоугольник для каждого контура
        x, y, w, h = cv2.boundingRect(contour)

        # Проверяем соотношение сторон и приблизительность формы к кругу или квадрату
        aspect_ratio = w / float(h)
        area = cv2.contourArea(contour)
        rect_area = w * h
        extent = area / float(rect_area)
        find = False

        # Если контур достаточно круглый
        if 0.8 < aspect_ratio < 1.2 and extent > 0.5:
            shape = "неизвестная форма"
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

            if len(approx) > 4:
                shape = "кольцо"
            elif len(approx) == 4:
                shape = "квадрат"

            if shape == "кольцо":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print(f"Кольцо найдено! Позиция: ({x}, {y}), Ширина: {w}, Высота: {h}")
                find = True
                return frame, x, y, w, h
            elif shape == "квадрат":
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                print(f"Квадрат найден! Позиция: ({x}, {y}), Ширина: {w}, Высота: {h}")
                find = True
                return [frame, x, y, w, h]
    return [frame, None, None, None, None]


def main(lower_color, upper_color):
    tello = Tello()
    tello.connect()
    print(tello.query_battery())
    tello.streamon()
    tello.takeoff()
    tello.move_down(30)

    while True:
        frame = tello.get_frame_read().frame


        result = detect_shapes(frame, lower_color, upper_color)
        frame = result[0]
        x = result[1]
        y = result[2]
        w = result[3]
        h = result[4]
        centerx = 1080/2
        centery = 1920/2
        if x != None:
            print(f"Detect: {x}, {y}, {w}, {h}")
            if y < centery:
                tello.move_up(10)
            elif y > centery:
                tello.move_down(10)
        cv2.imshow('Shape Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    tello.land()
    cv2.destroyAllWindows()


# Пример диапазона для голубого цвета
lower_blue = np.array([100, 150, 0])
upper_blue = np.array([140, 255, 255])

# Запуск основного цикла с указанием диапазона цвета
main(lower_blue, upper_blue)
