## chapter14 可迭代的对象、迭代器和生成器

> 1. 迭代器模式：当扫描内存中放不下的数据集时，我们要找到一种惰性获取数据项的方式，即按需一次获取一个数据项
> 2. 所有的生成器都是迭代器，因为生成器完全实现了迭代器的接口
> 3. 根据《设计模式：可复用面向对象软件的基础》书中的定义：
>> 1. 迭代器： 用于从集合中取出元素
>> 2. 生成器： 用于凭空生成元素
> 4. python中的`range`返回的是一个类似生成器的东西，但是并不是生成器，如果要求返回的是`list`,可以使用`list(range(5))`

### 14.1 Sentance第一版: 单词序列
```python
class Sentance:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(text)
    def __getitem__(self, index):
        return self.words[index]
    def __len__(self):
        return len(self.words)
    def __repr__(self):
        return 'Sentance{}'.format(reprlib.repr(self.text)
```
#### 序列可以迭代的原因:`iter函数`
> 1. 解释器需要迭代对象x的时候，会自动调用iter(x)
> 2. 