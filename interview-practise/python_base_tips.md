## REVIEW OF PYTHON（阿菜2019年自制面经）

------------
### 1. 在Python中，string、tuiple、number都是不可更改的对象。list和dict和set都是可更改的对象。

```python
a = 1
print(id(a))
def func(a):
    print('address of var a:', id(a))
    a = 2
    print('address of var a:', id(a))
    print('address of const 2', id(2))
func(a)
print('value of var a:', a, 'address of a:', id(a))
```
    在我学习C++的时候。函数的参数传递存在两种方式，分别是值传递和引用传递，值传递的时候，
    
    1. 但是c++和python中的引用传值都是不一样的，在python中一切都是对象，所有东西都是引用，这里a是一个指向常量1所在的内存地址的引用，也就是说在python中都是引用传递。
    
    2. 但是python里的引用传递并不是c++里的引用传递，在python中，不可变对象的引用传递是会在函数内部创建新的引用的。但是可变对象的引用传递是不会在函数内部创建新的引用的。所以在修改可变对象的时候要尤其小心一点。

-------------
### 2. @staticmethod 和 @classmethod
```python
class Student(object):
    def __init__(self, a, b):
        pass
    
    @classmethod
    def func1(cls, a, b):
        pass

    @staticmethod
    def func2(a, b):
        pass
    
    def func3(self, a, b):
        pass
```
    1. 在python中有类方法一共有三种，分别是实例方法。静态方法和类方法
    2. 实例方法中的self, 表示的是具体的实例本身; 类方法中的cls表示的是这个类本身；self和cls都是，可以取别的名字，但是第一个位置就是self和cls的。
    3. 实例方法的调用离不开实例，类方法离不开类；student.func3(arg1, arg2)；Student.func1(arg1, arg2); 静态方法其实和普通的方法一样并没有什么区别，只不过在调用的时候需要使用student.func3(arg1, arg2)。

-----------------------
### 3. 类变量和实例变量
```python
class Person(object):
    name = 'Stranger'
p1 = Person()
p2 = Person()
p1.name = 'caiqj'
print(p1.name, p2.name)
```
```python
class Person(object):
    name = []
p1 = Person()
p2 = Person()
p1.name.append('caiqj')
print(p1.name, p2.name)
```
    1. p1.name 实际上用的是Person的类变量。实例变量就是属于一个实例的，类变量就是属于类的。
    2. 例子一 不一样是因为不可变对象的原因，使用的时候注意。

--------------
### 4. python的自省机制
    1. 检查某些事物以确定它是什么、它知道什么以及它能做什么。
    2. 在python shell中输入help()，然后就可以键入keywords查看python支持哪些关键字了。

##### 4.1 sys
    1. sys.executable 查看当前的python解释器的路径
    2. sys.platform 查看当前程序所运行的os
    3. sys.argv 第一个参数是脚本所在的执行路径 第二个 第三个参数才是传入脚本的参数
    4. sys.path 是模块搜索的路径

##### 4.2 keywords
    1. 让我们返回到关于 Python 关键字的问题。尽管帮助向我们显示了关键字列表，但事实证明一些帮助信息是硬编码的。关键字列表恰好是硬编码的，但毕竟它的自省程度不深。

##### 4.3 dir()
    1. dir()接受传入对象，然后以列表的形式返回该对象的所有成员。如果什么参数都不传的话，返回的就是当前作用域里面的所有东西。
    2. dir() 可以查看到这样的一个模块 ： __builtins__；但是这个模块是解释自己创建的，在物理磁盘上是找不到的。
    3. hasattr(Person, 'name')   # True
    4. getattr(Person, 'name')   # 返回类对象的值 写函数名字也是可以的 如果不存在的话就会报错
    5. issubclass(SuperHero, Person) # 判断是不是子类

##### 4.4 文档字符串
    1. 所有对象的第一行注释 作为这个对象的__doc__的值
    2. int('0b101', base=2)    # base是使用的是什么进制进行转换 这里必须写2进制，因为’0b‘已经标示了；

##### 4.5 type、 isinstance、id(object)、object.__dict__
    1. type 返回的是变量的类型，但是istance不仅可以判断1是不是int类型，它还可以判断1是不是int的继承类的实例
    2. id可以查看引用所指向的内存地址
    3. __dict__可以查看一个类的所有的自定义所建造的属性

