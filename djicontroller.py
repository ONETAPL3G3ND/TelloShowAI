from djitellopy import Tello

class Controller:

    def __init__(self):
        self.tello = Tello()

    def Connect(self):
        self.tello.connect()

    def StreamOn(self):
        self.tello.streamon()

    def TakeOff(self):
        self.tello.takeoff()

    def GetFrame(self):
        return self.tello.get_frame_read().frame


    def setup(self):
        self.Connect()
        self.StreamOn()
        self.TakeOff()
