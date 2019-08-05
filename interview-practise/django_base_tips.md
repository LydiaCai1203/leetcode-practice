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
[Django执行流程](https://juejin.im/post/5a6c4cc2f265da3e4c080605)
[WSGI](https://www.jianshu.com/p/679dee0a4193)
    
#### 执行启动命令 python manage.py runserver；这条命令使用的是Django自带的web server, 主要用于开发和调试。正式环境中会使用nginx和uwsgi模式。
    1. 无论是哪种方式都会创建一个WSGIServer对象，接受用户的请求。
    2. 当一个用户的请求到达的时候，会为用户指定一个WSGIServer, 用于处理用户请求与响应，这个handler是处理整个request的核心。

#### WSGI 全称是Web Server Gateway Interface 这个东西并不是服务器 也不用于与程序交互的API 只是定义了一个接口 用于描述Web Server 和 Web Application之间的通信规范的。
    1. 当客户端最先发送一个请求的时候，最先处理请求的其实是我们经常说的Apache和Nginx之类的服务器。
    2. web服务器会再把请求交给web application 进行处理。这中间的中介就是WSGI，它把web server和 web application连接起来了。

#### 中间件 是位于Web Server 和 Web Application之间的，它可以添加额外的功能
    1. 对来自用户的数据进行预处理 然后再发给Wen Application
    2. 应用将响应负载返回给用户之前，对结果数据进行一些最终的调整

#### 数据流 前面说过的WSGI Handler，这个东西控制了从请求到响应的整个过程
    1. 导入settings配置和Django异常类
    2. 加载settings的中间件类
    3. 创建request, view, response, 和 exception_middleware 四个列表。
    4. 现在遍历request_middleware列表，对request进行预处理。
    5. 解析url进行匹配
    6. 遍历view_middleware列表，对view进行一些预处理
    7. 实现view逻辑
    8. 如果引发异常 就循环遍历exception_middleware
    9. 遍历response_middleware，对response进行初始化，然后返回response

[流程图]()
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