##### 4.6 callable() 可以判断对象是否是可调用的

-----------------
### 5. 字典推导式
```python
name = ['caiqj', 'jx']
age = [22, 23]
print({
    n, a for n, a in zip(name, age)
})
```

扩展： 如果把{}换成()的话 得到的就是一个生成器啦。

------------------
### 6. python中的单下划线和双下划线
```python
class Person(object):
    def __init__(self, name, age):
        self._name = 'caiqj'
        self.__age = 23

person = Person()
print(person._name)   # 可以访问 这个只是人为约定的
print(person.__age)   # 这样直接访问是访问不到的
```
----------------------
### 7. 可迭代对象、迭代器和生成器
    1. 所有的生成器都是迭代器 因为生成器都实现了迭代器的接口
    2. 如果一个对象实现了__iter__(), 解释器需要迭代的时候就会使用iter(obj)，返回的就是一个迭代器
    3. 如果没有__iter__()，但是实现了__getitem__()的话，就会调用__getitem__()返回一个迭代器。
    4. 标准的迭代器接口需要实现两个函数，分别是__next__()和__iter__()
```python 
mystr = '123456789'
myiter = iter(mystr)
while True:
    try:
        print(next(myiter))
    except StopIterator as e:
        del myiter
        break
```
    5. 迭代器模式：就是可以用于顺序访问集合对象的元素，而不需要知道对象的内部表示
    6. 只要有yield的函数就会返回一个生成器
    6. for循环会捕捉异常 所以没有异常抛出
    7. http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python

-----------------------
### 8. *args, **kwargs
    1. *args 必须在 **kwargs前面

------------------------
### 9. 面向切面编程AOP和装饰器(非常极其重要，必须理解透彻)
    1. 能把装饰的函数替换成其它的函数
    2. 能在加载模块的时候就立即执行
```python
    register = []
    def record(func):
        print('enter record and before inner')
        def inner():
            print('enter inner func')
            register.append(func.__name__)
        return inner
    
    @record
    def func1():
        print('enter func1')
        
    @record
    def func2():
        print('enter func2')
```
    3. 也就是说，装饰器在import的时候就会被执行了
```python
    class Average(object):
        def __init__(self):
            self.items = list()
        def __call__(self, new_value):
            self.items.append(new_value)
            total = sum(self.items)
            return total/len(self.items)
```
    4. items在这里是一个自由变量 闭包就是引用了自由变量的函数
    5. 其实闭包就是可以通过配置定制不同的函数，大概就是这个意思吧。
```python
    def make_average():
        items = list()
        def inner(new_value):
            items.append(new_value)
            total = sum(items)
            return total / len(items)
        return inner
```
    6. 这里的变量不能赋值的原因就是因为是不可变的变量 所以才会报异常。有一个nonlocal可以定义自由变量 就可以解决问题了
```python
    def make_average():
        items_count = 0
        def inner(new_value):
            items_count += 1
        return inner
```
```python
    def make_average():
        items_count = 0
        def inner(new_value):
            nonlocal items_count
            items_count += 1
            return items_count
        return inner
```

    7，面试题：他让我写一个装饰器，可以捕获所装饰的函数所产生的异常，捕获到异常以后继续执行，如果产生三次异常就终止运行这个函数
```python

from functools import wraps
def retry_and_throw(func):
    times = 0
    @wraps(func)
    def inner(*args, **kwargs):
        nonlocal times
        while True:
            times += 1
            if times > 3:
                break
            else:
                try:
                    print('try')
                    func(*args, **kwargs)
                except Exception as e:
                    print('catch')
                    continue
                else:
                    print('no exception')
                    break
        return func(*args, **kwargs)
    return inner

@retry_and_throw
def func(*args, **kwargs):
    raise Exception
```
    这道题的知识点有很多：
        1. functools.wraps；
        2. nonlocal； 这道题如果times是一个可变的对象，就不需要nonlocal加持了 
        3. 必包和自由变量 
      * 4. 在装饰器里面 调用 所装饰的函数；直接使用func(*args, **kwargs)
```python
8. 写一个可以记录执行时间的装饰器，装饰器几乎是面试的必考题
```

