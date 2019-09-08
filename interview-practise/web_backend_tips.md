## REVIEW OF WEB_BACKEND（阿菜2019年自制面经）

------------------
### 1. 说一下GET请求和POST请求之间的区别
[Yahoo 网站性能优化,但是有人说这个get代替post优化网站性能是有问题的，还没有进行考证](https://segmentfault.com/a/1190000000353790)

[与Yahoo结论相悖的一篇博文](https://mp.weixin.qq.com/s?__biz=MzI3NzIzMzg3Mw==&mid=100000054&idx=1&sn=71f6c214f3833d9ca20b9f7dcd9d33e4#rd)

    1. GET请求一般都把请求参数放在url里面，POST请求一般都把请求参数放在请求体里面。但是也并不是说GET请求不能有请求体，POST请求不能把参数放在URL里面。
    
    2. GET请求的URL是UrlEncode编码方式，但是POST有多种编码方式。
    
    3. GET在浏览器回退时时无害的，POST在浏览器回退的时候会再提交。
    
    4. GET请求会被浏览器主动cache,保存在浏览器的历史浏览数据里面。但是POST请求不会，除非手动设置。
    
    5. HTTP协议规范并没有对GET请求URL长度进行限制，这个限制是特定的浏览器以及服务器对它的限制。IE浏览器URL长度的处理就是2K+35。Chrome对URL的最大处理长度是。APACHE能接受的最长8192个字符。
       HTTP协议规范也没有对POST请求体进行大小限制，起到限制作用的是服务器处理程序的处理能力。Tomcat里面可以配置理POST请求的最大能力。
    
    6. 多数的浏览器在POST请求的时候，分成两部分headers+data。在GET请求的时候，headers+data一起发送的。所以才说POST请求一次会产生两个TCP数据包，但是GET请求一次会产生一个TCP数据包。但是并不是所有的浏览器都是这样的，比如FireFox的POST请求就只发送一次。所以理论上说，GET请求比POST请求的网络耗时更加少。

------------------
### 2. 说一下浏览器的缓存机制(HTTP缓存机制)

[腾讯前端工程师讲解浏览器缓存，条理清晰，建议阅读](https://juejin.im/entry/5ad86c16f265da505a77dca4)

[理解expires和Cache-Control这里看](https://segmentfault.com/a/1190000016199807)

##### 浏览器的缓存机制实际上是根据HTTP报文的缓存标识进行的
    1. 浏览器每次发起请求都会先去浏览器缓存中查找请求的结果以及缓存标识。
    2. 浏览器每次拿到返回的请求结果都会将结果和缓存标识存进浏览器缓存中去。
    3. 我们根据是否需要向服务器重新发起请求，将缓存过程分为两个部分，分为是强制缓存和协商缓存。

#### 强制缓存
    1. 发起HTTP请求，如果浏览器缓存中没有该请求的缓存结果和缓存标识，浏览器就会向Server发起一次HTTP请求。

    *2. 发起HTTP请求，如果浏览器缓存中存在该请求的请求结果和缓存标识，但是，该请求的缓存结果失效，浏览器缓存只返回缓存标识。浏览器就会携带该资源的缓存标识，向Server再发起一次Http请求。也就是说，这一次使用的是协商缓存。
    
    3. 发起HTTP请求，如果浏览器缓存中存在该请求的缓存结果和缓存标识，且都没有失效，就会直接返回该结果。

*当浏览器向服务器发起HTTP请求的时候，服务器会将缓存规则放在HTTP响应报文的请求头当中，与，请求结果一起返回给浏览器。控制强制缓存的字段是Expires和Cache-Control(exp.max-age=600)，后者的优先级高于前者，就是说600s内发起请求都是直接拿缓存里的内容*

#### 协商缓存
    1. 发起HTTP请求，如果浏览器缓存中存在该请求的请求结果和缓存标识，但是，该请求的缓存结果失效，浏览器缓存只返回缓存标识。浏览器就会携带该资源的缓存标识，向Server再发起一次Http请求。如果Server返回304，意思就是该资源无更新，浏览器就会向浏览器缓存获取该请求的缓存结果。
    
    2. 如果Server该资源更新了，就会返回200，以及该次请求的请求结果。然后浏览器会将该次请求结果和请求标识存在浏览器缓存当中。

*在使用强制缓存失效以后，浏览器就会携带缓存标识向服务器发起请求，由服务器的缓存标识决定是否使用缓存的过程。(Last-Modified / If-Modified-Since和Etag / If-None-Match，其中Etag / If-None-Match的优先级比Last-Modified / If-Modified-Since高。)*

#### 内存缓存和硬盘缓存
    1. 内存缓存：将编译解析以后的文件直接存在该进程的内存文件中，占据该进程一定的内存资源，方便下次运行使用时进行快速地读取。

    2. 硬盘缓存：直接将缓存写入硬盘文件中。
    在浏览器中，js和图片等文件解析执行以后直放在内存缓存当中，css文件则会直接存在硬盘缓存中，每次渲染页面都需要从硬盘获取缓存。
     
------------------
### 3. URL编码
    1. 一般来说，URL只能使用英文字母、阿拉伯数字和某些标点符号，不能使用其他文字和符号。
    2. 如果URL中有汉字，就必须编码后使用。
    3. 结论1: 网址路径，用的是utf-8编码。
    4. 结论2: 查询字符串的编码，用的是操作系统的默认编码
    5. 结论3: GET和POST方法的编码，用的是网页的编码。
[一个台湾老教授的博客](http://xml-nchu.blogspot.com/search/label/%E5%BF%83%E5%BE%97)

[阮一峰大神的解释](http://www.ruanyifeng.com/blog/2010/02/url_encoding.html)
##### 老实说我也不知道这个规则现在还适用不适用了，先放在这里吧，有时间做实验。

------------------
### 4. 说一下cookies和session的区别
[新浪前端技术专家写的cookie到底是什么](http://tech.sina.com.cn/i/csj/2013-03-18/19428157177.shtml)

+ 重点
    + 原本session是一个抽象的概念，开发者为了实现中断和继续等操作，将user-agent和server之间一对一的交互，抽象为”会话“。进而衍生出会话状态，
    也就是session的概念。
        + 1. cookie是一个实际存在的东西，http协议定义在header中的字段，可以认为是session的一种后端无状态实现。
        + 2. 而我们今天常说的session是为了绕开cookies的各种限制，通常借助cookie本身和后端存储实现的，一种更高级的会话状态的实现，
        + 3. session是因为sessionid的存在，需要借助cookie实现，但是这并非必要，只是通用性较好的一种实现。

##### Session的客户端实现形式(SessionID的保存方法)
    1. 使用Cookie来保存，服务器通过设置Cookie的方式将SessionID发到客户端上。如果我们不设置过期时间，那么这个Cookie将不会存在硬盘上，浏览器关闭以后这个这个Cookie就消失了。
    
    2. 使用URL附加信息的方式，就像我们经常看见的JSP网站会有的aaa.jsp?JSESSIONID=*是一样的，这种方式就和第一种方式里面不设置过期时间是一样的。

    3. 在页面表单里面增加隐藏域，后者通过POST方式发送数据。

##### Session和Cookie的区别和联系
    最大的区别还是一个放在服务器上面，一个放在客户端里。

------------------
### 5. cookie的应用
    1. cookie里面可能会存放一些用户的基础信息，比如说用户名，这样在切换页面的时候，就能在页面上显示用户的名字。当然还有其他的信息什么的。
    2. 存放用户浏览的信息，放在cookie里面，给到广告主，帮助广告主精准投放广告。

------------------
### 6. Response里的headers里的Set-Cookie各个字段的作用
[详解cookie里面的各个字段的作用](http://bubkoo.com/2014/04/21/http-cookies-explained/)

    1. expires: 指定了浏览器何时删除cookies,如果设置了一个过去的时间，将会马上被删除。
```python
    	
    Set-Cookie: name=Nicholas; expires=Sat, 02 May 2009 23:38:25 GMT
```
    2. domain: 指定了cookie将要被发送到哪个/哪些域里面。浏览器会将domain的值去和请求的域名做一个尾部比较。sina可能会有好几个域名，比如说:a.sina.com/b.sina.com, 在cookies里面带上这个字段以后就会匹配到所有的sina.cn的这个字段。所以这就是分布式很多台机器上都可以拿到cookies的原因了。
```python
    Set-Cookie: name=Nicholas; domain=nczonline.net
```
    3. path: 指定了 请求资源的URL 里面必须存在指定的路径的时候，才会在headers里面发送cookies。这个匹配采用的是字符的逐个匹配，所以说下面这个例子也会匹配URL里面有/blogrool的。注意：肯定是先核实的domain。
```python
    Set-Cookie:name=Nicholas;path=/blog
```
    4. secure: 只是一个标记，没有值。只有当一个请求是通过SSL和HTTPS创建时，包含secure选项的cookies才能被发送至服务器。
```python
    Set-Cookie: name=Nicholas; secure
```
**cookie的整个机制本来就是不安全的，所以机密和敏感的信息不应该在cookie中传输或者是传送。在HTTPS连接上传输的cookie都会被自动加上secure选项**

------------------
### 7. Cookies的覆盖情况
    1. name:same; expires:diff; domain:same; path:same;     # 覆盖
    2. name:same; expires:same; domain:same; path:diff;     # 覆盖(如果先/path_1;再/;就不会进行覆盖，但是调换顺序就会覆盖，我也不知道这是为什么。)
    3. name:diff; expires:same; domain:same; path:same;     # 不覆盖
    4. 稍微试了一下 也没有把规律试出来 好累啊！！！

------------------
### 8. 说一下通常的网络模型有几层，以及各层的意思和协议
    1. OSI七层模型，由下至上有：物理层、数据链路层、网络层、传输层、会话层、表示层、应用层
    2. TCP/IP模型，由下至上有：网络接口层、网络层、传输层、应用层
    3. 教学中的五层模型，由下至上有：物理层、数据链路层、网络层、传输层、应用层
##### 各层的职责
    1. physical layer: 底层的数据传输，如网线，网卡标准。
    2. data link layer: 定义数据的基本格式，如何传输，如何标示，如网卡的MAC地址。
    3. network layer: 定义IP编址，定义路由功能，如不同设备的数据转发、IP。
    4. transport layer: 端到端传输设备的基本功能，如TCP/UDP。
    5. session layer: 控制应用程序之间的会话能力，如不同的软件数据分发给不同的软件。
    6. presetation layer: 数据格式标识，基本压缩加密功能。
    7. application layer: 各种应用软件，包括web应用，有：HTTP FTP TELNET。

------------------
### 9. 在浏览器地址栏输入一个URL后回车，背后会进行哪些技术步骤？
[我靠，竟然找到一个大神的回答，再次感慨，google是真的好用啊！！！！](https://github.com/skyline75489/what-happens-when-zh_CN)
    
    1. 浏览器会判断输入的是URL还是关键字，当协议或者主机名不合法的时候，就会当成关键字传给默认的搜索引擎。

    2. 转换非ASCII码的Unicode字符，进行编码（URLEncode）
    
    3. 浏览器会检查自带的HSTS(HTTP Strict Transport Protocal)，这个东西里面存的是那些只允许浏览器使用HTTPS协议的网站。即使有些网站不在HSTS中，浏览器第一次发出的请求也是使用的HTTP,网站返回浏览器只能使用HTTPS的请求。
    
    4. DNS查询；
        1. 首先检查域名是否在Chrome的缓存中
        2. 缓存中没有的话就先去找是不是在自己本地的hosts文件里面
        3. 如果hosts文件里面没有，就会向DNS服务器发送一条请求进行查询
            a. 查询本地DNS服务器
            b. 如果DNS服务器和我们的本机在同一个子网下面，系统会DNS服务器进行ARP查询
            c. 如果DNS服务器和我们的本机不在同一个子网下，系统会按照一下的ARP过程对默认网关进行查询
        4. ARP(Address Realize Protocal)过程 这个过程有点复杂了，待我整理一下。

-------------------------
### 10. 说一下cookie，session，token的区别是什么
    pass
-------------------------
### 11. 说一下怎么解决跨域的问题？
    设置一个代理

-------------------------
### 12. 说一下RESTful规范
    pass
