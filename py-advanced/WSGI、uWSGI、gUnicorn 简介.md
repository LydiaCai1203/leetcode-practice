# WSGI、uWSGI、Gunicorn 简介与简单应用

首先祭出最重要的，有请我们的官方文档。

[wsgi](https://wsgi.readthedocs.io/en](https://wsgi.readthedocs.io/en) | [uwsgi](https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/](https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/) | [gunicorn](https://docs.gunicorn.org/en/stable/run.html)

## WSGI

### 一、什么是 WSGI

WSGI 是 Web Server Gateway Interface. 它具体描述了 web server 如何与 web application 沟通的方式，以便与让这些 web application 可以串联在一起去处理一个网络请求。

### 二、不明觉厉，但是不懂，接下去查

1. WSGI 不是一个 server, 不是一个 python module, 不是一个 framework, 不是 API，也不是软件。它仅仅只是一个接口定义，定义了 server 与 application 之间的通讯格式。如果一个 application 是按照 WSGI 规范写的，它则可以在任何 server 上运行。

2. 符合 WSGI 的程序，被夹在 application 和 server 中间，称为所谓的 middleware. 它不仅仅要实现 WSGI 接口，还要实现分别面向 application 和 server 的那两面。对于这个程序的上面，表现的像个 server. 下面则表现的像个 application.

3. 一个符合规范的 WSGI 服务，只会做两件事情，一个是接收来自客户端的请求，通过 WSGI 服务 发送给 application. 一个是将 application 返回的响应发送给客户端。所以麻烦恶心的细节都由 application 或 middleware 实现。

### 三、ok, 不就是个规范么。康康 Application 的基础实现吧

+ application 必须是一个 可调用的对象，比如一个函数，比如一个类，比如一个实现了 `object.__call__()`的实例。

+ 必须要接收两个位置参数，
  
  + 一个 包含了 CGI 变量的 dict (CGI 公共网关接口 )
  
  + 一个被 application 用来发送 HTTP status 和 HTTP headers 给 server 的回调函数

```python
def application(environ, start_response):
    response_body = 'Request method: %s' % environ['REQUEST_METHOD']
    status = '200 ok'
    response_headers = [
         ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    # Send them to the server using the supplied function
    start_response(status, response_headers)
    return [response_body]
```

可以看到 application 做了两件事，通过 CGI 环境变量拿到本次请求的一些信息，然后将处理封装成请求体再返回给 server。

#### 3.1 CGI 是什么

CGI 是 Web 服务器 和 运行其上的应用程序进行 “交流” 的一种约定。CGI 早期的出现是为了解决 Web 服务器 与 外部应用程序 之间进行数据互通。

CGI 是 Web 服务器 和 一个独立的进程  之间的协议。它会把 HTTP 请求 和 其 header 射程进程的环境变量，HTTP 请求的 body 设置成进程的标准输入，进程的标准输出设置为 HTTP 响应。  

Web 服务器 一般只用来处理静态文件的请求，一旦碰到动态脚本的请求，Web 服务器主进程就会 fork 一个新的进程来启动 CGI 程序，将动态脚本交给 CGI 程序处理。CGI 程序回去接续动态脚本，然后将结果返回给 Web 服务器，最后由 Web 服务器将结果返回给客户端，之前 fork 出来的进程也会关闭。

 进程的不断 fork 开销是非常大的，后来就出现了 Fast-CGI，其实就是常驻型的 CGI，在请求到达的时候不会耗费时间去 fork 一个进程来处理。

### 四、Environment Dictionary

```python
from wsgiref.simserver import make_server

def application(environ, start_response):
    response_body = [
        '%s: %s' % (key, value) for key, value in sorted(environ.items())
    ]
    response_body = '\n'.join(response_body)
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]

httpd = make_server(
    'localhost',
    8051,
    application
)

httpd.handle_request()
```

可以大概看到一些信息，request_method , content_type, 不过似乎没看见请求参数。

### 五、Response 可迭代对象

在老机器上，把 return [response] 替换为 return response，会发现返回的时候特别慢，因为服务器会遍历字符串，每次就向客户端发送一个字节。为了更好的性能，把请求包装成一个可迭代对象，性能会更高。

### 六、解析请求 - GET

当 `REQUEST_METHOD` 是 `GET` 时，就会有一个 `QUERY_STRING`, 里面的内容是 URL 问号之后的内容。你可以写程序去解析查询参数，更简单的方式是使用 `cgi.parse_qs()` , 不过现在的 `parse_qs` 这个方法在 `urllib.parse.parse_qs` 中。

```python
In [4]: parse_qs('name=caiqj&age=26')
Out[4]: {'name': ['caiqj'], 'age': ['26']}
```

用户输入始终是不安全的。要对用户传入的 query_string 进行清理，以防止脚本注入。比如 `html = '&lt;abc&gt'`  使用了 `escape(html)` 则会返回 `<abc>`

```python
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape

html = """
<html>
<body>
   <form method="get" action="">
        <p>
           Age: <input type="text" name="age" value="%(age)s">
        </p>
        <p>
            Hobbies:
            <input
                name="hobbies" type="checkbox" value="software"
                %(checked-software)s
            > Software
            <input
                name="hobbies" type="checkbox" value="tunning"
                %(checked-tunning)s
            > Auto Tunning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: %(age)s<br>
        Hobbies: %(hobbies)s
    </p>
</body>
</html>
"""

def application (environ, start_response):

    # Returns a dictionary in which the values are lists
    d = parse_qs(environ['QUERY_STRING'])

    # As there can be more than one value for a variable then
    # a list is provided as a default value.
    age = d.get('age', [''])[0] # Returns the first age value
    hobbies = d.get('hobbies', []) # Returns a list of hobbies

    # Always escape user input to avoid script injection
    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % { # Fill the above html template in
        'checked-software': ('', 'checked')['software' in hobbies],
        'checked-tunning': ('', 'checked')['tunning' in hobbies],
        'age': age or 'Empty',
        'hobbies': ', '.join(hobbies or ['No Hobbies?'])
    }

    status = '200 OK'

    # Now content type is text/html
    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

httpd = make_server('localhost', 8051, application)

# Now it is serve_forever() in instead of handle_request()
httpd.serve_forever()
```

### 七、解析请求 - POST

POST 的请求体位于 WSGI 服务器提供的 WSGI.input 文件中，类似于环境变量。

```python
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
from html import escape

html = """
<html>
<body>
   <form method="post" action="">
        <p>
           Age: <input type="text" name="age" value="%(age)s">
        </p>
        <p>
            Hobbies:
            <input
                name="hobbies" type="checkbox" value="software"
                %(checked-software)s
            > Software
            <input
                name="hobbies" type="checkbox" value="tunning"
                %(checked-tunning)s
            > Auto Tunning
        </p>
        <p>
            <input type="submit" value="Submit">
        </p>
    </form>
    <p>
        Age: %(age)s<br>
        Hobbies: %(hobbies)s
    </p>
</body>
</html>
"""

def application(environ, start_response):

    # the environment variable CONTENT_LENGTH may be empty or missing
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    # When the method is POST the variable will be sent
    # in the HTTP request body which is passed by the WSGI server
    # in the file like wsgi.input environment variable.
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)

    age = d.get('age', [''])[0] # Returns the first age value.
    hobbies = d.get('hobbies', []) # Returns a list of hobbies.

    # Always escape user input to avoid script injection
    age = escape(age)
    hobbies = [escape(hobby) for hobby in hobbies]

    response_body = html % { # Fill the above html template in
        'checked-software': ('', 'checked')['software' in hobbies],
        'checked-tunning': ('', 'checked')['tunning' in hobbies],
        'age': age or 'Empty',
        'hobbies': ', '.join(hobbies or ['No Hobbies?'])
    }

    status = '200 OK'

    response_headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

httpd = make_server('localhost', 8051, application)
httpd.serve_forever()
```

## uWSGI

[请求缓存方案](https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/tutorials/CachingCookbook.html#cache-them-all)

### 一、什么是 uWSGI

github 上提到 uWSGI application server container

刚刚已经了解到 WSGI 是一个 Web Server Gateway Interface, 是连接 server 和 application 之间的桥梁。很多现有流行的 web 框架都是自带 WSGI Server 的，但是性能都不好，只是为了服务测试所用的。

那么实际上，uWSGI Server 是一个实现了 uwsgi 协议的 server。

### 三、先写一个 WSGI Application

```python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return ["Hello World"]
```

### 四、 启动服务

```python
uwsgi --http :9090 --wsgi-file app.py
```

### 五、如果你想要添加并发和监控的话，你可以用

```python
uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2

uwsgi --http :9090 --wsgi-file foobar.py --master --processes 4 --threads 2 --stats 127.0.0.1:9191
# 向你的应用发送几个请求然后 telnet 到 9191 端口，你将得到大量有趣的信息。你可能想要使用 “uwsgitop” (使用 pip install 你就能得到它)，这是一个类似 top 的工具，用于监控应用实例。
```

### 六、可以放到一个完整的 web 服务器后面去

即使 uWSGI HTTP router 是一个可靠的高性能服务器，你可能还是想把你的应用放到一个完整的 web 服务器后面去。比如 Nginx。我觉得这句话的意思就是，其实有 uwsgi 就不需要 nginx 了。

### 七、部署 Django

[Django+Nginx+uWSGI](https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/tutorials/Django_and_nginx.html)

假定你的 Django 项目在 /home/caiqingjing/myproject 下

```ini
socket = 127.0.0.1:3031
chdir = /home/foobar/myproject/
wsgi-file = myproject/wsgi.py
processes = 4
threads = 2
stats = 127.0.0.1:9191   # 查看日志用的
```

然后你就可以运行它了

·`uwsgi yourfile.ini`

### 八、部署 Flask

Flask 把它的 WSGI Application 直接暴露成 app, 所以我们需要告诉 uWSGI 

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"
```

然后你就可以运行它了

`uwsgi --socket 127.0.0.1:3031 --wsgi-file myflaskapp.py --callable app --processes 4 --threads 2 --stats 127.0.0.1:9191`

[挂载多个 flask app](https://uwsgi-docs-cn.readthedocs.io/zh_CN/latest/Snippets.html)

### 九、部署 Tornado

这就涉及到我这几天遇到一个很有意思的事情了，当时我和豪哥正在沟通项目的部署方案，我的部署方案是 Tornado + Supervisor + Nginx，但是豪哥还是坚持问我是否有别的部署方案。我想起来之前开会的时候，豪哥和黑哥都说一般用 uWSGI 来部署。哦，原来它们都不知道 Tornado 不是 WSGI 应用啊。

Tornado 通常是独立运行的，不需要一个 WSGI 容器。Tornado 自带了多进程启动方案，但是有一些局限性，比如多个进程使用的是一个端口。官方推荐使用的是 supervisor 的进程组进行管理。同样的，复杂均衡你还是可以使用 Nginx。

不过还是会有用到 uWSGI 部署的地方，比如 Google App Engine，只运行 WSGI。应用程序不能独立运行自己的服务。在这种情况下，Tornado 支持一个有限制的操作模式，不支持异步操作，不支持 协程、@asynchronous、AsyncHttpClient、auth 模块，和 WebSockets.

```python
import tornado.web
import tornado.wsgi

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

tornado_app = tornado.web.Application([
    (r"/", MainHandler),
])
application = tornado.wsgi.WSGIAdapter(tornado_app)
```

我真的很想吐槽，我有问题，豪哥那说话的态度，和我提出他的问题，他就一副不服的样子。有错就承认自己的错，不说话算什么意思，别人又不知道你听明白了没有。每次都很来气，到后来我和他说话，他指出我的问题我也开始火气很大。

如果你非要用 uWSGI 部署 Tornado 参考下列链接

[uWSGI 与 Tornado 集成](https://tornado-zh.readthedocs.io/zh/latest/wsgi.html#running-tornado-apps-on-wsgi-servers](https://tornado-zh.readthedocs.io/zh/latest/wsgi.html#running-tornado-apps-on-wsgi-servers)

## Gunicorn

### 一、Gunicorn 是什么

github 上提到 gunicorn 'Green Unicorn' is a WSGI HTTP Server for Unix, fast clients and sleepy applications.

有了对 uWSGI 的理解，Gunicorn 你也应该能很快上手了。接下来说一下基础的简单的使用。

### 二、老规矩先写一个 WSGI Application

`gunicorn [OPTIONS] APP_MODULE`

Example with the test app:

```python
def app(environ, start_response):
    """Simplest possible application object"""
    data = b'Hello, World!\n'
    status = '200 OK'
    response_headers = [
        ('Content-type', 'text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])
```

### 三、现在你可以启动这个 app 了:

`gunicorn –workers=2 test:app`

当然也可以直接是一个创建应用的函数名

```python
def create_app():
    app = FrameworkApp()
    ...
    return app
```

`$ gunicorn --workers=2 'test:create_app()'`

位置参数 和 关键字参数 当然也可以被传递到函数里，但是从环境变量的配置文件里面加载 会好过于 从命令里面传入。怎么从命令行里面传直接看下文档吧。

### 四、部署 Django

如果你没有直接指明 application 的名字，Gunicorn 会寻找能被调用的 application 的名字。Django 就直接写上项目名就可以了。

`$ gunicorn myproject.wsgi`

当然你可以使用 `--env` 来指定 Django 的 settings 文件。用 `-pythonpath` 来指定 python 路径。

`gunicorn --env DJANGO_SETTINGS_MODULE=myproject.settings myproject.wsgi`

当然也是可以使用配置文件的

```ini
[server:main]
use = egg:gunicorn#main
host = 127.0.0.1
port = 8080
workers = 3
```

 `gunicorn --paste development.ini -b :8080 --chdir /path/to/project`

### 五、部署 Flask 不多说了，Tornado 别多想了。

### 六、Gunicorn 的设计艺术

[文档文档还是文档](https://docs.gunicorn.org/en/stable/design.html)

#### 6.1 Server Model

Gunicorn 是基于 pre-fork worker 模型设计的，这意味这，Gunicorn 有一个主进程，管理其它的 worker 进程。主进程不会知道任何和  inidividual clients 有关的事情，所有的请求         和响应都会被 worker 进程处理。

#### 6.2 Sync Workers

最基础和默认的 worker type 是 synchronous worker，也就是一个 worker 一个时间就请求一个单一请求。这个模型有一个简单的原因就是，如果出现一些攻击，至多也就影响一个请求。

sync worker 不支持持久话连接，每个连接都会在返回响应之后关闭，即使你已经在`headers`加上了 `Keep-Alive` 或者 `Connection: keep-alive` 。

#### 6.3 Master

主进程是一个简单的循环，它舰艇各种进程信号，并作出响应的反应，它通过监听 TTIN、TTOU、CHLD 等信号来管理正在运行的工作人员列表。TTIN 和 TTOU 会告诉主进程增加或减少 worker 的数量，CHIL 表示子进程已终止，主进程会自动重启失败的工作进程。

#### 6.4 Asynchronous Workers

async workers 基于 greenlet (通过 Eventlet 和 Gevent)。Greenlets 是 Python 多线程协作的实现。通常，一个应用使用这些 workers 并且不需要做任何更改。

#### 6.5 Tornado Workers

还格外提供了 Tornado worker 类，你可以用它来写 applications, 这些应用使用 Tornado 框架来写。因为 Tornado workers 是为了服务 WSGI application 服务的。官方文档说这里详细说明，我觉得意思就是，我不说，你也别用了。

#### 6.6 AsyncIO Workers

worker gthread是一个线程化的worker。它接受主循环中的连接，接受的连接作为连接作业添加到线程池中。On keepalive连接被放回循环中等待事件。如果keep alive超时后没有事件发生，则连接将关闭。懒得翻译了。

#### 6.7 Choosing a Worker Type

默认的 sync workers 假定你的应用在 CPU 和网络带宽方面收到了资源的限制。一般来说意味着应用程序不应该做任何 未定义时间 的事情，比如说网络请求就是一个花费时间不确定的事情。一些时候，加入外部网络出现问题，客户端的请求就会堆积在服务端，所以最好使用 async workers.

由于资源受限，事实上事实上所以我们需要在 Gunicorn 前面配置一个缓冲代理。

下面是使用 async worker 的一些情况

```python
Applications making long blocking calls (Ie, external web services)
Serving requests directly to the internet
Streaming requests and responses
Long polling
Web sockets
Comet
```

`(2  x  $num_cores)  +  1` number of workers is the best conf.
