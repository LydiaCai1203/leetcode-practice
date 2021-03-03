# 16 章 协程

*协程是指一个过程，这个过程与调用方写作，产生由调用方提供的值。yield 视为控制流程的方式，协程可以把控制器让步给中心调度程序，从而激活其他的协程。*

### 16.1 生成器如何进化为协程的

**用作协程的生成器的基本行为**

```python
# send: 生成器调用方调用 send() 发送数据，该数据会称为生成器函数中 yield 表达式的值
# throw: 让调用方抛出异常，在生成器中处理
# close: 中止生成器
def simple_coroutine():
    print('coroutine started...')
    x = yield 3
    print('coroutine received...', x)

my_cro = simple_coroutine()                           # GEN_CREATED
next(my_cro)      # yield 3                             GEN_SUSPENDED
my_cro.send(42)   # x=42, 然后抛出 StopIteration 异常     GEN_CLOSED
```

+ 协程可以处于 **`GEN_CREATED(等待开始执行, 协程还未被激活)`**、**`GEN_RUNNING(解释器正在执行，只有在多线程应用中才能看到这种状态)`**、**`GEN_SUSPENDED(在 yield 表达式处暂停)`**、**`GEN_CLOSED(执行结束)`** 四种状态中任意一种状态。可以使用 `inspect.getgeneratorstate()` 来查看协程状态。

+ `next()` 启动生成器，调用以后会在 `yield` 处暂停。也可以使用 `my_cro.send(None)` 也能达到启动的效果。

+ `send()` **会把 42 传给协程**，然后从 yield 处开始往下，协程恢复运行，一直运行到下一个 `yield` 表达式，或者终止。

+ `yield` 在 **表达式右边**，`yield` 的右边没有数据，协程只需从客户那里接收数据。默认产出值是 `None`。2

### 16.2 使用协程计算移动平均值

```python
def average():
    total = 0.0
    count = 0
    average = 0
    while True:
        term = yield average
        total += term
        count += 1
        average = total / count
```

+ 这里的 `yield` 表达式用于暂停执行协程，然后把结果发送给调用方，还用于接收调用方后面发送给协程的值，恢复无限循环。

+ 这样做的好处就是 total 和 count 声明成局部变量就可以了，不许使用闭包属性保持上下文。

### 16.3 预激协程的装饰器

```python
# 使用协程之前需要预激，因此需要先调用 next()
# 为了简化步骤，使用预激协程的装饰器
def functools import wraps

def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return inner
```

+ 使用 `yield from` 调用协程时，会自动预激，但是这与我们写的预激装饰器不兼容。

+ `asyncio.coroutine` 装饰器不会预激协程，可以兼容 `yield from`

### 16.5 终止协程和异常处理

```python
# 未处理的异常会导致协程终止, 比如平均值那个里面使用 send('a') 就会导致异常
# 导致异常协程终止，此时如果试图重新激活协程，会抛出 StopIteration 异常
def DemoException(Exception):
    pass

def demo_exc_handling():
    print('started...')
    while True:
        try:
            x = yield
        except DemoException:
            print('DemoException handled, continuing...')
        else:
            print('received...', x)
    # 这一行代码永远不会执行到
    raise RuntimeError('This line should never run.')

# close 关闭协程
my_coro = demo_exc_handling()
next(my_coro)
my_coro.send(10)
my_coro.close()                      # GEN_CLOSED

# 把 DemoException 传入 my_coro，它会处理，然后继续运行
my_coro = demo_exc_handling()
next(my_coro)
my_coro.send(10)
my_coro.throw(DemoException)         # GEN_SUSPENDED

# 如果传入别的异常，会导致协程终止
my_coro.throw(ZeroDivisionError)     # GEN_CLOSED
```

+ **generator.throw**
  
  ```markdown
  生成器会在 yield 处抛出指定的异常，如果该生成器在内部做了捕获异常和处理，则代码会向前执行直到遇到下一个 yield 表达式。产出的值会成为调用 generator.throw 方法得到的返回值。如果称生气没有处理抛出的异常，异常会向上冒泡，传到调用方的上下文中。
  ```

+ **generator.close**
  
  ```markdown
  生成器会在 yield 处抛出 GeneratorExit 异常，如果生成器没有处理这个异常，或者抛出了 StopIteration 异常。调用方不会报错。如果收到了 GeneratorExit 异常，生成器一定不能产出值，否则解释器会抛出 RuntimeError, 生成器抛出的其他异常会向上冒泡，传给调用方。
  ```

