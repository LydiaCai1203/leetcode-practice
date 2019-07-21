## REVIEW OF DJANGO（阿菜2019年自制面经）

[无意中看到的一个讲django2.*的书](https://djangobook.com/)

------------
### 1. 说一下你对Django的MVC模式的理解
#### 先说一下对MVC的理解：
    1. 位于最上层的View层，这是直接面向用户的，提供给用户操作界面，是程序的外壳。
    2. 最下面的一层Model层，也就是程序需要操作的数据和信息。
    3. 中间的一层就是controller层，根据用户从视图层输入的指令，选取数据层的数据，然后对其进行相应的操作，最后产生结果。
#### Django有他自己的逻辑，通常被称为MTV框架：
    1. Django将MVC中的视图层分为两部分，一部分是Template，一部分是views（也就是Django的视图），分别是如何展现 和 展现哪些数据。
    2. Model层还是Django中的model是一样的，是程序需要操作的数据和信息。
    3. Controller在Django中由它的URLConf,其机制使用的是正则表达式来匹配url,然后去调用合适的Python函数。

-------------
### 2. 你是否使用过Django中的middelware
    1. Middleware的作用是request和response的，或者说你想在views之前执行一些操作，也可以使用Middleware。
    2. Middleware也是有执行顺序的，先后顺序一定要注意，比如过session中间件必须在auth之前被执行到。

-------------
### 3. 当发一个请求给Django的时候，Django内部的一个执行流程是什么样子的
    pass

-------------
### 4. 说一下发送请求，从服务器本地网卡开始，到Django的一个整体的执行流程是什么样子的
    pass

-------------
### 5. 给你一个Model Class，然后把在MySQL中的表结构反推出来
    pass

-------------
### 6. 直接用Django的ORM写查询语句
    pass

-------------
### 7. 说一下Django的ORM中的class里面metaclass的用处，还有一个什么abstract=True是什么意思
```python
class User(object):
    pass

class Student(User)：
    pass
# 这里面的继承我都还没有用到过找时间看
```
