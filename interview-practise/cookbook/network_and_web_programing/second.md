# 创建 TCP 服务器

#### 一、创建 TCP 服务器

```python
from socketserver import BaseRequestHandler, TCPServer

class EchoHandler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        while True:

            msg = self.request.recv(8192)
            if not msg:
                break
            self.request.send(msg)


if __name__ == '__main__':
    serv = TCPServer(('', 20000), EchoHandler)
    serv.serve_forever()
```

#### 二、创建一个 TCP 客户端

```python
import time
from socket import socket, AF_INET, SOCK_STREAM

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 20000))
s.send(b'Hello')

s.recv(8192)
```

#### 三、创建一个类文件接口放置在底层Socket上的例子

```python
from socketserver import StreamRequestHandler, TCPServer


class EchoHandler(StreamRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # self.rfile is a file-like object for reading
        for line in self.rfile:
            # self.wfile is a file-like object for writing
            self.wfile.write(line)


if __name__ == '__main__':
    server = TCPServer(('', 20000), EchoHandler)
    server.serve_forever()
```

#### 四、最后

+ `socketserver` 默认情况下是单线程的，一次只能为一个客户端提供连接服务。如果想处理多个客户端，可以初始化一个 `ForkingTCPServer` 或者是 `ThreadingTCPServer` 对象。

+ 使用 `ForkingTCPServer` 和 `ThreadingTCPServer`会为每一个客户端连接创建一个新的进程或线程。由于客户端的连接是没有限制的，因此同一时刻大量的请求会让你的服务器崩溃。这种情况下可以预先分配一个线程池或者是进程池。

```python
from threading import Thread
from socketserver import BaseRequestHandler, TCPServer

NWORKERS = 16

def EchoHandler(BaseRequestHandler):

    def handle(self):
        print('Got connection from', self.client_address)
        while True:
            msg = self.request.recv(5120)
            if not msg:
                break
        self.request.send(b'recv finished')


if __name__ == '__main__':
    sevrer = TCPServer(('localhost', 20000), EchoHandler)
    for n in range(NWORKERS):
        t = Thread(target=server.serve_forever)
        t.daemon = True
        t.start()
    server.serve_forever()
```

+ 一般来说一个TCPServer在实例化的时候会绑定并且激活相应的 socket。有时候你想通过设置某些选项去调整底下的`socket`, 可以设置参数`bind_and_active=True`

```python
if __name__ == '__main__':
    server = TCPServer(('', 20000), EchoHandler, bind_and_activate=False)
    # set up various socket options
    serv.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # bind and activate
    server.server_bind()
    server.server_activate()
    server.serve_forever()
```

+ 下面是一个直接用`socket`编程的例子
  
  1. 计算机之间的数据传输方式
     
     1. SOCK_STREAM 表示面向连接的数据传输方式。数据可以准确无误地到达另一台计算机，如果损坏或丢失，可以重新发送，但是效率相对慢。常见 HTTP 协议就是使用的 SOCK_STREAM 传输数据，因为要确保数据的准确性，否则网页无法正常解析。
     
     2. SOCK_DGRAM 表示无连接的数据传输方式。计算机只管传输数据，不作数据校验，如果数据在传输中损坏，或者没有到达另一台计算机，是没有办法补救的。所以 SOCK_DGRAM 的效率比 SOCK_STREAM 的效率要高。
  
  2.  在 Linux 中，一切皆文件。socket 也是文件的一种，和普通文件的操作没有区别。所以在网络数据传输过程中自然可以使用与 I/O 相关的函数。可以认为，两台计算机之间的通信，实际上是两个 socket 文件的相互读写。
  
  3. `int socket(int af, int type, int protocol);`  其中的 `af` 参数就是地址族， 也就是IP地址类型，常用的有 `AF_INET` 和 `AF_INET6` 。前者表示的是IPv4的地址，后者表示的是IPv6的地址。

```python
import time
from socket import socket, AF_INET, SOCK_STREAM


def echo_handler(address, client_sock):
    print('Got connection from {}'.format(address))
    while True:
        msg = client_sock.recv(8192)
        if not msg:
            break
        client_sock.sendall(msg)
    client_sock.close()


def echo_server(address, backlog=5):
    # tcp protocol
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(backlog)
    while True:
        client_sock, client_addr = sock.accept()
        echo_handler(client_addr, client_sock)


if __name__ == '__main__':
    echo_server(('', 20000))
```




































































