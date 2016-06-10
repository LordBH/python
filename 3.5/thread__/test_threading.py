import threading
import time


def f():
    while True:
        time.sleep(.5)
        print('F')


def f2():
    while True:
        time.sleep(.5)
        print('@')


my_first_thread = threading.Thread(target=f)
my_second_thread = threading.Thread(target=f2)


my_first_thread.start()
my_second_thread.start()


