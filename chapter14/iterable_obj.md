## chapter14 可迭代的对象、迭代器和生成器

> 1. 迭代器模式：当扫描内存中放不下的数据集时，我们要找到一种惰性获取数据项的方式，即按需一次获取一个数据项
> 2. 所有的生成器都是迭代器，因为生成器完全实现了迭代器的接口
> 3. 根据《设计模式：可复用面向对象软件的基础》书中的定义：
>> 1. 迭代器： 用于从集合中取出元素
>> 2. 生成器： 用于凭空生成元素
> 4. python中的`range`返回的是一个类似生成器的东西，但是并不是生成器，如果要求返回的是`list`,可以使用`list(range(5))`

### 14.1 Sentence第一版: 单词序列
```python
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    def __getitem__(self, index):
        return self.words[index]
    def __len__(self):
        return len(self.words)
    def __repr__(self):
        return 'Sentence{}'.format(reprlib.repr(self.text)
```
#### 序列可以迭代的原因:`iter函数`
> 1. 解释器需要迭代对象x的时候，会自动调用iter(x)
> 2. 内置的iter函数有以下作用
>> 1. 检查对象是否实现了`__iter__()`,如果实现了就调用它，获取一个迭代器
>> 2. 如果没有实现`__iter__()`,但是实现了`__getitem__()`,python就会创建一个迭代器，尝试按顺序从0开始获取元素
>> 3. 如果尝试失败，python就会抛出`TypeError`异常，通常会提示“C object is not iterable” C是目标对象所属类
##### python序列都可以迭代的原因是因为都实现了`__getitem__()`,其实标准的序列也都实现了`__iter__()`
```python
class Foo:
    def __iter__(self):
        pass
from collections import abc
issubclass(Foo, abc.Iterable)
```
##### 从python3.4开始，检查对象x能否迭代，最准确的方法就是调用iter(x)，如果不可以迭代，再处理TypeError,iter()会考虑到调用__getitem__()，但是abc.Iterable则不会考虑


