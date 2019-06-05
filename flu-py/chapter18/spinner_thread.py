import threading
import itertools
import time
import sys


class Singal:
    go = True


def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + '---' + msg
        write(status)
        # 会强行刷新缓冲区，然后将缓冲区的内容都写到终端上，所以我们才能看得见显示的内容
        flush()
        # \x08 就是退格符，这才是出现动画的关键啊
        write('\x08' * len(status))
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    # 假装等待IO一段时间
    time.sleep(3)
    return 42

def supervisor():
    singal = Singal()
    spinner = threading.Thread(
        target=spin,
        args=('thinking!', singal)
        )
    print('spinner object:', spinner)
    spinner.start()

    # 这里的意思就是，主线程执行完一个比较耗时的操作以后，就会设置go为False，然后子线程判断标志就会退出循环
    result = slow_function()
    singal.go = False
    
    # 等待spinner线程结束 相当与等待进度条才显示结果的意思吧
    spinner.join()
    return result

    
def main():
    result = supervisor()
    print('Answer:', result)

if __name__ == '__main__':
    main()