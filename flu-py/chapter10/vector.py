"""
tips:
1. reprlib 可以生成长度有限的表示形式

2. repr的目的是为了调试，所以是绝对不能抛出异常的

3. 协议：非正式的接口，只有在文档中进行定义，在代码中不定义。
   for example: python 的序列协议只需要实现__len__()和__getitem__()两个方法。
   这个类的对象就可以使用在任何期待序列的地方了。
   说一个东西是不是序列 要看这个东西的行为像不像序列 这就是python中的鸭子类型的意思

   如果只是需要实现迭代的行为 只需要实现__getitem__()的方法就可以了

4. 切片原理：
   切片返回的应该是各自类型的新实例 而不是都是列表 或者都是元组什么的
   a. 切片对象：slice()
   b. slice(None, 10, 2).indices(5)           -->  (0, 5, 2)
   c. slice(-3, None, None).indices(5)        -->  (2, 5, 1)
   slice(start, end, step).indices(len)       # 超过边界的索引都会被截掉

5. dir(classname) 查看类的属性
   help(slice.indices)    查看这个成员的相关注释

6. list(range(7))  array.array('d', range(7))

7. @property 可以把数据成员标记为只读属性

8. 在类中声明__slot__属性可以防止设置新实例属性，该属性只是为了节省内存，而且仅当内存严重不足的
时候才应该使用。

9. __setattr__() 应该和 __getattr__()成对出现

10. __hash__()和__eq__() 有助于把vector实例变成可散列对象。

11. zip() 函数的使用

12. 内置的enumerate()可以用来处理索引

13. lambda a: a+1 匿名函数的相关市县

14. 一个标准： sum(i for i in my_list) 

"""
from array import array
import reprlib
import math
import numbers

class Vector:
    typecode = 'd'
    shortcut_names = 'abcdefghijklmn'

    def __init__(self, components):
        self._components = array(self.typecode, components)
    
    @property
    def x(self):
        return 'i am x'

    def __getattr__(self, attr):
        """
        my_obj.x 解释器会检查实例有没有名为x的属性，
        如果没有，就到类(my_obj.__class__)中进行查找
        如果都没有的话 就会去调用 __getattr__()
        """
        cls = type(self)
        if len(attr) == 1:
            pos = cls.shortcut_names.find(attr)
            if 0 <= pos < len(self._components):
                return self._components[pos]
        raise AttributeError('should not input over 2 chars')

    def __setattr__(self, name, value):
        """
        为属性成员赋值的时候就会调用这个函数了，但是给x对象赋值的时候要额外小心 因为是只读对象
        super()函数用于动态访问超类的方法。
        """
        cls = type(self)
        if len(name) == 1:
            if name in cls.shortcut_names:
                error = 'readonly attribute'
        elif name.islower():
            error = 'can not be over 2 chars'
        else:
            error = ''
        
        if error:
            raise AttributeError(error)
        
        super().__setattr__(name, value)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        """
        调试的时候输出的对象
        """
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        """
        print的时候输出的对象
        """
        return str(tuple(self))

    def __bytes__(self):
        return bytes(ord(self.typecode)) + bytes(self._components)

    def __eq__(self, other):
        return tuple(self) == tuple(other)    
    
    def __abs__(self):
        return math.sqrt(sum(x*x for x in self))

    def __bool__(self):
        return bool(abs(self))

    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(1, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    """    
        比较low的实现    
        def __getitem__(self, index):
            return self._components[index]
    """



    
class TestSlice:
    """
    obj = TestSlice()
    obj[1]               # index = 1
    obj[1: 3]            # index = slice(1, 2, None)
    obj[1: 4: 2]         # index = slice(1, 4, 2)
    obj[1: 4: 2, 9]      # index = (slice(1, 4, 2), 9)
    obj[1: 4: 2, 7:9]    # index = (slice(1, 4, 2), slice(7, 9, None))
    """
    def __getitem__(self, index):
        return index


class Ziptest:
    """
    介绍一下zip的使用
    1. zip()函数返回一个生成器，按需生成元组
    2. 当其中一个可迭代对象消耗完以后，zip不会发出警告就会停止
    3. from itertools import zip_longest
    直到最长的可迭代对象消耗完，还可以自己选择填充缺失位置的数值
    """
    def example(self):
        my_list = list(zip(range(3), 'ABC'))


    





