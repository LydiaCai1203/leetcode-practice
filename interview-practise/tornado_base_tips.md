## Tornado 面试基础

### 1. Tornado 是什么？

```markdown
Tornado 是一个 Python web 框架和异步网络库，通过使用非阻塞网络 IO，Tornado 可以支持上万级的连接，处理 长连接、websockets 和 其他需要与每个用户保持长久连接的应用。使用它在处理严峻的网络流量时表现得足够强健，但却在创建和编写时有着足够的轻量级。

下次想想如何从三个方面来说：
1. 速度
2. 简单
3. 可扩展性
```

### 1. Tornado 同步/异步 调用

**可以使用基准工具测试：siege http://localhost:8000/?q=pants -c10 -t10s**

```python
# 同步调用
client = tornado.httpclient.HTTPClient()
response = client.fetch(
    "http://search.twitter.com/search.json?" + \
    urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100})
)
body = json.loads(response.body)

# 异步调用
@tornado.web.asynchronous
def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    client.fetch(
        "http://search.twitter.com/search.json?" + urllib.urlencode(
        {"q": query, "result_type": "recent", "rpp": 100}),
        callback=self.on_response
    )
def on_response(self):
    ...
    self.finish()
```

### 2. 异步装饰器和 finish 方法

```markdown
Tornado 默认在函数处理返回时关闭客户端的连接，但是在使用回调函数的异步请求时，需要连接保持状态直到回调函数执行完毕。因此 `@tornado.web.asynchronous` 就是保持连接开启，Tornado 不会自己关闭连接了，必须要调用 `finish()` 显示关闭连接。
```

### 3. 异步生成器

 [官方文档更多用法](https://www.tornadoweb.org/en/stable/gen.html)

```python
@tornado.web.asynchronous
@tornado.gen.engine
def get(self):
    client = tornado.httpclient.AsyncHTTPClient()
    # yield 返回程序对 tornado 的控制，允许在 http 请求过程中执行其他任务
    # 当 http 请求完成时，requesthandler 在其停止的地方恢复。
    response = yield tornado.gen.Task(
        client.fetch,
        "http://search.twitter.com/search.json?" + urllib.urlencode(
        {"q": query, "result_type": "recent", "rpp": 100})
    )
    body = json.loads(response.body)
    ....
    self.finish()       
```

### 4. 使用 Tornado 进行长轮询

```markdown
场景：
web 应用需要更新用户状态、发送新消息提醒, 等等。最常见的一个利用就是在线同步写作文档、web qq 等等。

解决方案：
1. 早期是浏览器以一个固定的时间间隔向服务器轮询新请求。这样会有一个问题，就是轮询频率必须足够快，数据才能最及时最新。但是又不能态频繁，这样的话 web 服务器扛不住。
2. "服务器推送" 技术允许 web 应用实时发布更新，同时保持合理的资源使用，确保可预知的扩展。最流行的技术是让浏览器发起连接模拟服务器推送更新。这种 http 连接被称为 长轮询。就是说，浏览器启动一个 http 请求，服务器端也保持开启，浏览器等待服务器推送数据过来，然后服务器返回响应并关闭连接后。浏览器再打开一个请求，然后等待即可。

长轮询的缺点：
1. 对于浏览器请求超时间隔无法控制
2. 许多浏览器限制了对于打开的特定主机的并发请求数量。当有一个连接保持空闲时，剩下的用来下载网站内容的请求数量就会有限制
3. 对于购物车这样的应用，在库存变化时所有的推送请求会同时应答和关闭，这样浏览器建立新请求时对服务器也是猛烈的攻击...
```

*长轮询实战：*

```python
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppingCart(object):
    """维护库存中商品的数量，把商品加入购物车的购物者列表"""
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for c in self.callbacks:
            self.callbackHelper(c)

        self.callbacks = []

    def callbackHelper(self, callback):
        callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

class DetailHandler(tornado.web.RequestHandler):
    """用来渲染 html"""
    def get(self):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
    """用于操作购物车的接口"""
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)

class StatusHandler(tornado.web.RequestHandler):
    """用于查询全局库存变化的通知"""
    # 这个装饰器使得 get 方法返回时不会关闭连接
    @tornado.web.asynchronous
    def get(self):
        self.application.shoppingCart.register(
            # 使用 async_callback 确保回调函数引发的异常不会使得 requesthandler 关闭连接，不过这只在 1.1 之前是显示必须的，新版本中不需要
            self.async_callback(self.on_message)
        )

    def on_message(self, count):
        self.write('{"inventoryCount":"%d"}' % count)
        self.finish()

class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
```

### 5. Tornado 和 Websockets

```markdown
websocket 协议提供了在客户端和服务器间持久连接的双向通信，协议本身使用 ws://URL 格式，通过使用 http 和 https 端口。
```

*实战*

```python
# 当一个新的 websocket 连接打开时，open 方法被调用，on_message 和 on_close 分别会在连接接收到新的消息和客户端关闭时被调用。
class EchoHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message('connected!')

    def on_message(self, message):
        self.write_message(message)
```

*购物车实战*

```python
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.options
from uuid import uuid4

class ShoppingCart(object):
    totalInventory = 10
    callbacks = []
    carts = {}

    def register(self, callback):
        self.callbacks.append(callback)

    def unregister(self, callback):
        self.callbacks.remove(callback)
        
    def moveItemToCart(self, session):
        if session in self.carts:
            return

        self.carts[session] = True
        self.notifyCallbacks()

    def removeItemFromCart(self, session):
        if session not in self.carts:
            return

        del(self.carts[session])
        self.notifyCallbacks()

    def notifyCallbacks(self):
        for callback in self.callbacks:
            callback(self.getInventoryCount())

    def getInventoryCount(self):
        return self.totalInventory - len(self.carts)

class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        session = uuid4()
        count = self.application.shoppingCart.getInventoryCount()
        self.render("index.html", session=session, count=count)

class CartHandler(tornado.web.RequestHandler):
    def post(self):
        action = self.get_argument('action')
        session = self.get_argument('session')

        if not session:
            self.set_status(400)
            return

        if action == 'add':
            self.application.shoppingCart.moveItemToCart(session)
        elif action == 'remove':
            self.application.shoppingCart.removeItemFromCart(session)
        else:
            self.set_status(400)

class StatusHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.application.shoppingCart.register(self.callback)

    def on_close(self):
        self.application.shoppingCart.unregister(self.callback)

    def on_message(self, message):
        pass
        
    def callback(self, count):
        self.write_message('{"inventoryCount":"%d"}' % count)

class Application(tornado.web.Application):
    def __init__(self):
        self.shoppingCart = ShoppingCart()

        handlers = [
            (r'/', DetailHandler),
            (r'/cart', CartHandler),
            (r'/cart/status', StatusHandler)
        ]

        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }

        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
```

### 6. tornado 的事件循环机制

[深入解析 tornado ioloop 源码](https://segmentfault.com/a/1190000005659237)

[官方文档](https://tordoc.readthedocs.io/zh_CN/master/guide/async.html)




