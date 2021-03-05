# 章7: 函数装饰器和闭包

### 7.1 装饰器基础知识

```markdown
装饰器是可调用的对象，其参数被装饰的函数。装饰器可能会处理被装饰的函数，然后把它返回，或者将其替换成另一个函数或可调用对象。
```

**下述两种写法等效**：

```python
@decorate
def target():
    print('running target()')

def target():
    print('running target()')
target = decorate(target)
```

**因此：**

```python
def deco(func):
    def inner():
        print('running inner()')
    return inner

@deco
def target():
    print('running target()')

# target() 等价于 inner()
```

### 7.2 Python 何时执行装饰器

```markdown
装饰器的一个关键特性是，它们在被装饰的函数定义之后立即运行。这样通常是在导入时(Python 加载模块时)就会运行了。

原因：《流畅的 python》第二十一章第三节 有讲解...
```

```python
registry = []
def register(func):
    print(f'running register: {func.__name__}')
    registry.append(func)
    return func

@registry
def f1():
    print('running f1')
    
running register: f1         # 调用 f1() 之前
print('running f1')          # 调用 f1() 之后
```

参考文章请看：[导入时 和 运行时](https://halfclock.github.io/2019/06/07/python-import-and-running/)

```
Python 有两种执行代码的方式：
1. 通过命令行方式执行 Python 脚本 - 运行时
2. 将代码从一个文件首次导入到另一个文件/解释器中 - 导入时

导入时：
1. 会执行所导入模块中的所有顶层代码。
2. 函数体会被编译，但是不会被执行。
3. 类的定义体会被执行，但是里面的方法不会被执行。
4. 嵌套于类的类的定义体也会被执行，但是里面的方法不会被执行。
5. 被装饰器装饰的类, 装饰器会先执行，然后再执行类的定义体。?

运行时：
1. 运行时的规则与导入时的规则基本一致，但是 if __name__ == '__main__' 中的代码块会被执行到。

运行时和导入时最大的不同就是，导入时 test.py 的 __name__ = 'test', 但是运行时 test.py 的 __name__ = '__main__'。因为在运行的时候，Python 解释器会将其赋值为 __main__。
```

### 7.3 变量作用域规则

```markdown
Python 在编译函数的定义体时，首先判断变量是局部变量，因为在函数中给它进行了赋值。如果函数想为全局变量赋值，需要 global 声明。
```

### 7.5 闭包

```markdown
闭包：
指延伸了作用域的函数，在函数定义体中引用了非函数定义体中定义的非全局变量。不过也只有嵌套在其他函数中的函数，才可能需要处理不在全局作用域中的外部变量。
```

```python
# 典型的闭包形式
def make_averager():
    series = []
    def averager(new_value):
        # 但是要注意这里这样赋值不会报错的原因是因为 series 是一个 list, 可变对象
        series.append(new_value)
        total = sum(series)
        return total / len(series)
```

### 7.6  nonlocal 声明

```markdown
nonlocal 声明可以把变量标记为自由变量，即使在函数中为变量赋予了新值了，也会变成自由变量。如果为 nonlocal 声明的变量赋予了新值，闭包中保存的绑定会更新。
```

```python
def make_averager():
    series = 0
    def averager():
        nonlocal series
        series += 10
        total = sum(series)
        return total / len(series)
    return averager
```

### 7.7 实现一个简单的装饰器

```markdown
装饰器的典型行为：
1. 把被装饰的函数替换成新函数，二者接受相同的参数。
2. 通常返回被装饰的函数本该返回的值，同时还会做些额外的操作。
```

```markdown
"""
    每次调用都为被装饰的函数计时
"""
import time
import functools

def clock(func):
    # func 就是自由变量
    # wraps 会把相关的属性从 func 复制到 clocked 中。作用是协助构建行为良好的装饰器
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        print(f'本次运行时间: {elapsed}')
        return result
    return clocked
```

### 7.8 标准库中的装饰器

**`functools.lru_cache` 做备忘**

```python
@functools.lru_cache(maxsize=128, typed=False)
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

```markdown
1. @functools.lru_cache 会应用在 @clock 返回的函数上
2. @functools.lru_cache 常被应用来优化递归函数
3. maxsize 指定存储多少个调用的结果，缓存满了之后，旧的结果会被扔掉，腾出空间，其值应该设为 2 的幂值。使用字典存储。
4. typed 如果是 True，把不同参数类型得到的结果分开保存，即把通常认为相等的浮点数和整数参数(1 和 1.0)分开存储。
```

**`functools.singledispatch` 单分派泛函数**

```python
from functools import singledispatch

@singledispatch0
def show(obj):
    print(obj, type(obj), "obj")

# 函数名不重要，因此可以使用 '_'
@show.register(str):
def _(text):
    print(obj, type(obj), str)

@show.register(str):
def _(n):
    print(obj, type(obj), int)

show(1)    
show("xx")
show([1])
```

```markdown
1. @functools.singleddispatch 可以把整体方案拆分成多个模块，甚至可以为你无法修改的类提供专门的函数。使用 @singledispatch 装饰的普通函数会变成泛函数。
2. 通过叠放多个 register 装饰器，可以让同一个函数支持不同的类型。
3. @singledispatch 不是为了把 Java 中的重载带入 Python，在一个类中为同一个方法定义多个重载变体，比在一个函数中使用一长串 if/elif/elif/elif 块要好。有点就是支持模块化的扩展，每个模块都可以为它支持的各个类型注册一个专门的函数。
```

### 7.9 叠放装饰器

**以下两种写法等价**

```python
@d1
@d2
def f():
    print(f.__name__)
```

```python
def f():
    print(f.__name__)

f = d1(d2(f))
```

### 7.10 参数化装饰器

```python
import time

DEFAULT_FMT = '{elapsed:0,8f}s, {name}'

# 只需要在外面再包一层即可
def clock(fmt=DEFAULT_FMT)：
    def decorate(func):
        def clocked(*args, **kwargs):
            t0 = time.time()
            result = func(*args, **kwargs)            
            elapsed = time.time() - t0
            info = DEFAULT_FMT.format(
                elapsed=elapsed,
                name=func.__name__
            )
            return result
        return clocked
    return decorate           
```

**本书作者认为：装饰器最好通过实现 `__call__`方法的类来实现，类装饰器具有灵活度大、高内聚、封装性等优点。下面是实现方式**

```python
import time

class Clock:
    def __init__(self, func):
        self._func = func
        
    def __call__(self, *args, **kwargs):
        t0 = time.time()
        result = self._func(*args, **kwargs)
        elapsed = time.time() - t0
        print(f'本地调用运行时间：{elapsed}s')
        return result

@Clock
def f1():
    time.sleep(5)
```














































