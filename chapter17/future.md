## chapter17 使用future处理并发

### 17.1 示例：网络下载的三种风格
##### future是一种对象，表示异步执行的操作，是concurrent.futures模块和asyncio包
##### 题外话：fluent-py看了大半本，越来越觉得，也不要把谁都想得那么不可超越，其实别人也没有我想象中的那么厉害嘛。
[本地配置Nginx]（https://github.com/fluentpython/example-code/tree/master/17-futures-py3.7/countries）
</br>
#### 1. stdout缓冲区的一个小知识点:
```python
import sys

for i in range(5):
    print(i, end=' ')
    sys.stdout.flush()
```
##### print()只有在遇到换行的时候才会刷新stdout，所以当`end=' '`的时候，如果不刷新缓冲区，就会导致12345一起输出到屏幕上。
</br>


### 17.1.2 使用concurrent.futures模块下载
#### 这个是我写的一个例子，感觉书上的例子有点复杂
```python
import time

from concurrent import futures
import requests


def download_one(i):
    print('current thread is:{}'.format(i))
    resp = requests.get('https://www.baidu.com')
    return resp.content


def download_many():
    with futures.ThreadPoolExecutor(5) as executor:                    # 指定threadpool里面最多有几个thread
        res = executor.map(download_one, [i for i in range(20)])       # 如果线程有异常抛出 同样会向上冒泡
    return res


if __name__ == '__main__':
    now = time.time()
    res_gen = download_many()
    
    for res in res_gen:
        # print(res)
        pass
    
    print(time.time() - now)
```
##### 编写并发代码的时候经常把for循环体改成函数以便于并发调用
</br>

### 17.1.3 future在哪里
#### 标准库中有两个名为Future的类，分别是concurrent.futures.Future和asyncio.Future。
#### 这两个类的作用相同，这两个类的实例都表示可能已经完成或者尚未完成的延迟计算。
#### Future实例对象的一些方法简介：
> 1. future封装待完成的操作，可以放入队列，完成的状态可以查询，得到结果（或抛出异常）后可以获取结果（或异常）
> 2. 不论什么时候我们都不应该自己去创建future对象，future对象表示的是一个终将发生的事情，而确定某件事情一定发生就是将执行时间排定，所以future对象应该始终由并发框架来生成。
> 3. 客户端代码也不应该去改变future的状态，因为我们并不知道什么时候执行结束，但是并发框架是知道的。
> 4. 这两种future实例都有.done()，表示事件是否已经开始执行。
> 5. 这两种future实例都有.add_done_callback(),这个方法也只有一个参数，类型是可调用对象，future执行结束以后会调用可调用对象。
> 6. .result()
>> 1. 在执行结束以后调用，在两种实例中都是一样的作用，返回可调用对象的结果或者是异常
>> 2. 在还没有执行结束的时候调用
>>> 1. 对于concurrency.futures.Future的实例来说，调用f.result()会阻塞调用方所在的线程，直到有结果可以返回。此时的result(timeout)有一个参数。
>>> 2. asyncio.Future.result方法并不支持设定超时时间，所以获取结果最好使用yield from的结构，但是对于前者来说不能使用yield from
> 7. executor.map()返回的是一个迭代器，所以在for遍历它的时候，会依次去调用每一个future的.result()来获取返回的结果。
#### 现在换一种方式写一下exectuor.map()
```python
def download_many():
    with futures.ThreadPoolExecutor(5) as executor:
        to_do = []
        for i in range(20):
            # submit 会排定可调用对象的执行时间，然后返回一个future,表示这是一个待执行的操作
            future = exector.submit(download_one, i)
            to_do.append(future)

        results = []
        # as_completed会在future执行结束以后产出future
        for future in futures.as_completed(to_do):
            res = future.result()  # 这个result绝不会阻塞 因为这里的fture对象可以肯定是执行完毕的
            results.append(res)
```
**这里的future对象并不是一个想成，而是待执行的事件，等待有空闲下来的线程出现，然后让该线程去执行它**
**严格来说，由于有GIL（全局解释器锁）的存在，目前测试的并发脚本并不能达到真正意义上的并发，任何时候都只允许运行一个线程，而使用asyncio的脚本实际上也是在单个线程中运行的**
**GIL对IO密集型的处理是无害的，因此是能提高执行速度的**
</br>

### 17.2 阻塞型IO和GIL
#### 1. CPython解释器本身就不是线程安全的，因此才有了GIL,一次只允许有一个线程执行Python字节码，因此，一个Python进程通常不能同时使用多个CPU核心。
#### 2. 我们在编写Python代码的时候通常是没有办法操控GIL的，但是可以使用别的C语言写的脚本来释放GIL，达到提到性能的目的，但是这样会直接增加代码的复杂度，所以没有人这样做。
#### 3. 标准库中所有执行阻塞性IO操作的函数，在等待操作系统返回结果的时候都会释放GIL，所以在这个维度的时候，Python是真正意义上的多线程。
#### 4. IO密集型Python程序也包括了，一个Python主线程在等待网络响应的时候，阻塞型IO函数会释放GIL，再运行一个线程。
#### 5. time.sleep()也会释放GIL
#### 6. 线程要拿到GIL才能运行，会有一个专门ticks进行计数 一旦ticks数值达到100 这个时候释放Gil锁 线程之间开始竞争Gil锁(说明:ticks这个数值可以进行设置来延长或者缩减获得Gil锁的线程使用cpu的时间)
**GIL锁是保证同一时刻只有一个线程能使用到CPU**
**互斥锁是保证多个线程/进程对公共区域进行修改的时候，不会发生数据修改混乱的现象**
</br>
#### 现在解释一下GIL和互斥锁之间的关系
> backgroud: 假设现在有两个线程，分别是thread01, thread02
> 1. 此时thread01拥有GIL和互斥锁，它开始执行并且拥有修改共享资源的权利，此时还没有执行到修改共享资源的地方
> 2. thread01执行到了IO密集的地方，或者说ticks数已经到达100，thread01会让出GIL锁
> 3. 如果是ticks到达100，thread01和thread02会共同竞争GIL，但是如果是因为IO阻塞而让出GIL,此时thread02会拿到GIL
> 4. 假设现在thread02拿到GIL,但是并没有拿到互斥锁，互斥锁还在thread01那里，所以thread02会再次让出GIL
> 5. 这个时候thread01和thread02会重新开始一起公平竞争GIL
##### 总结：
##### 所以说，如果thread执行的代码，即没有IO密集型的操作的时候，使用thread甚至会更加慢一点，因为还需要进行上下文切换，会造成一定时间上的消耗。

### 17.3 使用concurrent.futures模块启动进程
##### 这个模块实现的是真正的并行计算
#### 1. 它使用的ProcessPoolExecutor类把工作分配给多个Python进程，所以如果有CPU密集型处理，就会尽可能调用多个CPU核心，绕开GIL。
#### 2. usage: ` with futures.ProcessPoolExecutor() as executor:`
#### 3. 使用进程的时候一般不会指定进程数，应该是由`os.cpu_count()`返回的CPU内核数来决定的
#### 4. 使用线程的时候必须要执行线程数目，但是线程数目是取决于要做的是什么事情以及可用的内存是多少，最佳线程数需要经过测试才知道
**编译级别上的提速：使用PyPy**
> PyPy是一个独立的解析器，通过即时编译(Just In Time)代码，即避免了通过逐行解释代码，从而提升了执行的速度。它会将编译过的行代码缓存起来以提高执行速度。
> [分析了一下PyPy和CPython的优劣](https://gohom.win/2015/09/03/pypy-use/)
</br>

