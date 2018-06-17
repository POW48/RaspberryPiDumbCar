from picamera.array import PiRGBArray
import test_camera
import controller
import picamera

car = controller.Vehicle()
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.framerate = 60
threshold = 50
rawCapture = PiRGBArray(camera, size=(320, 240))


def center_ball():
    car.turn_right()
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        _, bound = test_camera.find_circle(frame.array)
        center_x = bound[0] + bound[2] / 2
        print(center_x)
        if camera.resolution[0] - threshold <= center_x <= camera.resolution[0] + threshold:
            car.stop()
            break
        rawCapture.truncate()
        rawCapture.seek(0)


def go_ball():
    pass


def catch_ball():
    pass


def release_ball():
    pass


def go_door():
    pass


if __name__ == '__main__':
    center_ball()
