## chapter16 coroutines

#### 在协程中，yield理解为是控制流程的工具

### 16.1 生成器如何进化为协程的
#### 协程是指一个过程，这个过程与调用方进行协作，产出由调用方提供的值

### 16.2 用作协程的生成器的基本行为
```python
def simple_coroutine():
    print('->coroutine started')
    x = yield
    print('->coroutine received x:', x)

my_coro = simple_coroutine()        # my_coro这个东西首先是一个生成器
print(my_coro) 
next(my_coro)
my_coro.send(42)
```
> 1. yield在表达式中使用，通常出现在表达式的右边，可以产出值，也可以不产出值，如果yield表达式后面没有表达式，生成器产出None，协程可能会从调用方接收数据，
> 2. 调用方把数据提供给协程使用的是.send(x)方法，而不是next()函数，通常调用方还是会把值推送给协程
> 3. yield在本例中就是右边没有表达式的情况
> 4. send()的参数会成为暂停的yield表达式的值，只有当协程处于暂停状态时才能调用send方法
> 5. 如果协程没有被激活，也始终需要使用next()进行激活,直接调用`my_coro.send(None)`也是一样的效果, send(non-none)就会报错啦，是不一样的情况
</br>
```python
import inspect

inspect.getgeneratorstate(my_coro)     # 用来查看当前生成器的状态
```
</br>

##### 现在看一个其它的例子 
```python
def simple_coroutine(a):
    print('->a:', a)
    b = yield a
    print('->b:', b)
    c = yield a + b
    print('->c:', c)

my_coro = simple_coroutine(2)
value0 = my_coro.send(None)                # ->a:2 value0=2
value1 = my_coro.send(3)                   # ->b:3 value1=5
value2 = my_coro.send(6)                   # ->c:6 value2=exception
```
> 1. 协程在yield关键字所在的位置停止执行
> 2. 在赋值语句中，右边的表达式会优先执行，所以会yield a 也就是生成a值，然后就停止了
> 3. 等到客户端再次调用.send()的时候协程被激活,b此时会被赋值
> 4. 有人和我一样觉得这个特性很神奇吗。。。。。。
</br>
</br>

### 16.3 示例：使用协程计算移动平均值
```python 
def average():
    total = 0.0
    count = 0
    average = None
    while True:
        x = yield average
        total += x
        count += 1
        average = total/count

obj = average()
next(obj)
average_value = obj.send(5)      # 5.0
average_value = obj.send(6)      # 5.5
```
**当且仅当调用方在协程上调用.close()的时候，或者已经没有对协程的引用了，导致协程被垃圾回收程序回收；额。这个协程才会终止**

### 16.4 预激协程的装饰器
##### 如果不预先激活协程，那么协程也没有用，为了简化协程的用法，会使用一个预激程序
```python
from functools import wraps
def pre_activate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        obj = func(*args, **kwargs)
        next(obj)
        return obj
    return wrapper

@pre_activate
def average():
    pass
```
> 1. average = pre_activate(average)  相当于 average = wrapper
> 2. average = origin_average + next(obj) 
</br>
</br>

### 16.5 终止协程和异常处理
> 1. 在上个例子中，如果你使用的是s=obj.send('1234')就会导致协程发生异常然后中止，所以可以设定某一个值作为哨符来让协程终止的
> 2. generator.throw(exx_type, exc_value, traceback)
> 3. generator.close()
```python
class SampleException:
    pass

def sample_exc_handling():
    print('->coroutine started')
    while True:
        try:
            x = yield
        except SampleException:
            print('meet sample exception already')
        else:
            print('coroutine meet x:', x)
    raise ValueError('This line should never be run')
```
> 1. obj.send(sample_exc)也不会导致协程异常中止
> 2. obj.throw(sample_exc)才会让协程正确捕获异常
> 3. obj.throw(ZeroDivisionError)会让协程无法处理而异常跳出，协程此时的状态就会变为closed
</br>
</br>

### 16.6 让协程返回值

```python 
from collections import namedtuple
Result = namedtuple('Result', 'count average')

def average():
    total = 0.0
    count = 0
    average = None
    while True:
        x = yield average
        if not x:
            break
        total += x
        count += 1
        average = total/count
    return Result(count, average)

obj = average()
next(obj)
obj.send(5)
obj.send(6)
obj.send(None)
```
> 1. 返回result实例的时候也会抛出StopIteration异常
> 2. return 的值会作为抛出异常的实例值
##### 看下面的代码可以发现return的值走到哪里了
```python
try:
    obj.send(None)
except StopIteration as exec:
    result = exec.value
print(result)
```
</br>
</br>

### 16.7 使用yield from

#### example1
```python
def gen():
    for i in 'AB':
        yield i
    for j in range(1, 3):
        yield j
list(gen())

# 下面的这种实现方式将与上面的这种实现方式一致

def gen():
    yield from 'AB'
    yield from range(1, 3)
list(gen())
```
</br>
#### example2
```python
def chain(*iterables):
    for it in iterables:
    yield from it

s = 'asd'
t = tuple(range(3))
list(chain(s, t))
```
</br>
##### yield from x 表达式对x对象所做的第一件事就是：
> 1. 调用iter(x)， 从中获取迭代器，因此x可以是任何可迭代的对象
**yield from 的主要功能是打开双向通道，把最外层的调用方和最内层的子生成器连接起来，这样二者可以直接发送和产生值**
```python
from collections import namedtuple

Result = namedtuple('Result', 'count average')

def average():
    total = 0.0
    count = 0
    average = None
    while True:
        x = yield average
        if not x:
        break
        total += x
        count += 1
        average = total/count
    return Result(count, average)

# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from average()

# usage
results = {}
grouper_gen = grouper(results, 'test')
next(grouper_gen)
grouper_gen.send(5)
grouper_gen.send(6)
grouper_gen.send(None)
print(results)
```
> 1. 返回的Result对象会成为grouper函数中yield from的值
> 2. grouper 是委派生成器
> 3. grouper中每一次的循环迭代时都会新建一个average的实例，每个实例都是作为协程使用的生成器对象
> 4. grouper发送的每一个值都会通过管道传给average实例，然后等待实例回传值，while会不断创建更多的实例，处理更多的值
> 5. 还是有点不太明白 调用方难道不是本来就能给生成器传值的吗 为什么专门要一个委派生成器？？？

**委派生成器相当于管道，可以把任意两个委派生成器连接在一起**
</br>
</br>

### 16.8 yield from 的意义
#### 1. 子生成器产出的值都可以直接传给委派生成器的调用方
#### 2. 