### 16.6 让协程返回值

*Python3.3 引入 yield from 结构的主要原因之一与把异常传入嵌套的协程有关，另一个原因是让协程更方便地返回值。*

```python
from collections import nametuple

result = nametuple('Result', 'count average')

def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return result(count, average)
    

my_coro = average()
next(my_coro)
my_coro.send(10)
my_coro.send(30)
my_coro.send(None)
```

+ `send(None)` 以后会终止循环，导致协程结束，返回结果。生成器会抛出 `StopIteration` 异常对象，该异常对象的 `value` 对象保存着 `return` 的值。

+ `yield from` 结构，解释器会捕获 `StopIteration` 异常，还会把 `value` 的值变成 `yield from` 表达式的值。

### 16.7 yield from

```python
def gen():
    for c in 'AB':
        yield c
    for i in range(1, 3):
        yield i
        
list(gen())
```

```python
# yield from 是全新的语言结构，在生成器中使用 yield from subgen， subgen 会获得控制权，产出的值传给 gen 的调用方。调用方可以直接控制 subgen, 与此同时 gen 会阻塞，等待 subgen 终止。不过 yield from 不能在函数外使用。
def gen():
    yield from 'AB'
    yield from range(1, 3)

list(gen())
```

+ yield from x 对 x 对象做的第一件事情就是调用 iter(x)，从中获取迭代器。

+ yield from 结构的主要功能就是打开双向通道，把最外层的调用方与最内层的子生成器连接起来，这样两者可以直接发送和产出值。也可以直接传入异常，而不用在位于中间的协程中添加大量处理异常的代码。

**yield from 实践**

```python
from collections import namedtuple

result = nametuple('result', 'count average')

# 子生成器
def average():
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield
        if term is None:
            break
        total += term
        count += 1
        average = total / count
    return result(count, average)
    
# 委派生成器
def grouper(result, key):                      # 5
    while True:                                # 6
        result[key] = yield from average()     # 7
        
# 客户端
def main(data):                                # 8
    result = {}
    for key, values in data.items():
        group = grouper(result, key)           # 9
        next(group)                            # 10
        for value in values:
            group.send(value)
        group.send(None)
    print(results)
```

```python
data = {
    "girls;kg": [40.9, 38.5, 44.3],
    "girls;m": [1.6, 1.51, 1.4],
    "boys;kg": [39.0, 40.8, 43.2],
    "boys;m": [1.38, 1.5, 1.32]
}
```

### 16.8  yield from 的意义

```markdown
yield from 的行为：

1. 子生成器产生的值都直接传给委派生成器的调用方
2. 使用 send() 方法发给委派生成器的值都直接传给子生成器。如果 send(None) 则调用子生成器的 __next__()，如果不是 None, 调用子生成器的 send()。如果调用的方法抛出 StopIteration 异常，委派生成器恢复运行。任何其他异常都会向上冒泡，传给委派生成器。
3. yield from 表达式的值是子生成器终止时传给 StopIteration 异常的第一个参数。
4. 生成器退出时，生成器中的 return expr 表达式会触发 StopIteration(expr) 异常退出。
5. 传入委派生成器的异常，除了 GenerationExit 之外，都传给子生成器的 throw()。如果调用 throw() 时抛出 StopIteration 异常，委派生成器会恢复运行。除此之外的异常会向上冒泡。
6. 如果把 GenerationExit 异常传入委派生成器，或者在委派生成器上调用 close()，那么在子生成器上调用 close() 将导致异常抛出，异常会向上冒泡，传给委派生成器。
```



# 17 章：使用 future 处理并发

```markdown
python 3.2 引入了 concurrent.futures 模块，future 指一种对象，表示异步执行的操作。这个概念是 concurrent.futures 模块 和 asyncio 包的基础。
```

### 17.1 网络下载的三种风格

**同步下载(代码略)**

**concurrent.futures 模块下载**

```markdown
concurrent.futures 模块的主要特色是 ThreadPoolExecutor 和 ProcessPoolExecutor 类，这两个类实现的接口能分别在不同的线程或进程中执行可调用的对象。这两个类在内部维护这一个工作线程或者进程池。

ps: 显示一个字符串一般需要刷新 sys.stdout，这样能在一行消息中看到进度，正常情况下，python 遇到换行才会刷新 stdout 缓冲。  
```

