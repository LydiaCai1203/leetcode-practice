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






































































































































