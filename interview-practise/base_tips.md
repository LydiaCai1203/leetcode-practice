## REVIEW OF PYTHON

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
    2. 例子一不一样是因为不可变对象的原因，使用的时候注意。

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

------------------
### 6. python中的单下划线和双下划线
```python
class Person(object):
    def __init__(self, name, age):
        self._name = 'caiqj'
        self.__age = 23

person = Person()
print(person._name)
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
### 9. 面向切面编程AOP和装饰器
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
    3. 也就是说，装饰器在import的时候就会被执行了 所以是加载模块的时候就会被执行了
```python
    class Average(object):
        def __init__(self):
            self.items = list()
        def __call__(self, new_value):
            self.items.append(new_value)
            total = sum(self.items)
            return total/len(self.items)
```
    4. items在这里是一个自由变量 闭包就是引用了自由变量的函数
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
        4. 在装饰器内调用被装饰的函数

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
    2. 新式类相比于旧式类，多出很多的内置方法，都是从object那里继承过来的
    3. 这个暂时不看了 感觉点有点多

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

    4. import 方法 做为python中的天然的单例模式，在第一次import的时候会产生.pyc文件，就会生成一个实例，第二次import的时候，
    就直接家在.pyc文件，这就是所谓的import中的单例模式了。

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
    就是每个线程若是想要执行的话 就要拿到这个GIL, 也就是说一个cpu同时只能有一个线程在执行，所以说python里面的多线程是假的。
    
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