```python
import os
from concurrent import futures

import requests

MAX_WORKERS = 20
BASE_DIR = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'

def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)

def get_flag(cc):
    """cc is flag name"""
    url = f'{BASE_DIR}/{cc}/{cc}.gif'
    resp = requests.get(url)
    return resp.content

def download_one(cc):
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    return cc
        
def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    # executor.__exit__ 方法会调用 executor.shutdown(wait=True) 方法，它会在所有线程都执行完毕之前阻塞线程。
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(download_one, sorted(cc_list))
    return len(list(res))

if __name__ == '__main__':
    download_many(['CN', 'IN', 'UŚ', 'ID', 'BR'])
```

### 17.3 future 在哪里

```markdown
concurrent.futures.Future 和 asyncio.Future 两个类的作用相同，其实例均表示可能已经完成或者尚未完成的延迟计算。Future 封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果(或抛出异常)后可以获取结果(异常)。

通常我们不应该自己创建 Future，而是应该由并发框架(concurrent.futures 或 asyncio) 来实例化。Future 表示终将发生的事情，而确定某件事会发生的唯一方式是执行的时间已经排定。因此只有排定把某件事交给 concurrent.futures.Executor 子类处理时，才会创建 concurrent.futures.Future 实例。

客户端代码不应该改变 Future 的状态，并发框架在 Future 表示的延迟计算结束后会改变 Future 的状态，而我们无法控制计算何时结束。

例如：
Executor.submit() 的参数是一个可调用的对象，调用这个方法后会为传入的可调用对象排期，并返回一个 Future。
```

**Executor.submit()**

```python
"""
到目前位置，python 线程受到 GIL 的限制，任何时候都只允许运行一个线程。但是 GIL 几乎对 I/O 密集型处理是无害的。因此我们写的这个并发脚本才会执行地这么快。
"""
from concurrent.futures import ThreadPoolExecutor

def download_many(cc_list):
    with ThreadPoolExecutor(max_workers=3) as executor:
        to_do = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            to_do.append(future)
            print(f'Scheduled, {cc}, {future}')
        results = []
        
        # as_completed 会在 future 运行结束之后产出 future
        for future in futures.as_completed(to_do):
            # future.result() 这个方法不会阻塞
            res = future.result()
            results.append(res)
            
    return len(results)
```

### 17.2 阻塞型 I/O 和 GIL

```markdown
CPython 解释器本身就不是线程安全的，因此才会有 GIL，一次只允许使用一个线程执行 Python 字节码。因此一个 Python 进程通常不能同时使用多个 CPU 核心。这是 CPython 解释器的局限，与 Python 语言本身无关。Jython 和 IronPython 没有这种限制。不过目前最快的解释器 PyPy 是有 GIL 的。

编写 Python 代码是无法控制 GIL 的，但是执行耗时任务时，可以使用一个内置的函数或一个使用 C 语言编写的扩展来释放 GIL。

标准库中所有执行阻塞型 I/O 操作的函数（time.sleep 也会释放 GIL），在等待 OS 返回结果时都会释放 GIL，这意味着 Python 语言在这个层次上可以使用多线程。这也是 I/O 密集型程序不受 GIL 限制的原因。一个 Python 线程在等待网络响应时，阻塞型 I/O 函数会释放 GIL，然后再运行一个线程。

如果需要做 CPU 密集型处理，使用 ProcessPoolExecutor 这个模块就可以绕过 GIL，利用所有可用的 CPU 核心。
```

```python
from concurrent.futures import ProcessPoolExecutor

def download_many(cc_list):
    workers = min(MAX_WORKERS, len(cc_list))
    # 如果不传进程池个数，默认就是 os.cpu_count() 的个数
    # 对于最佳线程个数，要经过测试才知道，取决于做什么事，内存有多少等等
    with ProcessPoolExecutor() as executor:
```

### 17.3 实验 Executor.map 方法

