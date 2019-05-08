"""
1. _变量名 用来定义的变量或者是函数名称 在使用from module import * 的时候不会被导入
2. 变量名_ 这种形式通常是用来将变量名与关键词区分开来使用的 比如class_
3. __变量名 作为在python的类成员对象出现，当使用dir(Student)的时候 可以看到我们定义的私有变量名称显示为 '_Student__age' 
4. __变量名__ 作为魔术对象存在 但是官方并不建议这样给自己的对象命名
5. 'aaaaa{}'.format(name) 可以 但是 'aaaaa%s' % name 会出问题 必须使用 'aaaaa%s' % (name,)
6. Generators are iterators, a kind of iterable you can only iterate over once. 
   Generators do not store all the values in memory, they generate the values on the fly.
7. yield is a keyword that is used like return, except the function will return a generator.
8. 生成器的使用适用于：your function will return a huge set of values that you will only need to read once.
9. when you call the function, the code you have written in the function body does not run.
10. 第一次for从函数调用生成器对象时，它将从头开始运行函数中的代码，直到它命中yield，然后它将返回循环的第一个值。然后，每个其他调用
将再次运行您在函数中写入的循环，并返回下一个值，直到没有值返回。
11. import itertools
    horses = [1, 2, 3, 4]
    races = itertools.permutations(horses)
    list(itertools.permutations(horses))
    可以列出races中四个元素排列组合一下的所有情况
12. 一个基本的设计原则是，仅仅当两个函数除了参数类型和参数个数不同以外，其功能是完全相同的，此时才使用函数重载，如果两个函数的功能其实不同，
那么不应当使用重载，而应当使用一个名字不同的函数，这或许是python不提供函数重载的原因。
13. 装饰器的陷阱：
    下面这个装饰器的例子不能单独从标签来看执行顺序，执行顺序还是从上往下执行的
14. 新式类和经典类的区别：
    经典类的写法：
    class B:
        pass
    新式类的写法：
    class C(object):
        pass
15. 新式类是在创建的时候继承内置object对象（或者是从内置类型，如list,dict等），而经典类是直
接声明的。使用dir()方法也可以看出新式类中定义很多新的属性和方法，而经典类好像就2个
16. 其中内置的object对象一般是定义了一系列特殊的方法来实现所有对象的默认行为
    __str__()是为了对象的可读性  __repr__()是为了对象信息的唯一性 所以按照规范来说，每一个类都需要重写一个__repr__()
    __str__()如果没有实现的话  会默认调用__repr__()
17. class A:
        pass
    class A:
        def _init__(self):
            pass
    a = A('caiqj')      # 以上两种类定义方法都会报错

    class A(object):
        pass
    class A(object):
        def __init__(self):
            pass 
    a = A('caiqj')      # 这样使用也会报错的 但是新式类和经典类的报错不一样而已
18. 新式类都有一个__new__的静态方法，原型是object.__new__(cls[,...])
当你调用C(*args, **kwargs)用来创建一个类C的实例时，python内部调用的是C.__new__(*args, **kwargs)
返回值就是类C的实例c，在确认c是C的实例以后，python再调用C.__init__(c, *args, **kwargs)来初始化实例c
    code:
        c = C(2)
        c = C.__new__(C, 2)
        if isinstance(c, C):
            C.__init__(c, 2)   # __init__的第一个参数为实例的对象
19. object.__new__()会创建的一个新的，没有经过初始化的实例，当你重写__new__的时候，不需要加上@staticmethod
解释器会自动判断它为静态方法，如果需要重新绑定，只需要在类外执行, C.__new__ = staticmethod(func)
20. 通常每一个实例都会有一个__dict__属性，用来记录实例中的所有属性和方法
21. 类C拥有比较少的变量时，并且拥有__slot__属性时，它就没有__dict__属性，变量的值存在一个固定的地方
    这样做可以生成小而精的实例，可以节省每一个实例的内存消耗
22. 如果还想在之后添加新的变量就可以在__slots__
23. 类继承中的调用顺序，新的对象模型采用的是从左到右，广度优先的方式。
    这个顺序的实现是通过新式类中特殊的只读属性__mro__，类型是一个元组，保持着解析顺序信息，只能通过类
    来使用，而不能通过实例来使用, classname.__mro__可以显示解析顺序
24. 只有在__new__返回一个cls实例时后面的__init__才能被调用
25. python 中的多线程由于GIL的存在 也就是解释器全局锁的存在，保证解释器中某一个时刻只有一个线程在执行
所以python中的多线程实际上只能实现并发 但是不能实现并行
26. filter map reduce 返回的其实也是一个生成器 github上面的那个说的很好 很多文章看了都学到了很多
27. python 中的浅拷贝和深拷贝 浅拷贝拷贝的是对象的引用
    a = [1, 2, 3, ['a', 'b']]
    b是对上面这个对象的浅拷贝 当a[3].append('c')的时候，b也会变成a = [1, 2, 3, ['a', 'b']]
    但是当a.append(4)的时候，b并不会发生其他任何的改变
    深拷贝的话则不会发生这类任何问题
28. python的垃圾回收机制：
    pyobject是每个对象必有的内容，其中ob.refcnt就是作为引用技术，当一个对象有新的引用时，它的refcnt就会增加
    当引用删除的时候，就会减少，当变成0的时候，该对象的声明就已经结束了 来跟踪和回收垃圾
29. 标记-清除机制，等到没有空闲内存的时候从寄存器和程序栈上的引用出发，遍历以对象为节点，以引用为边构成的图
    把所有可以访问到的对象打上标记，然后清扫一遍内存空间，把所有没有标记的对象进行释放
    这个是用来解决容器对象可能产生循环引用的问题
30. 分代技术：
    以空间换时间的方法提高垃圾回收效率
    将系统中的所有内存块根据其存活时间划分为不同的集合，每一个集合就称为一个‘代’，垃圾收集频率随着‘代’
    的存活时间增大而减小，存活时间通常利用经过几次垃圾回收来进行度量
    索引数越大 对象的存活时间越长

31. list内部的实现在Cpython中还是使用链表实现来实现的 插入和删除的时间复杂度都是O(n)
    list的扩容数量是0->4->8->16->25->35....
    在需要的时候扩容，但是不允许过度的浪费，还会在适当的时候进行内存回收
    (newsize // 8) + (newsize < 9 and 3 or 6)
    反正就是有一个算法 感觉还挺厉害的样子

32. read读取整个文件
    readline 读取下一行 使用生成器的方法
    readlines读取整个文件到一个迭代器以供我们遍历

33. u can use super().__init__() instead of super(ChildB, self).__init__()
34. xrange 和 range 都在循环使用 但是xrange是一个序列对象并且惰性生成

"""
from functools import wraps

