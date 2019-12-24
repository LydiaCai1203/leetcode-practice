import time
import threading


def threading_main():
    print('main thread start')
    thread = threading.Timer(5.0, threading_sub, args=['sub thread'])
    thread.start()
    print('main thread end')


def threading_sub(name):
    print(name + 'hello')


if __name__ == '__main__':
    start = time.time()
    threading_main()
    end = time.time()
    print(f'run time is {end-start}')
