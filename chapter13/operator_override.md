## chapter 13 正确重载运算符


### 13.1 运算符重载基础
    
> 1. 不能重载内置类型的运算符
> 2. 不能新建运算符，只能重载现有的
> 3. 某些运算符不能重载 如`is` `and` or `not` 但是为运算符什么是可以重载的
> 4. 基本原则： 返回一个新对象，不修改self

### 13.2 一元运算符
> 1. 支持一元运算符很简单，只需要实现相应的特殊方法，这些特殊方法只有一个参数就是self
> 2. `__neg__(self)       # -1`
>    `__pos__(self)       # +1`
>    `__abs__(self)       # abs(-1)` 
>    `__invert__(self)    # ~1  整数位取反`
> 3. 并不是所有的情况下 `obj == +obj` 的

### 13.3 重载向量加法运算符`+`
#### 比如两个长度不同的向量相加
```python
import itertools
class Vector1:
    def __init__(self, values):
        self.values = list(values)
    def __add__(self, obj):
        obj = itertools.zip_longest(self.values, obj.values, fillvalue=0)
        return Vector1(i+j for i, j in obj)
    def __repr__(self):
        print(self.values)
v1 = Vector1([1, 2])
v2 = Vector2([3, 4, 5, 6])
v1+v2
```
> python会为中缀运算符特殊方法提供的特殊的分派机制
>> 1. 如果左操作数有`__add__()` 而且返回值不是`NotImplemented`,就调用`v1.__add__(self, v2)`
>> 2. 如果做操作数没有`__add__()` 或者调用方法以后返回`NotImplemented`，就会检查右操作数有没有`__radd__()`方法。
>>    如果有，而且返回的不是`NotImplemented`,就调用`v2.__radd__()`，然后返回结果。
>> 3. 如果右操作数没有`__radd__()`，或者调用了以后返回的是`NotImplemented`，就会抛出`TypeError`。并在错误消息中指出操作数类型不支持
>> 4. 以r开头的内置运算符表示会在右操作数上进行作用
>> 5. 为了遵守鸭子类型的精神，我们不应该直接去检测元素的数据类型是否正确，取而代之我们应该去捕获异常
```python
class Vector1:
    ...
    def __add__(self, obj):
        try:
            obj = itertools.zip_longest(self.values, obj.values, fillvalue=0)
            rst = [i+j for i, j in obj]
        except:
            return NotImplemented
        return rst
```

### 13.4 重载标量乘法运算符
> 1. `Vector([1, 2, 3]) * x` 如果`x`是数字 就是计算标量积；各个分量都会乘以`x`，这个叫做元素级乘法
```python
class Vector1:
    ...
    def __mul__(self, scalar):
        return Vector(i*scalar for i in self.values)
    def __rmul__(self, scalar):
        return self * scalar
```
> 2. 这样写会有一个缺陷就是当`scalar`是也是`vector`对象或是别的什么的时候会出现`TypeError`的问题
>    但是我们可以使用`isinstance()`来判断抽象基类.
```python
class Vector1:
    ...
    def __mul__(self, scalar):
        if instance(scalar, numbers.Real):
            rst = [i*scalar for i in self.values]
        else:
            return NotImplemented
        return rst
    def __rmul__(self, scalar):
        return self.scalar
```
> 3. 还有一些其它内置的运算符函数
>> 1. `__truediv__()`  /  ` __rtruedive__()`   / `__itruediv__()`
>> 2. `__mod__()`  /  `__rmod__()`  /  `__imod__()`

### 13.5 比较运算符
> 1. 正向反向调用使用的都是同一系列的方法。比如对于`==`来说调用的都是`__eq__()`
```python
a == b   a.__eq__(b)  or   b.__eq__(a)   ==>  返回的是id(a) = id(b)
a != b   a.__ne__(b)  or   b.__ne__(a)   ==>  返回的是not(a == b)
a > b    a.__gt__(b)  or   b.__lt__(a)   ==>  抛出TypeError
a < b    a.__lt__(b)  or   b.__gt__(a)   ==>  抛出TypeError
a >= b    a.__ge__(b)  or   b.__le__(a)   ==>  抛出TypeError
a <= b    a.__le__(b)  or   b.__ge__(a)   ==>  抛出TypeError
```
> 2. `all()`这个函数会判断这个迭代对象里面的所有元素 是否都为`True`,如果有一个为`False`，就是`False`
> 3. `[1, 2] == (1, 2)     # False`
> 4. `Vector(1, 2) == (1, 2)`
> 解释器会首先判断`isinstance()`，如果类型不对抛出`NotImplemented`，解释器会调用`tuple(1, 2).__eq__()`
> 如果也抛出`NotImplemented`的错误，这时候解释器就会最后再调用一次`id(a) == id(b)` 进行一次最后的比较，如果还是不行就不行

> 如果中缀运算符抛出了异常，我们最好将其进行捕获，然后抛出`NotImplemented`，这样解释器回去调用反向运算符，有的时候因为操作数类型导致
> 的异常可能会因为反向运算符就返回正确的结果。

### 13.6 增量赋值运算符
> 1. 增量赋值运算符并不会修改不可变的实例，而是会重新生成一个对象，再进行绑定
> 2. `a+= b` 使用的是`__iadd__`即就地运算符，就会直接修改左操作数而不是返回一个全新的对象了
> 3. 不可变类型一定不要实现就地运算特殊方法，会出问题的
> 4. python处理就地运算符的操作其实就是当作普通的运算符然后再进行一个赋值操作 因此不管是可变还是不可变类型都可以使用


