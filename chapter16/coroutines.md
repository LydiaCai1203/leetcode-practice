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
#### 1. 子生成器产出的值可以通过return直接返回给yield from表达式的值，就是本例当中的results[key]的值
#### 2. 使用send()发给委派生成器的值都会直接传给子生成器。如果send(None)，就会调用子生成器的next()，如果不是None,就会调用子生成器的send()，为了优化所产生的意义。
#### 3. 生成器退出时，生成器（子生成器）中的return expr表达式会出发StopIteration(expr)异常抛出
#### 4. yield from表达式产生的值是 子生成器终止时传给StopIteration异常的第一个参数
</br>
#### yield from的另外两个特性和异常与终止相关
#### 5. 传入委派生成器的异常，除了GeneratorExit之外，都传给子生成器的throw()方法，如果调用throw()的时候抛出StopIteration异常，委派生成器会恢复运行，StopIteration之外的异常会向上冒泡，传给委派生成器
#### 6. 如果把GeneratorExit异常传入委派生成器，或者在委派生成器上调用close()，那么在子生成器上调用close()，如果它有的话。 如果调用close()导致异常抛出，那么异常会向上冒泡，传给委派生成器，否则，委派生成器抛出GeneratorExit异常
</br>
##### 还是感觉有点迷糊，但是上述至少解释了为什么抛出StopIteration，但是委派生成器还是在继续运行的现象。


**下面是一个关于解释yield from是如何运作的简化版的例子**
```python
# 题外话，这本书虽然对于某些人来说并没有让他收获到什么东西，但是我看了以后感觉获益匪浅

_i = iter(EXPR)                 # EXPR是任何可迭代的对象
try:
    _y = next(_i)               # 预激生成器，将结果存储在_y中，作为产出的第一个值，_i在这里就是子生成器
except StopIteration as _e:
    _r = _e.value               # 如果捕获了异常，就将异常的value属性赋值给_r,也就是最简单的情况下的返回值RESULT
else:
    # 预激成功以后
    while True:                 # 委派生成器将制作为调用方和子生成器之间的通道
        _s = yield _y           # _y就是子生成器产出的值，_s就是调用方发给委派生成器的值，这个值会转发给子生成器
        try:
            _y = _i.send(_s)
        except StopIteration as _e:
            _r = _e.value
            break
RESULT = _r
```
#### 在生成器内部.throw()和.close()都会触发异常抛出，yield from也是要处理这种情况发生的
#### 下面再解释一遍yield from处理异常和终止的时候的机制：
##### 我感觉还是没有说清楚，所以这个yield from的实现机制还是需要再仔细看看
> 1. 当出现关闭委派生成器或者是子生成器的时候会抛出GeneratorExit异常，异常在yield from中就会被捕获，首先去关闭子生成器。然后在将异常抛出，即异常会向上冒泡。
> 2. 如果调用方是通过.throw()进行异常的传入的时候，会尝试使用子生成器的.throw()进行异常的抛出，然后将异常信息进行保存
> 3. 如果没有异常抛出的话就按照之前的提的优化的部分实现剩下的逻辑。


### 小结
#### 1. 生成器中的return result会抛出StopIteration(result）异常，这样调用方才可以从value属性中获取the result。 但是yield from能够自动处理，666
#### 2. yield from结构中有三个主要的部分：委派生成器、yield from预激活的子生成器，以及通过委派生成器中的yield from表达式架设起来的通道把值发给子生成器，从而驱动整个过程的客户代码。
#### 3. [yield from运行机制详解](http://flupy.org/resources/yield-from.pdf)

![GitHub](https://avatars2.githubusercontent.com/u/3265208?v=3&s=100 "GitHub,Social Coding")