class Student:
    __name = 'caiqj'
    __age = 24
    nickname = '阿菜菜在路边边'
    
    def eat(self):
        print('acai is eating')

    def sleep():
        print('acai is sleeping')

# ================
my_generato         r = (i for i in range(5))    # for item in my_generator 只能迭代一次

def create_generator():
    fanwei = range(5)
    for item in fanwei:
        yield item

my_generator = create_generator()       # 同样 返回的也是一个生成器

# ================
def makebold(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return "<b>" + fn(*args, **kwargs) + "</b>"
    return wrapped

def makeitalic(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"
    return wrapped

@makebold
@makeitalic
def hello():
    return "hello world"      # '<b><i>hello world</i></b>'


# ==============================
"""这样写还是有问题的 dic 没有has_key这个方法"""
class Singleton(object):
    _singleton = {}
    def __new__(cls):
        if not cls._singleton.has_key(cls):
            cls._singleton[cls] = object.__new__(cls)
        return cls._singleton[cls]

"""
不管是新式类还是经典类的写法 如果__new__和__init__两个都同时定义了
如果是s = Stu()的话
在实例化的时候就只会调用__new__ 而不会调用__init__，
如果只定义了__init__ 就会调用__init__
"""
class Stu:
    def __new__(cls):
        print('enter __new__')
        return cls

    def __init__(self):
        print('enter __init__')

"""
这个实例是关于slots的使用
使用了__slots__的类的实例就不会有__dict__这个属性
如果自己同时实现了__new__和__init__ 在初始化的时候会出问题的 没事情不要自己去写__new__
现在好像也没有什么新式类和经典类了
"""
def Stu(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    __slots__ = 'x', 'y'

stu = Stu(1, 2)    """dir(stu)发现已经没有__dict__这个属性了"""





class A(object):
    def foo(self):
        print('A is foo')

class B(A):
    def foo(self):
        print('B is foo')
        A.foo(self)

class C(A):
    def foo(self):
        print('C is foo')
        A.foo(self)

class D(B, C):
    def foo(self):
        print('D is foo')
        B.foo(self)
        C.foo(self)
"""
output:     有一些时候我们会需要使用父类中的同名的方法，但是会出现重复使用的情况
D is foo
B is foo
A is foo
C is foo
A is foo
"""

"""
为了确保父类中的方法只能被顺序执行一次，在新对象系统中，可以使用super(aclass. object)可以返回obj实例的一个
特殊；诶行superobject超对象，但并不是简单的父类对象
"""
class A(object):
    def foo(self):
        print('A is foo')

class B(A):
    def foo(self):
        print('B is foo')
        super(B, self).foo()

class C(A):
    def foo(self):
        print('C is foo')
        super(C, self).foo()

class D(B, C):
    def foo(self):
        print('D is foo')
        super(D, self).foo()

"""
output:
D is foo
B is foo
C is foo
A is foo
可以保证父类正确地执行过一次
"""

class Singleton(object):
    _dict = dict()
    def __new__(cls):
        if 'key' in A._dict:
            print('exist')
            return A._dict['key']
        else:
            print('new')
            return super(A, cls).__new__(cls)

    def __init__(self):
        print('init')
        A._dict['key'] = self


def Singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance




