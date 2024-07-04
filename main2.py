import time

from djitellopy import Tello

tello = Tello()

tello.connect()
tello.takeoff()

tello.move_back(30)

tello.land()