```python
import time
from concurrent.futures import ThreadPoolExecutor

def loiter(n):
    print(time.time())
    time.sleep(n)
    return n * 10

def main():
    executor = ThreadPoolExecutor(max_worker=3)
    results = executor.map(loiter, range(5))
    # 这个 results 是个生成器，所以无论如果这一步都是不会阻塞的
    print(results)
    # 隐式调用 future 的 result() 方法，result 方法会阻塞，直至 future 运行结束
    # 每次迭代都要等待下一个结果做好准备
    for i in results:
        print(i)

>>>>>>>>>>>>> output    
loiter inner: 1614752383.559126
loiter inner: 1614752383.5593019
loiter inner: 1614752383.559463
loiter inner: 1614752383.559544
<generator object Executor.map.<locals>.result_iterator at 0x10b4bf040>
0       >>>>>>>>>> 显然这时候 GIL 锁被释放了s
loiter inner: 1614752384.5598478
10      >>>>>>>>>> 可以看到这里是顺序输出的，第二个结果的输出是等待第一个执行完的
20      >>>>>>>>>> 换成 list(range(1, 5))[::-1], 第一个结果 4s 后输出，后面的结果全部一起输出
30
40 
```

+ Executor.map() 这个函数虽然易于使用，但是由于它是顺序输出的，这个特性导致它可能有用也可能没用。因为我们通常会不管提交的顺序，只要 futures 里面有结果就进行获取。为此最好把 `Executor.submit` 和 `futures.as_completed` 结合起来使用。

+ `Executor.submit()`
  
  + 这个方法可以处理不同的可调用对象和参数，但是 `Executor,map` 只能处理同一个可调用对象。

+ `futures.as_completed()`
  
  + 传给它的 futures 集合可以来自多个 `Executor` 实例。比如一些是 `ThreadPoolExecutor`，另一些是 `ProcessPoolExecutor` 实例创建的。

### 17.5 显示下载进度并且处理错误

```python
def get_flag(img_url):
    resp = requests.get(img_url)
    if resp.status_code != 200:
        resp.raise_for_status()
    return resp.content

def download_one(url):
    try:
        image = get_flag(url)
    except requests.exceptions.HTTPError as exc:
        res = exec.response
        if res.status_code == 404:
            status = HTTPStatus.not_found
            msg = 'not found'
        else:
            raise
    else:
        save_img(image, f'{cc}.gif')
    return status, cc  
```

### 17.6 使用 futures.as_completed 函数

```python
def download_many(cc_list, base_urls):
    with futures.ThreadPoolExecutor(max_workers=4) as executor:
        to_do_map = {}
        for cc in sorted(cc_list):
            future = executor.submit(
                download_one, 
                cc, 
                base_url
            )
            to_do_map[future] = cc
        done_iter = futures.as_complete(to_do_map)
        for future in done_iter:
            try:
                res = future.result()
            except requests.exceptions.HTTPError as exc:
                error_msg = f'HTTP {res.status_code} - {res.reason}'
            except requests.exceptions.ConnectionError as exc:
                error_msg = 'Connection error'
            else:
                error_msg = ''
                status = res.status
            if error_msg:
                status = HTTPStatus.error
```

### 17.7 多线程和多进程的替代方案

```markdown
Python3 废弃了原来的 thread 模块，换成了高级的 threading 模块。如果说 concurrent.futures.ThreadPoolExecutor 类对于作业来说不够灵活，可能要使用 threading 模块中的组件(Thread、Lock、Semaphore等)。比如说使用 queue 模块，创建线程安全的队列，在线程之间传递数据。

对于 CPU 密集型的工作来说，要启动多个进程，规避 GIL，创建多个进程最简单的方式是使用 futures.ProcessPoolExecutor 类，如果场景复杂的化使用更高级的 multiprocessing 模块。multiprocessing 还能解决进程之间的通信问题。！
```

## 18 章：使用 asyncio 包处理并发

**并行**：指一次做多件事

**并发**：指一次处理多件事

asyncio 包，使用时间循环驱动的协程实现并发。是原来的 Tulip(郁金香) 移植过来的，后来改名叫做 asyncio。

### 18.1 线程和协程对比

**线程版本的旋转符号**