### 14.2 可迭代的对象与迭代器的对比
#### 可迭代的对象
> def. 使用iter内置函数可以获取迭代器的对象，如果对象实现了能返回迭代器的__iter__()，那么改对象就是可迭代的。序列都是可迭代的，因为都实现了__getitem__(）
> iterable & iterator: python从可迭代的对象中获取迭代器
#### 迭代器
> def. 实现了无参数__next__(),返回序列中的下一个元素，如果没有元素了，就会抛出StopIteration异常，Python中的迭代器还实现了__iter__(),因此迭代器也可以迭代

```python
# 以下两种写法是等价的
s = 'ABC'
for char in s:
    print(char)       # 字符串背后也是有迭代器的
```
```python
s = 'ABC'
it = iter(s)
while True:
    try:
        print(next(it))
    except StopIteration:      # 出现这个义仓表示迭代器到头了
        del it                 # 释放it引用
        break                  # 推出循环
```
#### 标准的迭代器接口有两个方法：
> 1. `__next__()`作用是返回下一个可用的元素
> 2. `__iter__()`返回的是self,以便在应该使用可迭代对象的地方使用迭代器
> 3. absclass Iterable(`__iter__()`)-->absclass Iterator(`__iter__()`&`__next__()`)
>> `def __iter__(self): return self`
#### 检查对象x是都是迭代器的最好的方式就是调用isinstance(x, abc.Iterator)
#### 迭代器无法被还原，无法检查是否还有遗留的元素，如果想再次迭代，就要构造一个新的迭代器

### 14.3 Sentence类第二版：典型的迭代器
```python
import re
import reprlib

pattern = '\w+'
pattern_it = re.compile(patern)
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = pattern_it.findall(text)
    def __repr__(self):
        return 'Sentence{}'.format(reprlib.repr(self.text))
    def __iter__(self):
        return SentenceIterable(self.words)

class SentenceIterable:
    def __init__(self, words):
        self.words = words
        self.index = 0
    def __next__(self):
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration()
        self.index += 1
        return word
    def __iter__(self):
        return self
```
#### 把Sentence变成迭代器：坏主意 因为可迭代的对象并不是一个迭代器
#### 迭代器模式
> 访问一个聚合对象的内容而无需暴露它的内部表示
> 支持对聚合对象的多种遍历
> 为遍历多种不同的聚合结构提供一个统一的接口
#### 要支持多种遍历就要实现自己的迭代器对象，这样就可以独立地实例化多个相互独立的迭代器对象了，也就可以实现多种遍历了


### 14.4 Sentence类第3版：生成器函数
#### python习惯的实现方式是用生成器函数代替SentenceIterator类。
```python
import re
import reprlib

pattern = '\w+'
pattern_it = re.compile(patern)
class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = pattern_it.findall(text)
    def __repr__(self):
        return 'Sentence{}'.format(reprlib.repr(self.text))
    def __iter__(self):              # 这里的迭代器其实是生成器对象
        for word in self.words:
            yield word
        return                       # 这个return语句都不是必要的
```
#### 不管有没有return语句，生成器函数都不会抛出StopIteration异常，而且在生成完全部值以后，会自动退出
#### 生成器函数的工作原理
> def. 只要在python函数中有yield的就是生成器函数
> 调用生成器函数的时候会返回一个生成器对象，也就是说生成器函数其实是生成器工厂
```python
def gen123():
    print('111')
    yield 1
    print('222)
    yield 2
    print('333)
    yield 3
    print("end")

obj = gen123()         # obj 是一个生成器对象
for i in obj:
    print(i)
```
#### 生成器函数会创建一个生成器对象，包装生成器函数的定义体，生成器会产生值，，生成器函数定义体中的return语句会触发生成器对象抛出StopIteration异常
#### 不太理解书上说的return语句会导致StopIteration异常进行抛出
> 1. 第一次循环 打印输出 111， 停留在第一条yield语句，生成了1的值
> 2. 第二次循环，打印输出222， 停留在第二条yield语句，生成了2的值
> ...
> 3. 第四次循环，打印输出end, 到达到函数定义题的末尾，导致生成器对象抛出异常
> 4. for循环机制会捕获异常，所以循环的时候是不会报错的

### 14.5 Sentence第四版：惰性实现
#### `re.finditer()`是`re.findall()`的惰性版本，它返回的不是一个列表，而是一个生成器
```python
import re
import reprlib

RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return 'Sentence{}'.format(reprlib.repr(self.text))
    def __iter__(self):
        for match in RE_WORD.finditer(self.text):
            return match.group()                        # 从MatchObject实例中提取匹配正则表达式的具体文本
```

### 14.6 Sentence类第五版：生成器表达式
#### 生成器表达式可以简单地理解为是列表推导的惰性版本， 生成器表达式也是生成器的惰性工厂
```python
import re
import reprlib

RE_WORD = re.compile('\w+')
class Sentence:
    def __init__(self, text):
        self.text = text
    def __repr__(self):
        return 'Sentence{}'.format(reprlib.repr(self.text))
    def __iter__(self):
        return (match.group() for match in RE_WORD.finditer(self.text))
```
#### 生成器表达式完全可以替换成生成器函数，不过有时候使用生成器表达式会更加便利

### 14.7 何时使用生成器表达式
#### 简单说就是 方便用生成器表达式就用表达式，不行就用函数

### 14.8 另一个例子： 等差数列生成器
#### 无穷等差数列生成器 itertools.count(start, step)
```python
it = itertools.count(1, 1.5)
next(it)          # 1
next(it)          # 2.5
next(it)          # 4.0
```
### 14.9 标准库中的生成器函数

##### 欧阳老师问我 是不是很恨这个把我丢在这里的人 我有点惊讶 难道大家都觉得我是这样想的吗 我其实一点都不怪他，我就是讨厌他，因为他也讨厌我呀，和他是走是留没有关系
##### 而且就算他会一直留在这家公司，我也不会，因为我在这里并不是很自在，我觉得自己成长的也很慢，我知道我这样很自私，但我真的不是因为他走才讨厌他的，真的不是。

#### os.walk()，这个函数在遍历目录树的过程中产出文件名，因此递归搜索文件系统就像for循环那样简单
> 第一组：用于过滤的生成器函数
>> 从输入的可迭代对象中产出元素的子集，而且不修改元素本身；如itertools.takewhile()
```python 
import itertools

def vowel(c):
    return c.lower() in 'aeiou'

list(itertools.filterfalse(vowel, 'Aardvark'))     # ['r', 'd', 'v', 'r', 'k']
list(itertools.dropwhile(vowel, 'Aardvark'))       # ['r', 'd', 'v', 'a', 'r', 'k']  跳过vowel返回为真的元素，然后接下来不做任何处理判断
list(itertools.takewhile(vowel, 'Aardvark'))       # ['A', 'a']                      返回真挚的遇到flase不符合条件的就退出
list(itertools.compress('Aardvark', (1, 0, 1, 1, 0, 1)))    # ['A', 'r', 'd', 'a']
list(itertools.islice('Aardvark', 4))              # ['A', 'a', 'r', 'd']
list(itertools.islice('Aardvark', 4, 7))           # ['v', 'a', 'r']

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
list(itertools.accumulate(sample))                 # [5, 9, 11, 19, 26, 32, 35, 35, 44, 45]
list(itertools.accumulate(sample, min))            # [5, 4, 2, 2, 2, 2, 2, 0, 0, 0]
list(itertools.accumulate(sample, max))            # [5, 5, 5, 8, 8, 8, 8, 8, 9, 9]

import operator
list(itertools.accumulate(sample, operator.mul))           # [5, 20, 40, 320, 2240, 13440, 40320, 0, 0, 0]
list(itertools.accumulate(range(1, 11), operator.mul))     # [1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800]
```
#### 阿菜的扩展部分：
> 使用pymongo做查询操作的时候返回的cursor也是一个生成器对象，如果我们只想要前几个元素，可以不使用limit，因为这个limit这里好像有一个坑，我想不起来了，暂不提
> list(itertools.islice(cursor, 2))
> 这就可以得到一个数量确实只有2个的列表了，我感觉比pymongo里面的limit要好些
> 话说这个函数就是可以对任何的生成器都进行切片操作的一个东西啊，感觉会很好用，不是吗？

#### 用于映射的生成器函数
```python
list(enumerate('asdfgh', 1))                                        # [(1, 'a'), (2, 's'), (3, 'd'), (4, 'f'), (5, 'g'), (6, 'h')]
list(enumerate('asdfgh', 2))                                        # [(2, 'a'), (3, 's'), (4, 'd'), (5, 'f'), (6, 'g'), (7, 'h')]
list(map(operator.mul, range(11), range(11)))                       # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
list(itertools.starmap(operator.mul, enumerate('asdfgh', 1)))       # ['a', 'ss', 'ddd', 'ffff', 'ggggg', 'hhhhhh']
list(itertools.chain(range(3), range(5)))                           # [0, 1, 2, 0, 1, 2, 3, 4]  可以将两个迭代器生成的元素无缝链接在一起
// 内置的zip函数 会用 所以不写了
// itertools.zip_longest 长度不一样的能被填充然后进行配对 会用 不写了
list(itertools.cycle('ABC'))                                        # 把it产生出各个元素存储副本，然后按照顺序重复不断地产出各个元素
// 还有一些函数 感觉并没有很实用 如果还有要翻查的 再回来看fluent-py好了
```

### 14.10 python3.3中的新出现的句法： yield from
#### 如果生成器函数需要产生另一个生成器产生的值，解决的方法通常是使用一个嵌套的for循环
```python
def chain(*iterators):
    for iterator in iterators:
        for it in iterator:
            yield it
list(chain(range(3), range(5)))                                     # [0, 1, 2, 0, 1, 2, 3, 4]
```
#### chain生成器函数把操作依次交给接受到的各个可迭代对象处理
```python
def chain(*iterators):
   for iterator in iterators:
       yield from iterator
```

### 14.11 可迭代的归约函数
#### 接受一个可迭代的对象，然后返回单个结果，这些函数叫做：归约函数、累加函数、合拢函数
```python
all(it)
any(it)
max(it, [key=], )
min(it, [key=], )
functools.reduce(func, it, [initial])     
sum(it, start=0)        # 这个可以用一用
```

### 14.12 深入分析iter函数
#### iter还有一个比较少见的用法，iter(必须是可调用的对象， 哨符)
#### 当可调用的对象返回了哨符对应的这个值的时候，就会抛出StopIteration异常，而不产出哨符
```python 
from random import randint

def d6():
    return randint(1, 6)

d6_iter = iter(d6, 1)
d6_list = list(d6_iter)          # 不知道会产生几个数字，反正当产生1的时候，迭代就会停止
```
#### 现在讲一个更加实用的例子
```python

```