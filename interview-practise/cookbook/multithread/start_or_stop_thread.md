## First Part: 启动或停止线程

------------------------

#### 一、 启动一个线程

```python
import time
from threading import Thread


def countdown(n):
    while n > 0:
        print('In Sub Thread T-minus', n)
        n -= 1
        time.sleep(2)


if __name__ == "__main__":
    t = Thread(target=countdown, args=(10, ))
    t.start()
    # 将子线程的加入到当前线程 当前线程会等待子线程结束
    # t.join()
    print(f"main thread is alive：{t.is_alive()}")
```

+ Python 中的线程会在一个单独的系统级线程中进行，这些系统由操作系统全权管理。线程一旦启动，将独立执行，直到目标函数返回。
  
  -----------------------------

#### 二、 Python 解释器直到所有的线程终止前仍会保持运行，对于需要长时间运行的线程，或者需要一直运行的后台任务，应当考虑使用后台线程。

```python
# 只需要在创建线程的时候指定 deamon=True
t = Thread(target=countdown, args=(10, ), daemon=True)
t.start()
```

+ 后台线程无法等待

+ 后台线程会在主线程终止时自动销毁

-------------------------------

### 三、如果你需要终止线程，那么这个线程必须通过编程在某个特定点轮询来退出。

```python
import time
from threading import Thread


class CountdownTask(object):
    def __init__(self):
        self.__running = True

    def terminate(self):
        self.__running = False

    def run(self, n):
        while self.__running and n > 0:
            print('T-minus', n)
            n -= 1
            time.sleep(2)


if __name__ == "__main__":
    c = CountdownTask()
    t = Thread(target=c.run, args=(10, ))
    t.start()
    # t.join()
    c.terminate()
    t.join()
```

+ t.join() 出现的位置决定什么是主线程还是子线程拥有当前 CPU 的控制权

+ 如果线程执行的是 I/O 这样的阻塞操作，通过轮询来终止线程就会使得线程之间的协调变得非常棘手。如果一个线程一直阻塞在一个 I/O 操作上，它就会永远无法返回，也就无法检查自己是否已经被结束了。应该使用超时循环来小心操作线程。（这个例子暂时没看懂 先不写出来了）

--------------------------------------------

#### 四、GIL

由于全剧解释锁的原因，Python 的线程被限制到 同一时刻 只允许 一个线程执行这样一个执行模型。所以Python的线程更适用于处理I/O和其他需要并发执行的阻塞操作(比如等待I/O、等待从数据库中获取数据等等)，而不是需要多处理器并行的计算密集型任务。
