import threading
import time
import ctypes


def get_time():
    while True:
        pass

my_thread = threading.Thread(target=get_time)
my_thread.daemon = True
my_thread.start()

time.sleep(1)

thread = my_thread

exc = ctypes.py_object(SystemExit)
res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
    ctypes.c_long(thread.ident), exc)
