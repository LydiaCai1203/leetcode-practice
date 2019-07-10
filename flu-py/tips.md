## @property、@*.setter
### example(错误的例子)
```python
class Student(object):
    password = ''

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, value):
        self.password = value
```
#### 1. 加上了@property装饰器的函数变成了readonly的属性
#### 2. 加上了@*.setter装饰器的函数变成了read&write的属性
#### 3. self.password = value 也会调用@password=setter，所以会死循环，然后造成栈溢出
</br>
#### 正确的写法应该是
```python
class Student(object):
    password_hash = ''
    
    @property
    def password(self):
        return self.password_hash
    @password.setter
    def password(self, value):
        self.password_hash = md5(value)
```