```python
import time
from functools import wraps
def record_runtime(func):
    @wraps(func)
    def inner(*args, **kwargs):
        from_time = time.time()
        func(*args, **kwargs)
        print(time.time() - from_time)
        return func(*args, **kwargs)
    return inner
```
------------------------
### 10. 鸭子类型
    1. python中的鸭子类型的意思就是，不管它是什么，只要这个东西看上去像鸭子，走起来也像鸭子，就认为这个东西是个鸭子。
    2. 所以说如果一个对象它实现了__iter__()、__getitem__()什么的，就是可迭代的,就可以用在for in 里面。

------------------------
### 11. python 中的重载
    1. 函数的重载是为了解决可变的参数类型 和 可变的参数个数；并且在函数的功能是一样的前提下，才会使用函数的重载。
    2. 对于函数功能相同，但是参数类型不同，python根本不需要处理，因为python本身就可以接受不同类型的参数
    3. 对于函数功能相同，但是参数个数不同，可以使用defalu args 和 mult-args两种方式
    4. 所以python并不需要函数重载

------------------------
### 12. 新式类和旧式类
    1. 新式类： class Base(object); 旧式类： class Base；
    2. 新式类相比于旧式类，多出很多的内置方法，都是从object那里继承过来的 好像旧式类里面是没有__new__这个类方法的
    3. 新式类在继承上还使用了C3算法，有一个__mro__属性，里面是继承类的顺序列表

-------------------------
### 13. __new__ 和 __init__
    1. __new__是一个静态方法，也就是说和普通的方法其实没有什么区别，但是__init__是一个实例方法
    2. __new__会返回一个已经创建了的实例，但是__init__什么都不会返回
    3. 只有当__new__返回一个cls实例以后，才会调用__init__
    4. __new__静态方法的第一个参数是要实例化的类
    5. __metaclass__是在创建类的时候起作用，和__new__还有__init__是对创建实例起作用的

-------------------------
### 14. 单例模式
```python 
class BaseClass(object):
    def add(self, x):
        return x + 1
class SubClass(object):
    def add(self, x):
        x = super().add(x)
        return x + 1
obj = SubClass()
obj.add(1)               # 在调用的时候回先进入SubClass的add，然后进入BaseClass的add
```
    1. 使用__new__方法
```python 
class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_isinstance'):
            print('还没有创建实例')
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
obj = Singleton()
obj1 = Singleton()
print(id(obj), id(obj))
```
    1.1 这样写 是线程不安全的 所以改进版就是加上双重锁
    1.1.2 其实 不用加上双重锁也是可以的 只要保证两个线程不会同时进入__new__里面就可以了，但是这样所有实例的时候都需要锁才能进入__new__了
    所以说，这样的话对于多线程来说，效率太低了。因此使用双重锁，先用if判断一下，如果已经有实例的话，就不用进入同步的状态了。
```python 
# 要注意写法 Singleton.lock.acquire() 
# 用完的时候还要释放锁 Singleton.lock.release()
import threading
class Singleton:
    lock = threading.Lock()
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            print('还没有创建实例')
            with cls.lock:
                if not hasattr(cls, *args, **kwargs):
                    cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
```

    2. 共享属性，就是在创建实例的时候，将所有的实例的__dict__都指向同一个dict，让他们共享属性
```python
class Singleton(object):
    _state = {}
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._state
        return obj
```
    2.1 但是我并不认为这个是真正意义上的单例模式，毕竟实际上确实产生了多个对象，只不过__dict__是共享的
    
    3. 装饰器形式 装饰类的装饰器; 网上还有人在getinstance里面return instance这个dict，我真的搞不懂他是想干嘛
```python 
from functools import wraps
def singleton(cls):
    instance = {}
    @wraps(cls)
    def getinstance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
    return getinstance
```

    4. import 方法 做为python中的天然的单例模式，在第一次import的时候会产生.pyc文件，就会生成一个实例，第二次import的时候，就直接加在.pyc文件，这就是所谓的import中的单例模式了。