```python
import sys
import time
import threading
import itertools


class Signal:
    go = True

def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    # 又学到一招
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        # 这就是出现动画的关键，使用退格符把光标移回来
        write('\x08' * len(status))
        time.sleep(1)
        if not signal.go:
            break
    # 使用空格清除状态信息，把光标移回到开头
    write(' ' * len(status) + '\x08' * len(status))

def slow_function():
    # 释放 GIL, 创建从属线程
    time.sleep(3)
    return 42

def supervisor():
    signal = Signal()
    spinner = threading.Thread(
        target=spin,
        args=('thinking!', signal)
    )    
    spinner.start()
    result = slow_function()
    # Python 没有提供终止线程的 API，这是有意为之的，若想关闭线程，必须给其发送消息
    siganl.go = False
    spinner.join()
    return result

def main():
    result = supervisor()
    print('result', result)
```

**协程版本的旋转符号**

```python
import asyncio
import itertools
import sys

# 打算交给 asyncio 处理的协程要使用该装饰器，不是必须做法
@asyncio.coroutine
def spin(msg, signal):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            # 这样休眠不会阻塞事件循环，会去事件循环里面找其他的协程执行
            yield from asyncio.sleep(.1)
        # spin 苏醒以后会抛出 CancelledError，然后会退出请求
        except asyncio.CancelledError:
            breaks
    write(' ' * len(status) + '\x08' * len(status))

@asyncio.coroutine
def slow_function():
    # slow_function 是一个协程，用休眠假装 IO 操作，使用 yield from 继续执行事件循环。也就是到这里中断，控制权交给主循环，等休眠结束以后会恢复这个协程
    yield from asyncio.sleep(3)
    return 42

@asyncio.coroutine
def supervisor():
    # supervisor 是一个协程，使用 async 排定 spin 协程的运行时间，使用一个 Task 对象包装 spin 协程，并立即返回。
    spinner = asyncio.async(spin('thinking!'))
    print('spinner object:', spinner)
    # 使用 yield from 驱动 slow_function 函数
    result = yield from slow_function()
    # 取消 Task 对象，会在协程当前暂停的 yield 处抛出 asyncio.CancelledError
    # 协程可以捕获这个异常，也可以延迟取消，甚至是拒绝取消
    spinner.cancel()
    return result

def main():
    # 获取事件循环引用
    loop = asyncio.get_event_loop()
    # 驱动 supervisor 协程，让其运行完毕，result 就是这次调用的返回值了
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('result', result)
```

+ 除非想 **阻塞整个主线程**，才当使用 `time.sleep`, 如果只是希望协程把控制权还给主线程，应该使用 `yield from asyncio.sleep`。

+ 使用 `@asyncio.coroutine` 并不是强制要求，但是这样可以在一众函数之中把协程凸显出来，有助于调试。如果还没有从中产出值，协程就被垃圾回收了，就可以发出警告，此外装饰器 **不会预激** 协程。

+ `asyncio.async` 产生的 `asyncio.Task` 对象用于驱动协程。它还可以通过 `loop.create_task` 的方法获取。获取的 `Task` 对象已经排定了运行时间，不需要再显示调用比如 `.start()` 方法进行启动了。

+ `Task` 也是 `Future` 的子类，用于包装协程。这和 `Executor.submit()` 创建 `Future` 实例是一个道理。

```markdown
调度程序任何时候都能中断线程，必须记住保留锁，防止多步操作在执行的过程中中断，防止数据处于无效的状态。协程则会默认做好全方位的保护，以防止中断。使用协程的时候想要交出控制权时，使用 yield 或 yield from 把控制权交还给控制程序，这就是能安全取消协程的原因。协程只能在暂停的 yield 处取消。因此可以处理 CancelledError 异常，执行清理操作。
```

### 18.2 asyncio.Future：故意不阻塞

目前 `asyncio.Future` 与 `concurrent.futures.Future` 类的接口基本一致，实现方式不同，不可以互换。

`asyncio.Future` 的 `.result()` 的特点。

+ 没有参数

+ 不能指定超时时间

+ 调用的时候不会阻塞去等待结果，如果 `Future` 没有运行完毕，就会抛出 `asyncio.InvalidStateError` 异常

`asyncio.Future` 对象的结果通常使用 `yield from` 从中产出结果。

+ `yield from` 不会阻塞事件循环，而是把控制权还给事件循环

+ `yield from` 与 `add_done_callback` 方法处理协程的作用是一样的，延迟的操作结束以后，事件循环不会触发回调对象，而是设置期物的返回值。`yield from` 则在暂停的协程中生成返回值，恢复执行协程。

### 18.2 从 future、任务和协程中产出

如果 foo 是协程函数(调用后返回协程对象)






















































































