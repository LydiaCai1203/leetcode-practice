"""
2019-4-16
some tips:
1. python 没有 interface 关键字
2. 除了抽象基类，每个类都有接口：类实现或继承的公开属性，包括了特殊方法，如—__getitem__,__add__这些
3. 受保护的和私有属性不在接口当中
4. 公开数据属性也可以放在接口当中
5. 接口就是对象公开方法的子集，让对象在系统中扮演特定的角色
6. 协议也是接口，只是不是正式的接口，因此协议不能像正式接口那样增加限制，一个类被允许只实现部分接口
7. 在python中， xx类对象，x协议，x接口都是一个意思
---------------------
序列协议：
1. 定义__getitem__，只是实现序列协议中的一部分，但是满足访问元素，迭代和使用in运算符了
2. 如果没有实现__contains__和__iter__,就会看看有没有__getitem__，有的话就是用它
3. 实现序列协议主要实现__getitem__和__len__即可
---------------------
1. 使用猴子补丁在运行时实现协议

2. python 的序列协议里面已经有了洗牌方法 也就是说random.shuffle只关心对象是否实现了 可变 序列协议
即便对象一开始没有提供该方法，后来提供了也是一样的。

from random import shuffle
my_list = list(range(10))
shuffle(my_list)     # 得到一个乱序的序列

3. 如果要实现可变的序列协议还需要实现__setitem__的方法
python 是动态语言，我们可以在运行时修正类的具体实现

# 这种技术就叫做猴子补丁：在运行的时候修改类和模块，而不用改动源码
def set_card(deck, position, card):
    deck._cards[position] = card
my_instance.__setitem__ = set_card
shuffle(my_instance)                     # 发现就不会再报错了

4. python的abc 可以使用register类方法在终端用户的代码中把某个类“声明”为一个一个抽象基类的子类
但是被注册的类必须要满足抽象基类对方法名称以及签名的要求，最重要的是满足底层语义契约。

5. 要么继承相应的抽象基类，要么就把类注册到相应的抽象基类中
如果要检查对象是不是序列 应该使用 isinstance(obj, collections.abc.Sequence)

6. 不要在生产环境中去定义抽象基类！！！！！！

7. isinstance 和 issubclass 来测试抽象基类
isinstance(1, numbers.Number)  

--------------------------
8. python3中的一些基类：
Iterable Container Sized

Sequence Mapping Set
不可变的集合类型，都有各自可变的子类，MutableSequence MutableMapping MutableSet

MappingSet
.items() .keys() .values() 返回的对象分别是ItemsView KeysView ValuesView

Callable Hashable
这两个抽象基类和集合并没有太大的关系，这两个基类的主要作用是为了内置函数isinstance提供支持，以一种安全的方式判断对象能不能调用或这是散列

Iterator 是 Iterable的子类

10pages finished
2019-4-17:
    null

"""
from random import shuffle
import collections
from collections import abc


class Foo:
    def __contains__(self, value):
        print('enter contains func')
        return False

    def __iter__(self):
        print('enter iter func')
        return iter([1, 2, 3])

    def __getitem__(self, pos):
        return range(0, 20, 10)[pos]


Card = collections.namedtuple('Card', ['rank', 'suit']) 

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
    
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, pos):
        return self._cards[pos]

    def __setitem__(self, position, card):
        """
        语言中参考使用的参数名是：self, key, value
        """
        self._cards[position] = card


class MutableFrenchDeck(collections.MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks for suit in self.suits]
    
    def __len__(self):
        return len(self._cards)

    def __getitem__(self, pos):
        return self._cards[pos]

    def __setitem__(self, position, card):
        """
        语言中参考使用的参数名是：self, key, value
        """
        self._cards[position] = card
    
    def __delitem__(self, position):
        """必须实现"""
        del self._cards[position]
    
    def insert(self, position, value):
        """必须实现"""
        self._cards.insert(position, value)
    




class Struggle:
    def __len__(self):
        return 20

"""
可以看出来只要实现了__len__，解释器会自动判断出是继承自哪个abc
"""
obj = Struggle()
print(isinstance(obj, abc.Sized))




    


