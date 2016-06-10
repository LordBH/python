import multiprocessing as mp
import time


def f():
    for x in range(10):
        print('F', x)
        time.sleep(.50)


def s():
    for x in range(10):
        print('S', x)
        time.sleep(.50)


if __name__ == '__main__':
    my_process = mp.Process(target=f)
    # my_process2 = mp.Process(target=s)
    my_process.start()
    # my_process2.start()
    # my_process.join()
    # my_process2.join()

    print("SLEEP")
    time.sleep(30)
