import RPi.GPIO as GPIO
import time
import threading

TRIG = 26
ECHO = 24

_running = False
_last_dis = None
_start = False
_thread = None
_count = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)


def distance():
    if _last_dis:
        return _last_dis
    return refresh_distance()


def refresh_distance():
    global _running, _last_dis, _count
    if _running:
        if _last_dis:
            return _last_dis
        else:
            return -1
    else:
        _running = True
        tmmp = time.time()
        while GPIO.input(ECHO):
            if time.time() - tmmp > 0.02:
                _running = False
                return -1
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.000015)
        GPIO.output(TRIG, GPIO.LOW)
        tmmp = time.time()
        while not GPIO.input(ECHO):
            if time.time() - tmmp > 0.02:
                _running = False
                return -1
        t1 = time.time()
        while GPIO.input(ECHO):
            if time.time() - t1 > 0.02:
                _running = False
                return -1
        t2 = time.time()
        dis = (t2 - t1) * 17000
        _last_dis = dis
        _count += 1
        _running = False
        return dis


def loop():
    while _start:
        refresh_distance()
        time.sleep(0.005)


def start():
    run()


def run():
    global _start, _thread
    if not _start:
        _start = True
        if _thread is None:
            _thread = threading.Thread(target=loop)
        _thread.start()


def stop():
    global _start, _thread
    _start = False
    _thread = None


if __name__ == '__main__':
    # run()
    # # time.sleep(60)
    # while True:
    #     print(distance())
    #     if input() == '0':
    #         break
    # stop()
    # print(_count)
    test()
