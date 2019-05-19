## chapter15 上下文管理器和else块

##### with语句会设置一个临时的上下文，交给上下文管理器对象控制，并且负责清理上下文。

### 15.1 if 语句之外的 else 块
##### else 语句块不仅能和if搭配使用，还可以和for,while,try搭配使用
> 1. for
>> 仅当for循环执行完毕以后才会执行的语句块，前提是没有被break中止
> 2. while
>> 仅当while循环因为条件为假值而退出的时候才会执行的语句块，同上，没有被break中止
> 3. try
>> 仅当try块中没有异常抛出时才运行else语句块，但是else子句抛出的异常是不会被前面的except进行捕获的
**在所有情况下，如果异常，或者return,continue,break导致控制权跳到了复合语句的主块之外，else子句也会被跳过**
**在这里的else可以解释成then的意思，就是做完主语句块里面的事情，然后再说else语句块里的东西**
</br>

#### exaple1:
**这里使用else会方便很多，就不用再设置什么flag进行单独判断**
```python
import collections
Item = collections.nametuple('Item', 'flavor')

item_list = [Item('apple'), Item('peach')]
for item in item_list:
    if item.flavor == 'banana':
        break
else:
    raise ValueError('banana flavor is not existed.')
```
</br>

#### exaple2:
**try语句中应该只包含可能会超出预期的代码，所以aftercall其实不应该出现在try语句块中**
```python
try:
    dangrous_call()
    after_call()
except:
    pass
```
</br>

### 15.2 上下文管理器和with块
##### 上下文管理器对象存在的目的是管理with语句，就像迭代器的存在是为了管理for语句一样
##### with语句的目的是为了简化`try/finally`模式，这种模式用于保证一段代码运行完毕以后再执行某项操作, 即使是`try`里面进行了`return`,也依旧会执行`finally`语句，通常拿来释放资源用的

#### 上下文管理器协议：
> 1. `__enter__` 和 `__exit__`
> 2. `with`语句开始运行时，会在上下文管理器对象上调用`__enter__`，`with`语句结束后，会在上下文管理器对象上调用`__exit__`方法
> 3. `__enter__()`不一定返回上下文管理器对象，还可能是其它对象
> 4. 不管以何种方式退出with块，`__exit__()`都会被调用
> 5. with语句块的as子句是可选的，对于open函数来说，必须加上as语句，因为要获得文件的引用，但是有些上下文管理器会返回None,因为没有什么可以返回给用户的
</br>
```python
with open('test.txt') as fp:       # fp绑定到打开的文件上，因为文件的__enter__方法返回self
    src = fp.read(60)
print(fp.closed)
print(fp.encoding)                 # 在with块末尾，调用了TextIOWrapper.__exit__方法把文件给关闭了
```
**fp这里其实就是一个上下文管理器对象,fp就有__enter__()和__exit__()**
</br>
```python
class LookingGlass:
    def __enter__(self):
        '''
        除了self,这个函数不传入任何的参数
        '''
        import sys
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'asdfgh'

    def reverse_write(self, text):
        self.original_write(text[::-1])

    def __exit__(self, exc_type, exc_value, traceback):
        '''
        分别是异常类，异常实例或者是traceback对象
        '''
        import sys
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print('pleace do not divide by zero')
            return True
```
##### 重复导入模块并不会消耗太多的资源，因为python会缓存导入的模块
##### __exit__中传入的三个参数是如果发送了异常，这三个参数才会有值，否则为None
</br>

### 15.3 使用@contextmanager
#### example
```python
import contextlib

@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])
    
    sys.stdout.write = reverse_write
    
    msg = ''       # 记得要在这里捕获异常 不然的话之后标准输出流的内容就会出现错误
    try:
        yield 'asdfg'
    except ZeroDivisionError:
        msg = 'Please go not divide by zero!'
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)
```
##### @contextlib.contextmanager会把函数包装成实现__enter__和__exit__方法的类
##### __enter__
> 1. 调用生成器函数，保存生成器对象
> 2. 调用next(gen),执行到yield关键字所在的位置
> 3. 返回next(gen)产生的值，以便于把产出的值绑定到with/as语句中的目标变量上
##### __exit__
> 1. 检查有没有把异常传给exc_type, 如果有，调用gen.throw(exception)，在生成器函数定义体中包含yield关键字的那一行抛出异常
> 2. 否则，调用next(gen)，继续执行生成器函数定义题yield语句之后的代码
> 3. 为了告诉解释器异常已经处理了，__exit__会返回一个True，代表上下文处理器有能力处理这个异常，如果是False还是None，都会向上冒泡异常。
> 4. 当你使用装饰器的时候，装饰器提供的__exit__会假定发给生成器的所有异常都得到处理了，因此应该压制异常，所以我们应该在代码中显示地抛出异常
> 5. 所以说如果上下文管理器如果__exit__是返回的是异常，即使上下文管理器已经退出了，在with语句块之外还是会将这个异常抛出的，所以在__exit__中进行try/catch还是很有必要的！！！！！！！！！！
</br>

#### example
##### 这个包可以直接修改文件 但是并不被推荐使用
```python
import fileinput

for line in fileinput.input('demo.txt', inplace=True):
    line = 'additional line ' + line.rtrip('\n')
```