-----------------------
### 15. python中的作用域
    当python遇到一个变量的话 会按照这样的顺序在在作用域中进行变量的搜索。
    1. 本地作用域
    2. 当前作用域被嵌入的本地作用域
    3. 全局、模块作用域
    4. 内置作用域
    
    Local: 在def创建的语句块中，每当函数被调用的时候都会创建一个新的局部作用域，在函数内部的变量声明，除非特别声明，都默认为是局部变量。如果需要对全局变量进行赋值，就需要使用global进行声明。
    
    Enclosing: E也是包含在L中的，表示的是在L的上一层函数中的局部变量域，主要是为了实现python的闭包
    
    Global: 在模块层次中定义的变量，每个模块都是一个全局作用域，仅存在于单个的模块文件当中
    
    Buildin: 系统内固定模块里定义的变量

-------------------------
### 16. GIL全局锁（全局解释器锁）
    就是每个线程若是想要执行的话 就要拿到这个GIL, 也就是说一个cpu同时只能有一个线程在执行，所以说python里面的多线程是假的，意思就是因为只有一个GIL。
    
    1. py2的逻辑当中，GIL的释放逻辑就是，当前线程遇到IO操作的时候，或者说ticks的数目达到100的时候，就进行释放。这个东西每次释放以后就会归零。
    
    2. py3的逻辑当中，GIL不再使用计数器，而是使用计时器，执行时间达到阈值以后，GIL就会释放锁，这样对CPU密集型的程序会更加的友好。
    
    3. 当GIL释放以后，线程都会进行锁竞争，切换线程，会消耗资源。

#### 16.1. 那么是不是python的多线程就一点用处都没有了呢？
    1. 对于CPU密集型的，ticks会很快就到达阈值，所以会频繁释放锁，所以对这种代码不友好。
    2. 对于IO密集型的，比如文件操作或者是网络爬虫，多线程能够有效提升效率。这里应该去了解ticks计时是怎么计时的，为什么面对CPU密集型的代码，会比较快达到阈值。py2的说法的话，ticks是计算的次数，所以比较快达到阈值我是可以理解的，但是计时器的说法，我比较不能理解了，这样对IO密集型的代码会比较友好吗？
#### 16.2 多核多线程 比 单核多线程的效果 更加差劲。一个CPU上只有一个GIL,其它的核上的线程也会进行竞争，但是GIL可能又回马上被线程0抢到，导致其它几个核上的线程会醒着等待到切换时间后又马上进入调度状态，这样会导致线程颠簸，比较浪费资源。
    这里的意思我还不是很了解就对了。还有点疑问。这里可能要回去复习操作系统相关的知识了。

#### 16.3 每个进程都有一个单独的GIL,这样就可以进行真正意义上的并行执行。

---------------------------
### 17. 进程和线程的区别（面试两次都被问到的问题）

