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
    4. __metaclass__是在创建类的时候起作用，和__new__还有__init__是对创建实例起作用的

-------------------------
### 14. 单例模式
    1. pass
