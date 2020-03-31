# 理解 Python asyncio

必须要说的是：这篇文章是以下三篇文章的部分摘抄，如果想看原文章的点击下面的链接查看。

[参考文章-阮一峰-Python 异步编程入门](http://www.ruanyifeng.com/blog/2019/11/python-asyncio.html)

[Python3 asyncio 简介](https://v2.laisky.com/p/asyncio/)

[参考文章-Python-doc-Asynchronous I/O](https://docs.python.org/3.9/library/asyncio-task.html#)

最近没法写博客，有很多郁闷的心情无法写在公开的地方，也不想带给别人。黑哥是个什么样的人我心里已经很清楚了，无止尽地朝我甩锅，我已经受够了。做好本职工作，学好技术，不求人，不靠人。

## 一、Python 异步编程的由来

​        历史上，Python 并不支持专门的异步编程语法，因为不需要。有了 threading 和 multiprocessing，就没有必要一定支持异步了。如果一个线程(或进程)阻塞了，新建其它线程(或进程)就可以了，程序不会卡死。

​        但是，多线程有“线程竞争”的问题，处理起来很复杂，还要涉及加锁。对于简单的异步任务来说，写起来很麻烦。从 Python3.4 引入 asyncio 模块，增加了异步编程。它受到了开发者的欢迎，称为从 Python2 升级到 Python3 的主要理由之一。

## 二、 asyncio 的设计

​        asyncio 模块最大的特点就是，只存在一个线程。

​        由于只有一个线程，就不可能有多个任务同时进行。asyncio 是 "多任务合作" 模式，允许异步任务交出执行权给其他任务，等到其他任务完成，再收回执行权继续往下执行。

​        由于代码的执行权在多个任务之间进行交换，所以看上去好像有多个任务同时运行，其实底层只有一个线程，多个任务分享运行时间。

​        asyncio 模块在单线程上启动一个事件循环(event loop)，时刻监听新进入循环的事件，加以处理，并不断重复这个过程，直到异步任务结束。

```python
import asyncio


async def coroutine_demo():
    r = await coroutine_child_demo()
    print(r)

async def coroutine_child_demo():
    asyncio.sleep(1)
    return 2


if __name__ == '__main__':
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(coroutine_demo())
```

## 三、并发

​        单核 CPU 的性能有其极限，所以我们需要并发来提高性能，但是并发又会导致资源的竞争，所以需要用锁来保护敏感区，但是锁会降低并发度，所以我们需要探索无锁的并发方案。

​        可以使用线程模型来提高并发度，但是每一个线程都需要独立的栈空间，即使不包含任何资源的初始栈空间，也是有大小的，而且栈空间的大小和线程切换的开销成正比，所以我们需要寻找比线程更加轻量的解决方案。

​        为了减少线程的切换，我们可以创建一个等于 CPU 核数的线程池，把需要运算的逻辑放进线程池，把需要运算的逻辑放进线程池，不需要时就拿出来换成其他的任务，保持线程的持续运算而不是切换。

​        为了更好的使用 CPU 的性能，我们应该在任务不再需要 CPU 资源时让其从线程池中退出来(比如等待 I/O 时)，这就需要一种机制，在任务阻塞的时候推出，在资源就绪的时候运行。所以我们将任务抽象为一种用户态的线程(协程，greenthread、coroutine)，当其需要调用阻塞资源时，就在 I/O 调度器里注册一个事件，并让出线程资源给其它协程，当资源就绪时，I/O 调度器会在有空余线程资源时，重新运行这个协程。

​        补充说明一下，在原生线程模型下，如果一个线程调用了阻塞接口（syscall），它也会被操作系统调度，让出 CPU 资源给其他 ready 的线程。 当线程数很多的时候，这就会构成较大的上下文切换开销（栈、寄存器）。使用用户态线程，尽可能的改为调用异步系统接口，然后采用 epoll 等方案监听就绪事件， 由 runtime 中实现的 scheduler 来在用户态根据就绪事件来切换不同的用户线程到同一个系统线程上运行，从操作系统层面来看，一直都是同一个内核线程在运行， 没有任何阻塞发生，所以切换开销极小。

​        需要注意的是，并不是所有的 syscall 都有异步接口，所以即使是在协程环境下，其实有时候还是需要依赖于内核线程， 比如可以看一下 `aiofile` 的实现就是依赖于线程池。这其实也是一个思路，偷懒的时候，可以简单粗暴的用线程池把所有的阻塞任务都封装为 coroutine。

​        用户态线程（下文称之为协程）的设计方案一般有三种（按照用户态线程和系统线程的比例）：

- 1:1：直接使用系统线程，可以利用多核，但是上下文开销大；
- N:1：多协程对应一个线程，节省了上下文开销，缺点是不能利用多核，asyncio 就是这个方案；
- M:N：多协程对应多线程，golang 的方案。

协程的优点在于，这是一种用户态的机制，避免的内核态用户态切换的成本，而且初始栈空间可以设置的很小（Golang 中的 goroutine 仅为 2 KB），这样可以创建比线程更大数量的协程。

### 四、asyncio

#### 1、coroutine

```python
# 创建协程
async def coroutine_demo():
      await asyncio.sleep(2)

print(coroutine_demo())
# <coroutine object coroutine_demo at 0x7fd35c523ca8>
```

​        协程都是非阻塞的，当你调用一个协程时(coroutine_demo)，这个协程程序就被执行了，直到执行到另一个协程(asyncio.sleep)，这时会在 ioloop 里挂起一个事件，然后立刻返回。此时要确保的就是给这个协程足够的时间执行完成，所以继续写完这个脚本。

```python
if __name__ == '__main__':
  # 创建事件循环 ioloop
  ioloop = asyncio.get_event_loop()
  # 启动协程
  coroutine = coroutine_demo()
  # 将其封装为 Future 对象
  future = asyncio.ensure_future(coroutine)
  # 将 Future 对象提交给 ioloop，让其等待该 Future 对象完成就行
  ioloop.run_until_complete(future)future
  print('all done')
```

### 2、Task & Future

​        Future 有点像一个 lazy object，当你调用一个协程时，这个协程会被注册到 ioloop，同时该协程会立刻返回一个 coroutine 对象，然后你可以用 `asyncio.ensure_future` 将其封装为一个 Future 对象。当协程任务结束时，这个 future 对象的状态也会发生变化，可以通过这个 future 对象来获取该任务的结果值(或异常)

```python
future = asyncio.ensure_future(coroutine_demo())
# 任务是否结束
future.done()
# 获取任务的结果，默认会阻塞等待任务结束
future.result(timeout=None)
```

​        目前提到了 coroutine、Task、future，三者关系个人理解为：

+ coroutine 是一个函数，可以用来定义协程
+ Task 就是 future，是 asyncio 中最小的任务单位，asyncio 里的各种调度都是基于 future 来进行的

下面举一些用例：

### 3、调度

​        先简单说一下 asyncio 的使用，首先你需要启动一个主函数，在主函数里你实例化 ioloop，然后在这个 ioloop 里注册任意多的 task，task 也可以注册子 task，之后你可以选择让 ioloop 永久地运行下去，或者运行到最后一个 task 完成为止。

​        首先看一个最简单的案例，请求多个 URL：

```python
urls = [
    'https://httpbin.org/',
    'https://httpbin.org/get',
    'https://httpbin.org/ip',
    'https://httpbin.org/headers',
]

async def crawler():
      async with aiohttp.ClientSession() as session:
          futures = map(asyncio.ensure_future, map(session.get, urls))
        for f in asyncio.as_completed(futures):
              print(await f)
        # 或者写成
        await asyncio.wait(futures)
        for i in futures:
              print(f.result())

if __name_- == '__main__':
      ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asyncio.ensure_future(crawler()))
```

​        上面的例子中可以看到，我们启动了很多 `session.get` 子协程，然后用 `asyncio.ensure_future` 将其封装为 `future` ，然后调用 `as_completed` 方法来监听这一堆子任务，每当有子任务完成时，就会触发 for 循环对结果进行处理。

​        asyncio 里除了 `as_completed` 外，常用的还有 `asyncio.wait(fs, timeout=None, when=ALL_COMPLETED)`。方法就是可以等待多个 `futures`。`when` 参数可以设定等待的模式，可以接受的参数还有：

+ FIRST_COMPLETED: 等待第一个完成
+ FIRST_EXCEPTION: 等待一个异常
+ ALL_COMPLETED: 等待全部完成

### 4、定时任务

```python
ioloop = asyncio.get_event_loop()
# 一段时间以后运行
ioloop.call_later(delay_in_seconds, callback, args)
# 指定时间运行
ioloop.call_at(when, callback, *args)
```

​        ioloop 使用的是自己的事件，可以通过 `ioloop.time()` 获取到 ioloop 当前的事件，所以如果你要用 `call_at` ，你需要计算出相对于 ioloop 的时间，所以其实这个方法没有意义。

### 5、锁

#### 5.1 并发控制

​        协程带来的性能提升非常显著，以至于你需要考虑一个你以前可能从未考虑过的问题：并发控制。对资源的控制也是也是异步编程的难点所在。

​        举个例子，你需要下载100万张图片，你开了20个线程来下载，那么在同一时间的最大并发量就是20，对于服务器而言，最多需要处理20 qps 的请求，对于客户端而言，最多需要在内存里放 20 张图片的数据。但是无论是在很短的事件内向远程发起100万的请求，也可能在内存里挂起100万次请求的数据，这无论对于服务端还是客户端都是难以接受的。

        asyncio 里提供了四种锁。

+ Lock

+ Semaphore

+ Event

+ Condition

        下面介绍一个最常用的案例，然后再逐一介绍这几个锁的区别。

        首先讲一下协程任务的并发控制，asyncio 提供了信号量方法 `asyncio.Semaphore(value=1)` ，这个方法会返回一个信号量，你可以初始化一个信号量后，然后在每次发起请求时都去请求这个信号量，来实现对协程任务数量的控制，比如我们可以通过信号量来控制对服务器的请求并发数。

```python
# initialize semaphore
concurrency_sem = asyncio.Semaphore(50)

async with aoihttp.ClientSession() as session:
    while 1: # 即使是这样写也不用担心并发数爆炸了
        # require semaphore
        # whill be blocked when accesses to 50 concurrency
        async with concurrency_sem:
            async with session.get(url, timeout=10) as resp:
                assert resp.status == 200
```

        信号量可以有效的控制同一时间任务的并发数，但是有时候一些协程任务的执行非常迅速，会导致任务执行返回的数据大量堆积，也就是说我们需要限制任务的处理总量，而不是并发量，这时候就可以采用`asynci.Queue(maxsize=0)` 来进行控制，我们可以通过设定 `maxsize` 来设定队列的总长度，当队列满时，`put` 操作就会被挂起，直到后续逻辑逐渐消化掉了队列里的任务以后，才能继续添加，这样就实现了对任务堆积总量的控制。

        比如说我们可以用 Queue 来限制我读取大文件时，不要一下子把整个文件都读进来，而是读几行就处理几行。

```python
task_q = asyncio.Queue(maxsize=1000)

async def worker_to_process_each_line():
    while not task_q.empty():
        line = await task.get()
        # do something with this line

with open('huge_file_with_many_lines.txt', 'r') as f:
    worker_to_process_each_line()
    for line in f:
        await task_q.put(line)
```

    活用 `Semaphore` 和`Queue`，基本就可以解决绝大部分的并发控制的问题了。

**信号量是什么**

        用于线程同步。简单来说，可以把信号量理解成是带计数器的锁，获取锁时计数器-1，释放锁时，计数器+1。最简单的信号量是一个只有0与1两个值的变量，成为 binary semaphore，而具有多个正数值的信号量被称之为通用信号量。互斥锁可以看成是二值信号量的特例，多值信号量可用于做并发控制。

#### 5.2 Lock

        最简单的互斥锁，其实会用 Semaphore 的话完全不需要用 Lock 了，毕竟 mutex 只是 Semaphore = 1 时的特例。

```python
lock = Lock()
async with lock():
    # ...
```

#### 5.3 Event

        事件锁，不过这个锁有两个状态：set 和 unset，可以调用 evt.wait() 挂起等待，直到这个事件被 set()：

```python
evt = Event()

async def demo():
    await evt.wait()  # wait for set
    print('done)

demo()
print(evt.is_set())
# False

evt.set()  # release evt
# done
```

#### 5.4 Condition

        就像 Semaphore 可以简单理解为带计数器的 Lock，Condition 也可以简单理解为带计数器的 Event。一个 Condition 可以被多个协程等待，然后可以按照需求唤醒指定数量的协程。其实 Condition 是 threading 模块里一直存在的锁，简单介绍一下使用方法，使用 condition 前先获取锁 (async with cond)，这是一个互斥锁，调用 wait() 时会自动的释放锁，针对 condition 的 `notify`、`notify_all、`wait`必须在获取锁后才能操作，否则会抛出`RuntimeError` 错误。

        所以当你 notify 后如果需要立即生效的话，需要退出这个 mutex，并且挂起当前协程等待调度， 其他协程才能顺利的获取 mutex，并且获取到 condition 的信号，执行后续的任务，并在完成后释放锁。

```python
from asyncio import Condition, sleep, get_event_loop, wait, ensure_future


async def workers(cond, i):
    async with cond:  # require lock
        print('worker {} is waiting'.format(i))
        await cond.wait()  # wait for notify and release lock
    print('worker {} done, released'.format(i))

async def main():
    cond = Condition()
    fs = list([ensure_future(workers(cond, i)) for i in range(5)])  # run workers
    await sleep(0.1)
    for i in range(3):
        print('notify {} workers'.format(i))
        async with cond:  # require lock
            cond.notify(i)  # notify
        await sleep(0.1)  # let another coroutine run

    async with cond:
        await sleep(0.5)
        print('notify all')
        cond.notify_all()
    await wait(fs)  # wait all workers done

get_event_loop().run_until_complete(main())

# Output:
# worker 0 is waiting
# worker 1 is waiting
# worker 2 is waiting
# worker 3 is waiting
# worker 4 is waiting
# notify 0 workers
# notify 1 workers
# worker 0 done, released
# notify 2 workers
# worker 1 done, released
# worker 2 done, released
# notify all
# worker 3 done, released
# worker 4 done, released
```

#### 5.6 多进程

        上面提到了，python asyncio 的实现方案是 N:1，所以协程是不能跨核的。为了利用多核，你需要创建多进程程序，并且为每一个进程初始化一个 ioloop。我们可以使用 `concurrent.futures` 里提供的 `ProcessPoolExecutor` 来轻松的实现多进程。

```python
from concurrent.futures import ProcessPoolExecutor, as_completed
from asyncio import get_event_loop, sleep, ensure_future


async def coroutine_demo():
    await sleep(1)

def runner():
    ioloop = get_event_loop()
    future = ensure_future(coroutine_demo())
    ioloop.run_until_complete(future)


def main():
    executor = ProcessPoolExecutor(max_workers=7)  # CPU 数 - 1
    for futu in as_completed([executor.submit(runner) for _ in range(7)]):
        result = futu.result()
        # ...
```

#### 5.7 多线程

        顺便提一下多线程，有时候需要兼容旧代码，你需要调用过去用线程写的程序，或者有些阻塞没法用 asyncio 解决，你只能包一层线程，但是你又希望用 asyncio 的方式来调用，这时候就需要用到 `run_in_executor`。

```python
from concurrent.futures import ThreadPoolExecutor
import time

executor = ThreadPoolExecutor(max_workers=10)
ioloop = get_event_loop()

def something_blocking():
    time.sleep(5)

# 关键代码
ioloop.run_in_executor(executor, something_blocking, *args)
```

        你可以通过 `ioloop.set_default_executor(executor)` 设置好常用的 executor，之后再调用 `run_in_executor(None, somthing_blocking, *args)` 的时候，第一个参数就可以传 `None` 了。

### 实用案例

再贴一个给同事写的批量下载 s3 图片的脚本，这个脚本需要读取一个有一千万行的图片文件地址文件， 然后按照每一行的地址去请求服务器下载文件，所以我做了一次最多读取 1000 行，最多发起 10 个 连接的并发控制：

```python
import os
import asyncio
import datetime

import aiohttp
import aiofiles


async def image_downloader(task_q):
    async with aiohttp.ClientSession() as session:
        while not task_q.empty():
            url = await task_q.get()
            try:
                async with session.get(url, timeout=5) as resp:
                    assert resp.status == 200
                    content = await resp.read()
            except Exception as err:
                print('Error for url {}: {}'.format(url, err))
            else:
                fname = split_fname(url)
                print('{} is ok'.format(fname))
                await save_file(fname, content)

def split_fname(url):
    # do something
    return 'FILENAME_AFTER_PROCESSED'

async def save_file(fname, content):
    async with aiofiles.open(fname, mode='wb') as f:
        await f.write(content)
        
async def produce_tasks(task_q):
    with open('images.txt', 'r') as f:
        for count, image_url in enumerate(f):
            image_url = image_url.strip()

            if os.path.isfile(split_fname(image_url)):
                continue

            await task_q.put(image_url)

async def run():
    task_q = asyncio.Queue(maxsize=1000)
    task_producer = asyncio.ensure_future(produce_tasks(task_q))
    workers = [asyncio.ensure_future(image_downloader(task_q)) for _ in range(10)]
    try:
        await asyncio.wait(workers+[task_producer])
    except Exception as err:
        print(err.msg)

def main():
    print('start at', datetime.datetime.utcnow())
    ioloop = asyncio.get_event_loop()
    ioloop.run_until_complete(asyncio.ensure_future(run()))
    print('end at', datetime.datetime.utcnow())


if __name__ == '__main__':
    main()

```






















































































