[参考 你知道堆和栈的区别吗](https://blog.csdn.net/echoisland/article/details/6403763)

    1. 线程是程序执行时候的最小单位，进程是资源分配时候的最小单位。
    2. 进程有自己独立的地址空间，每启动一个进程，系统就会为其分配地址空间，建立数据表来维护代码段，堆栈段，和数据段，这种操作非常的昂贵。
    3. 线程是共享进程中的数据的，使用相同的地址空间，因此CPU切换一个线程的花费远远比进程要小的多。同时创建一个线程的开销比创建一个进程的开销也要小的多。
    4. 线程之间的通信也非常方便，同一个进程下的线程共享全局变量，静态变量等数据。但是进程间的通信需要通过IPC的方式进行。
    5. 多进程程序会更加健壮，多线程程序只要有一个线程死掉了，整个进程也就死掉了，但是一个进程死掉了不会对其它的进程造成影响，因为进程有自己独立的地址空间。
    
    这样的回答我还是觉得很不好 所以还是要回去复习os才行

----------------------------
### 18. 协程
    1. 进程和线程都面临着用户态到内核态的切换，切换是需要切换时间的，协程是程序主动控制去切换的，没有线程切换的开销。

----------------------------
### 19. 闭包
    1. 必须有一个内嵌函数
    2. 内嵌函数必须引用的外部函数中的变量
    3. 外部函数的返回值必须是内部函数，
    4. 反正说的还是很模糊就对了。

----------------------------
### 20. lambda函数
```python
# 感觉就是冒号的左边就是传入的参数 右边就是函数体的感觉 
 g = lambda x:x+1
 g(1)
```

----------------------------
### 21. filter map reduce
```python
foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]
filter(lambda x: x % 3 == 0, foo)
map(lambda x: x * 2 + 10, foo)
reduce(lambda x, y: x + y, foo)
```

----------------------------
### 22. python里的拷贝
```python
import copy
a = [1, 2, 3, ['a', 'b', 'c']]
b = a    # 这个比较简单 就不做举例了
c = copy.copy(a)
d = copy.deepcopy(a)

c.append(5)
print(c)
print(a)
# 输出:
[1, 2, 3, ['a', 'b', 'c'], 5]
[1, 2, 3, ['a', 'b', 'c']]

c[3].append('d')
print(c)
print(a)
# 输出
1, 2, 3, ['a', 'b', 'c', 'd'], 5]
[1, 2, 3, ['a', 'b', 'c', 'd']]

d[3].append('e')
print(d)
print(a)
# 输出
[1, 2, 3, ['a', 'b', 'c', 'e']]
[1, 2, 3, ['a', 'b', 'c', 'd']]
```

-------------------------------
### 23. python里的垃圾回收机制
Python GC主要使用的是引用计数机制来跟踪和回收垃圾，在引用计数的基础上采用”标记-清除“的方式来解决容器对象可能产生的循环引用的问题，通过“分代回收”以空间换时间的方式提高垃圾回收效率。
#### 23.1 引用计数机制
    PyObject是每个对象必有的内容，其中ob_refcnt就是做为引用计数。当一个对象有新的引用时，它的ob_refcnt就会增加，当引用它的对象被删除，它的ob_refcnt就会减少.引用计数为0时，该对象生命就结束了。
    
    缺点：
    1. 循环引用计数浪费资源
    2. 循环引用
```python
a = [1, 2]
b = [3, 4]
a.append(b)
b.append(a)

del a
del b
```
    # a所指向的对象 与 b所指向的对象 引用计数都为2，del a 与 del b 以后，两个对象的引用计数还是1，就相当于永远不会被释放删除。

#### 23.2 标记-清除
    基本思路是先按需分配，等到没有空闲内存的时候从寄存器和程序栈上的引用出发，遍历以对象为节点、以引用为边构成的图，把所有可以访问到的对象打上标记，然后清扫一遍内存空间，把所有没标记的对象释放。
#### 23.3 分代计数
    将系统中的所有内存块根据存活时间划分为不同的集合，每个集合就会成为一个“代”。垃圾回收的频率随着“代”存活时间的增大而减小，存活时间通常通过几次垃圾回收来进行衡量。Python默认定义了三代对象集合，索引数越大，对象存活时间越长。
    
    例： 
        当某些内存块M经过了3次垃圾收集的清洗之后还存活时，我们就将内存块M划到一个集合A中去，而新分配的内存都划分到集合B中去。
        当垃圾收集开始工作时，大多数情况都只对集合B进行垃圾回收，而对集合A进行垃圾回收要隔相当长一段时间后才进行，这就使得垃圾收集机制需要处理的内存少了，效率自然就提高了。
        在这个过程中，集合B中的某些内存块由于存活时间长而会被转移到集合A中，当然，集合A中实际上也存在一些垃圾，这些垃圾的回收会因为这种分代的机制而被延迟。

------------------------------------
### 24. python里面如何实现tuple和list的转换
```python
a = [1, 2, 3]
b = tuple(a)
```

------------------------------------
### 25. python里面的is和==
    is比的是地址，==比的是值

------------------------------------
### 26. read、readline、readlines
    1. read读取的是整个文件，返回结果是str
    2. readline使用的是生成器，但是返回结果是str
    3. 读取整个文件到一个迭代器中供我们访问，返回结果是一个str

------------------------------------
### 27. 关于os的几个常用的函数
    1. os.listdir(./)   # 可以列出当前目录下的所有的文件
    2. os.path.join()   # 函数用于路径拼接文件路径 会从第一个/开始的path开始拼接 之前的全部丢弃
    3. os.path.isdir()  # 判断某个路径是不是指向的是一个目录

------------------------------------
### 28. 阅读下面的代码 说出下面各变量的值
```python
A0 = dict(zip(('a','b','c','d','e'),(1,2,3,4,5)))
A1 = range(10)
A2 = [i for i in A1 if i in A0]
A3 = [A0[s] for s in A0]
A4 = [i for i in A1 if i in A3]
A5 = {i:i**i for i in A1}
A6 = [[i,i**i] for i in A1]

A0 = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
A2 = []
A3 = [1, 2, 3, 4, 5]
A4 = [1, 2, 3, 4, 5]
A5 = {0:0, 1:1, 2:4, 3:9, 4:16, 5:25, 6:36, 7:49, 8:64, 9:81}
A6 = [[0, 0], [1, 1], [2, 4], [3, 9], ...]    # 别忘记写0
```

------------------------------------
### 29. 下面的代码会输出什么
```python
def f(x,l=[]):
    for i in range(x):
        l.append(i*i)
        print(l)
f(2)
f(3,[3, 2, 1])
f(3)
```
    1. f(2) 和 f(3, [3, 2, 1]) 的输出都不会写错，但是f(3)的输出就要注意了；
    2. 只要在for前面打印出l的地址 就一目了然了；因为当形参的默认参数是可变对象的时候，只会在定义的时候分配一次内存。之后不管使用几次这个函数，默认值都是一开始定义函数的时候产生的对象。
    3. 所以说f(2)的时候 这个默认值已经变掉了，之后f(3)的时候就会出问题啦！！！！！

-------------------------------------
### 30. 猴子补丁指的是什么？这种做法好吗？
    1. 猴子补丁这种东西充分利用了动态语言的灵活性，可以对现有的Api进行追加，替换，修改Bug，甚至性能优化等等。
```python
 import datetime
 datetime.datetime.now = lambda: datetime.datetime(2012, 12, 12) # 这样返回的就一直是2012-12-12了
```
    2. 这种做法并不是很好 因为函数在代码库中的行为最好保持一致（这个回答简直垃圾，讲的不清不楚的，我要是面试官我都不要你）

--------------------------------------
### 31. 阅读下面的代码 说出输出结果
```python
class A(object):
    def go(self):
        print("go A go!")

    def stop(self):
        print("stop A stop!")

    def pause(self):
        raise Exception("Not Implemented")

class B(A):
    def go(self):
        super(B, self).go()
        print("go B go!")

class C(A):
    def go(self):
        super(C, self).go()
        print("go C go!")

    def stop(self):
        super(C, self).stop()
        print("stop C stop!")

class D(B,C):
    def go(self):
        super(D, self).go()
        print("go D go!")

    def stop(self):
        super(D, self).stop()
        print("stop D stop!")

    def pause(self):
        print("wait D wait!")

class E(B,C): pass

a = A()
b = B()
c = C()
d = D()
e = E()
```
    1. d.go() 这里是先调用的C再调用的B,和继承的先后顺序也是有关系的
```python
# output
go A go!
go C go!
go B go!
go D go!
```
    2. 感觉例子不是很好 但是让我想到了C++里面构造函数和析构函数的调用顺序，我觉得应该按照那样举例子比较好.
    	 这道题在新式类里 和 旧式类 中，执行的结果输出顺序应该是不一样的，在新式类中使用了C3算法，C3算法在后面有做详细解释。

------------------------------
### 32. 阅读下面的代码 说出输出结果是什么
```python
class Node(object):
    def __init__(self,sName):
        self._lChildren = []
        self.sName = sName
    def __repr__(self):
        return "<Node '{}'>".format(self.sName)
    def append(self,*args,**kwargs):
        self._lChildren.append(*args,**kwargs)
    def print_all_1(self):
        print(self)
        for oChild in self._lChildren:
            oChild.print_all_1()
    def print_all_2(self):
        def gen(o):
            lAll = [o,]
            while lAll:
                oNext = lAll.pop(0)
                lAll.extend(oNext._lChildren)
                yield oNext
        for oNode in gen(self):
            print(oNode)

oRoot = Node("root")
oChild1 = Node("child1")
oChild2 = Node("child2")
oChild3 = Node("child3")
oChild4 = Node("child4")
oChild5 = Node("child5")
oChild6 = Node("child6")
oChild7 = Node("child7")
oChild8 = Node("child8")
oChild9 = Node("child9")
oChild10 = Node("child10")

oRoot.append(oChild1)
oRoot.append(oChild2)
oRoot.append(oChild3)
oChild1.append(oChild4)
oChild1.append(oChild5)
oChild2.append(oChild6)
oChild4.append(oChild7)
oChild3.append(oChild8)
oChild3.append(oChild9)
oChild6.append(oChild10)

# 说明下面代码的输出结果

oRoot.print_all_1()
oRoot.print_all_2()
```

```python
oRoot.print_all_1()会打印下面的结果：
<Node 'root'>
<Node 'child1'>
<Node 'child4'>
<Node 'child7'>
<Node 'child5'>
<Node 'child2'>
<Node 'child6'>
<Node 'child10'>
<Node 'child3'>
<Node 'child8'>
<Node 'child9'>

oRoot.print_all_2()会打印下面的结果：
<Node 'root'>
<Node 'child1'>
<Node 'child2'>
<Node 'child3'>
<Node 'child4'>
<Node 'child5'>
<Node 'child6'>
<Node 'child8'>
<Node 'child9'>
<Node 'child7'>
<Node 'child10'>
# 一个是深度优先遍历，一个是广度优先遍历
```

----------------------------------
### 33. 介绍一下except的用法和作用
```python 
try:
    print('enter try')
    raise Exception
except Exception as e:
    print('enter in except')
else:
    print('enter else')
finally:
    print('enter finally')
```
    1. 上面代码的输出结果
```python
enter try
enter in except
enter finally
```
    2. 注释掉raise这一行以后的输出结果
```python
enter try
enter else
enter finally
```

----------------------------------
### 34. python中的pass语句有什么用处
    pass语句并不会执行任何操作，一般用作占位程序使用

----------------------------------
### 35. python里面的match和search有什么区别
    match（）函数只检测RE是不是在string的开始位置匹配， search()会扫描整个string查找匹配, 也就是说match（）只有在0位置匹配成功的话才有返回，如果不是开始位置匹配成功的话，match()就返回none

----------------------------------
### 36. 用Python匹配HTML tag的时候，<.*>和<.*?>有什么区别？
    第一种写法是，尽可能多的匹配，就是匹配到的字符串尽量长，第二中写法是尽可能少的匹配，就是匹配到的字符串尽量短。
    比如<tag>tag>tag>end，第一个会匹配<tag>tag>tag>,第二个会匹配<tag>,如果要匹配到二个 >，就只能自己写了。
    1. .*  连在一起就意味着任意数量的不包含换行的字符
    2. .*? 匹配任意数量的重复，但是在能使整个匹配成功的前提下使用最少的重复

----------------------------------
### 37. Python里面如何生成随机数
    1. 使用random模块，random.randint(start, end, step) 生成随机整数，左闭右开
    2. random.random(), 会返回0-1之间的浮点数
    3. random.uniform(start, end), 会返回某个区间的浮点数

----------------------------------
### 38. 如果想在一个函数里面声明全局变量的话 声明的时候使用global就可以

----------------------------------
### 39. 单引号，双引号，三引号的区别
    1. 如果要换行的话 单引号和双引号都需要使用\n换行，但是三引号就可以直接换行
    2. 如果想在单引号里面使用单引号 需要使用转义字符 'Let\'s go'
    3. 单引号里面可以使用双引号 单引号和双引号其实是等价的

----------------------------------
### 40. 将下面的函数按照执行效率高低排序
```python
[random.random() for i in range(100000)]
def f1(lIn):
    l1 = sorted(lIn)
    l2 = [i for i in l1 if i<0.5]
    return [i*i for i in l2]

def f2(lIn):
    l1 = [i for i in lIn if i<0.5]
    l2 = sorted(l1)
    return [i*i for i in l2]

def f3(lIn):
    l1 = [i*i for i in lIn]
    l2 = sorted(l1)
    return [i for i in l1 if i<(0.5)]

f2 > f1 > f3
```
    1. python里有一个包帮助分析代码的性能
```python
import cProfile
lIn = [random.random() for i in range(100000)]
cProfile.run('f1(lIn)')
cProfile.run('f2(lIn)')
cProfile.run('f3(lIn)')
```
    2. 如果列表较小的话，很明显是先进行排序更快，因此如果你可以在排序前先进行筛选，那通常都是比较好的做法。

-------------------------------------
### 41. 如何使用python来查询和替换一个字符串
    1. re.sub(pattern, repl, string, count)
    2. 其中第二个参数是替换后的字符串
    3. count不给的话，默认是0，代表每个匹配到的都会替换字符

-------------------------------------
### 42. range and xrange
    1. xrange在循环的时候内存性能要比range更加好
    2. 在python2中，range会在内存中生成一个list, 但是xrange不是，是惰性加载的，循环到的时候才生成。

-------------------------------------
### 43. python里的类成员
    这道题，ztz还在cls的时候，考过我。这一次笔试的时候也还是做到了这道题，其实现在想想，他当初确定要走以后，是想过要在最后的时间里面教我一点东西的。其实这道应该和Python函数里面的default arguments放在一起。
```python
class Myclass(object):
    name = []
    def func_1():
        pass
obj1 = MyClass()
obj2 = MyClass()
obj1.name.append('caiqj')
obj2.name.append('jx')
print(obj1.name)
```
    知识点：
        1. class的类变量就是独独一份儿的。如果是不可变的对象，就是每个实例都有一份，如果是可变的对象，就要注意了，这里也有一个大坑在的。

--------------------------------------
### 44. 你知道python2和python3有哪些区别吗
#### 新式类和旧式类
    Python会计算出一个解析顺序列表，可以使用ClassName.__mro__进行查看；为了实现继承，Python会从左到右开始查找基类。当你使用super()的时候，Python会在mro列表上继续搜索下一个类，只要每个重定义的方法都使用过一次super()，mro列表里面的类就会被遍历一遍。
#### 所以什么是C3算法
```python
class A(object): pass
class B(object): pass
class C(object): pass

class E(A, B): pass
class F(B, C): pass
class G(E, F): pass
```
##### className.__mro__ 就可以查看解析类的顺序
```python
# 精髓：所有的[]中，某个在列表中排在第一的，在其他列表中也排在第一的，就merge进来
mro(A) = [A, O]
mro(B) = [B, O]
mro(C) = [C, O]

mro(E) = [E] + merge(mro(A), mro(B), [A, B])
       = [E] + merge([A, O], [B, O], [A, B])
       = [E, A] + merge([O], [B, O], [B])
       = [E, A, B] + merge([O], [O])
       = [E, A, B, O]

mro(F) = [F] + merge(mro(B), mro(C), [B, C])
       = [F] + merge([B, O], [C, O], [B, C])
       = [F, B] + merge([O], [C, O], [C])
       = [F, B, C] + merge([O], [O])
       = [F, B, C, O]

mro(G) = [G] + merge(mro(E), mro(F), [E, F])
       = [G] + merge([E, A, B, O], [F, B, C, O], [E, F])
       = [G, E, A, F, B, C, O]
```

-------------------------------------
### 44. 说一下 1 and 2 和 2 and 1 的结果是什么？
    这个题目的角度真的有点刁钻了，但这确确实实就是基础。
    1 and 2 输出的是 2
    2 and 1 输出的是 1
+ 两个知识点
    + 1. and 运算符的运算规则
    + 2. and 两边的操作数，其实是表达式，结果不是boolean, 而是值

-------------------------------------
### 45. 给你一个字符串，循环100万次，然后将他们拼接起来
    使用 += 或者是 join
+ 两个知识点
    + 1. += 和 join 两个哪个效率高
    + 2. 循环100万次，是放在list里面还是生成器里面？怎么循环，怎么生成？内存不会爆吗？再看！

-------------------------------------
### 46. 写出所有能让字符串倒置的方法
#### method-one：
```python
    'abc'[::-1]
```

#### method-two:
```python
    ''.join(reversed('abc'))
```
#### method-three:
```python
    from collections import deque
    d = deque()
    d.exetendleft('abc')
    ''.join(reversed('abc'))
```
#### method-four:
```python
    使用递归实现
```

-------------------------------------
### 47. 有用过functools和itertools里面的东西吗
    pass

-------------------------------------
### 48. 使用Python自己写测试用例
    好的公司出来的开发人员会比较注重这方面的素养