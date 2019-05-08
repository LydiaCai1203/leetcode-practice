"""
1. 基本上，内置类型的方法不会调用子类覆盖的方法。比如，dict的子类覆盖的__getitem__()不会被内置类型的get()所调用
2. obj = DoppelDict(one=1)    # __init__()跳过__setitem__()    {'one': 1}
3. obj['two'] = 2             # 会调用自己实现的__setitem__()    {'one': 1, 'two': [2, 2]}
4. obj.update(three=3)                # 不会使用自己覆盖的__setitem__()  {'one': 1, 'two': 3}
--------------
*. 不只是实例的调用有这个问题（self.get()不会调用self.__getitem__()）
1. obj = AnswerDict(one=1)
2. obj['one']   # 42   ------>but------>   obj.get('one')   # 1     会调用get() 不会调用 __getitem__()
3. obj.update({one:2})       # 还是一样的

# 直接子类化内置类型（dict list str）容易出错，因为内置类型的方法通常会忽略用户覆盖的方法，所以不要子类化内置类型
# 用户自己定义的类应该继承自 collections模块中的类 比如 UserDict UserList UserStr 都做了特别的设计
--------------
1. obj2 = DoppelDict2(one=1)     # {'one': [1, 1]}
2. obj2['two'] = 2               # {'one': [1, 1], 'two': [2, 2]}
3. obj.update({'three': 3})      # {'one': [1, 1], 'two': [2, 2], 'three': [3, 3]}
4. 同样的例子不举了 反正就是不会出现直接继承原生的内置类型的类会出现的哪些问题
--------------
下面说一下多重继承和方法解析顺序
1. 尤其要注意一下继承base类时候的顺序问题，从左往右是父类->爷爷类
2. d = D()
   # 输出的竟然是最爷爷辈的类所实现的ping() 因为B和C都没有实现ping()这个方法
   d.ping()                      #  A-ping: <inherit.D object at 0x10fb50ba8>
                                 #  D-ping: <inherit.D object at 0x10fb50ba8>
   # 自己没有实现 C类覆盖了B类型写的
   d.pong()                      #  C-pong: <inherit.D object at 0x10fb50ba8>
   
   # 
   d.pingpong()                  #  A-ping: <inherit.D object at 0x10fb50ba8>
                                 #  D-ping: <inherit.D object at 0x10fb50ba8>
                                 
                                 #  A-ping: <inherit.D object at 0x10fb50ba8>
                                 
                                 #  C-pong: <inherit.D object at 0x10fb50ba8>
                                 #  C-pong: <inherit.D object at 0x10fb50ba8>
                                 #  C-pong: <inherit.D object at 0x10fb50ba8>
3. C.pong(self)                  # 子类都可以直接调用超类的方法 但是要传入self 因为使用的是未绑定的方法

python能区分d.pong()调用的是哪个方法，因为python会按照特定的顺序遍历继承图，这个顺序叫做方法解析顺序（method resolution order）
类都有一个名为__mro__()的属性，它的值是一个元组，按照方法接续顺序列出各个超类，从当前类一直向上，直到Object为止

D类的__mro__属性如下： (inherit.D, inherit.C, inherit.B, inherit.A, object)
反正就是要按照顺序进行继承就对了。

4. 若想把方法委托给超类， 推荐使用super() 因为这样调用会遵守方法解析顺序
5. bool.__mro__                  #  (bool, int, object)
6. python 的GUI工具库 Tkinker
-----------------
使用多重继承需要注意的几个地方：
1. 把接口继承和实现继承分开
   1. 继承接口， 创建子类型，实现“是什么”的关系
   2. 继承实现，通过重用来避免代码重复
通过继承 重用代码 是实现细节，通常都可以使用组合和委托的模式，而接口继承则是框架的支柱
2. 使用抽象基类显示表示接口
   1. 如果类的作用是定义接口，应该明确地定义为抽象类
3. 通过混入重用代码
   1. 如果一个类的作用是为了多个不相关的子类提供方法实现，从而实现冲用的目的，并不是为了体现“是什么”，应该将这个类归为混入类
   混入类是不能实例化的。只是打包方法用的。
4. 在名称中明确指明混入
5. 抽象基类可以作为混入，反过来则不成立。
   1. 因为抽象基类也可以实现具体的方法 所以可以作为混入类 但是抽象基类可以定义类型，但是混入做不到，抽象类可以作为其他类的唯一基类
   但是混入类不可以作为超类使用。
6. 不要子类化多个具体类。具体类可以没有，或者最多只有一个具体超类，其余的都必须是抽象基类，或者是混入。
7. 聚合类就是如果抽象基类+混入的组合对客户代码会非常有用的话。
8. 优先使用对象组合，而不是类继承。

"""
import collections

# version 1.0
class DoppelDict(dict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)

class AnswerDict(dict):
    def __getitem__(self, key):
        return 42


# version 2.0
class DoppelDict2(collections.UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key, [value] * 2)
    
    def __getitem__(self, key):
        return 42


class A:
    def ping(self):
        print('A-ping:', self)

class B(A):
    def pong(self):
        print('B-pong:', self)

class C(B):
    def pong(self):
        print('C-pong:', self)

class D(C, B):                           
    def ping(self):
        super().ping()
        print('D-ping:', self)
    
    def pingpong(self):
        self.ping()
        super().ping()
        self.pong()
        super().pong()
        C.pong(self)

