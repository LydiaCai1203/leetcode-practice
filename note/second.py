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
my_generator = (i for i in range(5))    # for item in my_generator 只能迭代一次

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
