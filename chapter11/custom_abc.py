"""
1. 自己定义的抽象基类要继承abc.ABC
2. 抽象方法使用@abstractmethod 而且定义体中通常只有文档字符串
3. 抽象基类也可以包含具体的方法
4. 抽象基类中的具体方法只能依赖抽象基类定义的接口 或者具体方法 或者特性
5. 抽象方法可以有实现代码，即便实现了，子类也必须覆盖抽象方法，但是在子类中可以使用super()函数调用抽象方法
为它添加功能而不是实现。
6. 同样 抽象基类是不能被实例化的
--------------------
异常类的部分层次结构 可以查看相关文档（https://docs.python.org/dev/library/exceptions.html#exception-hierarchy）

--------------------
声明抽象类方法的推荐方法是：
class MyABC(abc.ABC):
    @classmethod
    @abc.abstractmethod          # 这一句必须放在最后一行，贴着def
    def an_abstract_classmethod(cls, ...):
        pass

7. random.shuffle(items)
   random.SystemRandom().shuffle(items)

8. 在抽象基类中添加额外的方法并没有问题

"""
import abc
import random

class Tombola(abc.ABC):
    
    @abc.abstractclassmethod
    def load(self, iterable):
        """从可迭代对象中添加元素"""
    
    @abc.abstractclassmethod
    def pick(self):
        """
        随机删除元素 然后将其返回
        """
    
    def loaded(self):
        """
        如果至少有一个元素 返回True 否则 返回 False
        """
        return bool(self.inspect())

    
    def inspect(self):
        """
        返回一个有序元组 由当前的元素组成
        """
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(sorted(items))



class BingoCage(Tombola):

    def __init__(self, items):
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)
    
    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    
    def __call__(self):
        self.pick()


class LotteryBlower(Tombola):

    def __init__(self, iterable):
        """接受任何可迭代的对象 构造成列表"""
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)
    
    def pick(self):
        try:
            position = random.randrange((len(self._balls)))
        except ValueError:
            raise LookupError('pick from empty LotteryBlower')
        return self._balls.pop(position)
    
    def loaded(self):
        return bool(self._balls)
    
    def inspect(self):
        return tuple(sorted(self._balls))


"""
即便不继承，也有办法把一个类注册为抽象基类的虚拟子类。这样做我们可以保证注册的类忠诚地实现了抽象基类定义的接口
python解释器会相信我们，不对类进行检查，如果有问题会在运行时抛出异常
"""
@Tombola.register
class TombolaList(list):

    def pick(self):
        if self:
            position = random.randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend

    def loaded(self):
        return bool(self)
    
    def inspect(self):
        return tuple(sorted(self))





    