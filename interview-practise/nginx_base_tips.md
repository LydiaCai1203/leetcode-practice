## Nginx 基础复习

[无意中发现的宝藏](http://tengine.taobao.org/book/chapter_02.html) 摘抄

### Nginx 配置模版 && 部分中文注释

```shell
#定义Nginx运行的用户和用户组
user www www;
    
#nginx进程数，建议设置为等于CPU总核心数。
worker_processes 8;
    
#全局错误日志定义类型，[ debug | info | notice | warn | error | crit ]
error_log /var/log/nginx/error.log info;
    
#进程文件
pid /var/run/nginx.pid;
    
#一个nginx进程打开的最多文件描述符数目，理论值应该是最多打开文件数（系统的值ulimit -n）与nginx进程数相除，但是nginx分配请求并不均匀，所以建议与ulimit -n的值保持一致。
worker_rlimit_nofile 65535;
    
#工作模式与连接数上限
events
{
    #参考事件模型，use [ kqueue | rtsig | epoll | /dev/poll | select | poll ]; epoll模型是Linux 2.6以上版本内核中的高性能网络I/O模型，如果跑在FreeBSD上面，就用kqueue模型。
    use epoll;
    #单个进程最大连接数（最大连接数=连接数*进程数）
    worker_connections 65535;
}
    
#设定http服务器
http
{
    include mime.types; #文件扩展名与文件类型映射表
    default_type application/octet-stream; #默认文件类型
    #charset utf-8; #默认编码
    server_names_hash_bucket_size 128; #服务器名字的hash表大小
    client_header_buffer_size 32k; #上传文件大小限制
    large_client_header_buffers 4 64k; #设定请求缓
    client_max_body_size 8m; #设定请求缓
    sendfile on; #开启高效文件传输模式，sendfile指令指定nginx是否调用sendfile函数来输出文件，对于普通应用设为 on，如果用来进行下载等应用磁盘IO重负载应用，可设置为off，以平衡磁盘与网络I/O处理速度，降低系统的负载。注意：如果图片显示不正常把这个改成off。
    autoindex on; #开启目录列表访问，合适下载服务器，默认关闭。
    tcp_nopush on; #防止网络阻塞
    tcp_nodelay on; #防止网络阻塞
    keepalive_timeout 120; #长连接超时时间，单位是秒
    
    #FastCGI相关参数是为了改善网站的性能：减少资源占用，提高访问速度。下面参数看字面意思都能理解。
    fastcgi_connect_timeout 300;
    fastcgi_send_timeout 300;
    fastcgi_read_timeout 300;
    fastcgi_buffer_size 64k;
    fastcgi_buffers 4 64k;
    fastcgi_busy_buffers_size 128k;
    fastcgi_temp_file_write_size 128k;
    
    #gzip模块设置
    gzip on; #开启gzip压缩输出
    gzip_min_length 1k; #最小压缩文件大小
    gzip_buffers 4 16k; #压缩缓冲区
    gzip_http_version 1.0; #压缩版本（默认1.1，前端如果是squid2.5请使用1.0）
    gzip_comp_level 2; #压缩等级
    gzip_types text/plain application/x-javascript text/css application/xml;
    #压缩类型，默认就已经包含text/html，所以下面就不用再写了，写上去也不会有问题，但是会有一个warn。
    gzip_vary on;
    #limit_zone crawler $binary_remote_addr 10m; #开启限制IP连接数的时候需要使用
    
    upstream opstrip.com {
        #upstream的负载均衡，weight是权重，可以根据机器配置定义权重。weigth参数表示权值，权值越高被分配到的几率越大。
        server 10.12.80.121:80 weight=3;
        server 10.12.80.122:80 weight=2;
        server 10.12.80.123:80 weight=3;
    }
    
    #虚拟主机的配置
    server
    {
        #监听端口
        listen 80;
        #域名可以有多个，用空格隔开
        server_name opstrip.com www.opstrip.com;
        index index.html index.htm index.php;
        root /var/www/opstrip.com;
        location ~ .*.(php|php5)?$
        {
            fastcgi_pass 127.0.0.1:9000;
            fastcgi_index index.php;
            include fastcgi.conf;
        }
        #图片缓存时间设置
        location ~ .*.(gif|jpg|jpeg|png|bmp|swf)$
        {
            expires 10d;
        }
        #JS和CSS缓存时间设置
        location ~ .*.(js|css)?$
        {
            expires 1h;
        }
        #日志格式设定
        log_format access '$remote_addr - $remote_user [$time_local] "$request" '
        '$status $body_bytes_sent "$http_referer" '
        '"$http_user_agent" $http_x_forwarded_for';
        #定义本虚拟主机的访问日志
        access_log /var/log/nginx/ha97access.log access;
    
        #对 "/" 启用反向代理
        location / {
            proxy_pass http://127.0.0.1:88;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            #后端的Web服务器可以通过X-Forwarded-For获取用户真实IP
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            #以下是一些反向代理的配置，可选。
            proxy_set_header Host $host;
            client_max_body_size 10m; #允许客户端请求的最大单文件字节数
            client_body_buffer_size 128k; #缓冲区代理缓冲用户端请求的最大字节数，
            proxy_connect_timeout 90; #nginx跟后端服务器连接超时时间(代理连接超时)
            proxy_send_timeout 90; #后端服务器数据回传时间(代理发送超时)
            proxy_read_timeout 90; #连接成功后，后端服务器响应时间(代理接收超时)
            proxy_buffer_size 4k; #设置代理服务器（nginx）保存用户头信息的缓冲区大小
            proxy_buffers 4 32k; #proxy_buffers缓冲区，网页平均在32k以下的设置
            proxy_busy_buffers_size 64k; #高负荷下缓冲大小（proxy_buffers*2）
            proxy_temp_file_write_size 64k;
            #设定缓存文件夹大小，大于这个值，将从upstream服务器传
        }
    
        #设定查看Nginx状态的地址
        location /NginxStatus {
            stub_status on;
            access_log on;
            auth_basic "NginxStatus";
            auth_basic_user_file conf/htpasswd;
            #htpasswd文件的内容可以用apache提供的htpasswd工具来产生。
        }
    
        #本地动静分离反向代理配置
        #所有jsp的页面均交由tomcat或resin处理
        location ~ .(jsp|jspx|do)?$ {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://127.0.0.1:8080;
        }
        #所有静态文件由nginx直接读取不经过tomcat或resin
        location ~ .*.(htm|html|gif|jpg|jpeg|png|bmp|swf|ioc|rar|zip|txt|flv|mid|doc|ppt|pdf|xls|mp3|wma)$
        { expires 15d; }
        location ~ .*.(js|css)?$
        { expires 1h; }
    }
}
```

### 1. Nginx 多进程模型结构

![](/Users/cqj/project/private/leetcode-practice/statics/nginx_struct.jpeg)

```markdown
nginx 启动后，在 uninx 系统中会以 daemon 的方式在后台运行，后台进程包含一个 master 进程 和 多个 worker 进程。我们要操作 nginx，只需要和 master 进程通信即可。

master 进程（主要用来管理 worker 进程）
1. 接收来自外界的信号
2. 向各 worker 进程发送信号
3. 监控 worker 进程的运行状态
4. 当 worker 进程异常退出后自动重新启动新的 worker 进程

worker 进程（处理基本的网络事件）
worker 进程的个数可以设置(一般与 cpu 核数一致)，worker 之间是独立的，对等竞争处理客户端的请求，一个请求只能在一个 worker 中处理。
```

### 2. 为什么说 Nginx 服务不间断？

```markdown
重启 nginx 服务 == 通过 kill 向 master 发送信号, master 收到 HUP 信号以后会经历以下过程（`nginx -s reload`）：
1. 重新加载配置文件
2. 启动新的 worker 进程
3. 通知老的 worker 进程结束
4. 新的 worker 进程开始接收新的 client 请求
5. 老的 worker 进程处理完当前 正在处理但是未处理完成 的 client 请求以后结束
```

### 3. worker 进程竞争模式是什么？

```markdown
在 master 进程里先建立好需要 listen 的 socket(listenfd)，然后再 fork 出多个 worker 进程。所有 worker 进程的 listenfd 会在新链接到来时变得可读，为保证只有一个进程来处理该连接，所有的 worker 进程在注册 listenfd 读事件前，需要抢到 accept_mutex 互斥锁，然后在读事件里调用 accept 接收该连接。接收 accept 连接后，开始读取请求、解析请求、处理请求，产生数据以后返回给客户端，最后才断开连接。
```

### 4. Nginx 如何实现高并发的？

```markdown
虽然 nginx 的每个 worker 里只有一个主线程，但是 nginx 采用了异步非阻塞的方式来处理请求。(这里指的就是 IO 多路复用吧)

首先一个请求的完整过程，建立连接，请求过来，读取请求，发送数据。这些具体到系统底层就是 各种读写事件。我们需要时不时检查一下这些事件的状态，当事件没有准备好发生时，会马上返回 EAGAIN，告诉我们等下再来看看，这期间可以做别的事情。

select、poll、epoll、kqueue 这类系统调用的作用，就是让我们可以同时监控多个事件，调用它们的时候是阻塞的，但是可以设置 timeout，在 timeout 内，如果事件准备好了就返回。拿 epoll 举例，当事件没准备好时，就放在 epoll 里面，事件准备好了，就去读写。当读写再次发生 EAGAIN 时，再将它们放回到 epoll 里面。

线程只有一个，一次只能处理一个请求，但是它可以在不同的请求之间进行切换，所谓高并发，指的是高并发 未处理完 的请求。这里的切换是因为事件没有准备好，主动让出的。所以切换没有任何代价。可以理解为是循环处理多个准备好的事件。

并发数多，只会占用更多的内存而已。在 24G 内存的机器上，并发请求数达到过 200 万。如无必要，不要增加无谓的上下文切换的消耗。这样占用的资源会更加多。

这也是 nginx worker 数会设置成 cpu 的内核数的原因，不带来不必要的 CPU 竞争，不导致不必要的上下文切换。nginx 甚至会在 4bit 字符串比较的时候转换成整数比较，以减少 CPU 的指令数。
```

### 5. Nginx 基础概念 - connection

```markdown
在 nginx 中，connection 就是对 tcp 连接的封装，其中包括了连接的 socket、读事件、写事件。利用 nginx 封装的 connection，我们可以很方便地使用 nginx 来处理与连接相关的事情，比如 建立连接、发送 和 接收数据。nginx 中的 http 请求就是建立在 connection 之上的。利用 nginx 提供的 connection, 我们可以和任何后端服务打交道。
```

### 6. 七层负载均衡 和 四层负载均衡(load balancer)  - 四种转发模式

[美团点评四层负载均衡](https://tech.meituan.com/2017/01/05/mgw.html)  - 有点怪

[LSV 文档 - 建议直接看这个](http://www.linuxvirtualserver.org/why.html)

[ARP 和 LAN 的关系](https://www.net.t-labs.tu-berlin.de/teaching/computer_networking/05.04.htm)

```markdown
早期的方法是 DNS 做负载：
通过给客户端解析不同的 IP 地址，让客户端的流量直接到达各个服务器。缺点：1. 延时性，在作出调度策略改变以后，由于 DNS 各级节点的缓存并不会及时的在客户端生效，而且 DNS 负载的调度策略比较简单，无法满足业务需求。

采用 负载均衡器 做负载：
客户端的流量首先会到达负载均衡器，由负载均衡服务器通过一定的调度算法将流量分发到不同的应用服务器上，同时 负载均衡服务器 也会对 应用服务器 做周期性的健康检查，当发现故障节点时便动态的将节点从应用服务器集群中剔除，以此来保证高可用。（LSV + Keepalaived）
```

#### 四层负载均衡：

```markdown
工作在 OSI模型 的 传输层(第四层)，主要工作是转发，它在接收到客户端的流量以后通过修改数据包的地址信息将流量转发到应用服务器。
```

#### 七层负载均衡：

```markdown
工作在 OSI模型 的 应用层(第七层)，需要解析应用层的流量，七层负载均衡接到客户端的流量以后，还需要一个完整的 TCP/IP 协议栈。七层负载均衡会与客户端建立一条完整的连接并将应用层的请求流量解析出来，再按照调度算法选择一个应用服务器，并与应用服务器建立另外一条连接，然后将请求发送过去，七层负载均衡的主要工作就是代理。
```

#### 四种转发模式：

```markdown
DR(Director Routing) 模式：

模式：client -> Director（Virtual IP, VIP）-> Real Server -> client

DR 模式也叫做三角传输，通过修改数据包的目的 MAC 地址来让流量经过二层转发到达应用服务器，然后应用服务器直接回复给用户。

优点：应用直接将应答发给客户端，性能好。
缺点：要求负载均衡服务器必须在一个二层可达的环境内。

PS：IEEE 802 标准所描述局域网(LAN)参考模型只对应 OSI 参考模型的数据链路层与物理层，VLAN 在 LAN 之上为避免广播域冲突，对广播域又进行划分。不同 VLAN 之间不能通信，需要三层设备(路由器)才可以。因此要求 Director 和 Real Server 必须通过 LAN 的单个不间断直接彼此连接。
```

```markdown
NAT(Network Address Translation) 模式：

模式：client -> Director（Virtual IP, VIP）-> Real Server -> Director -> client

NAT 模式通过修改数据包的目的 IP 地址，让流量到达应用服务器。
1. client 发送数据包到 Director
Source: 202.100.1.2:3456 | Dest: 202.103.106.5:80
2. Director 选择 Real Server，重写目的 IP 并转发
Source: 202.103.106.5:80 | Dest: 172.16.0.3:8000
3. Real Server 返回响应数据包给 Director
Source: 172.16.0.3:8000 | Dest: 202.103.106.5:80
4. Director 修改响应数据包的目的 IP 为 client_ip 并转发
Source: 202.103.106.5:80 | Dest: 202.100.1.2:3456

优点：Real Server 可以运行任何支持 TCP/IP 协议的操作系统，Real Server 可以使用 私有网络的IP，并且 Director 仅仅需要 IP 即可。
缺点：Director 充当网关形式，数据包来回都需要经过 NAT 转换，当 Real Server 达到 20 个甚至更多时，Director（LVS）可能将成为系统瓶颈。
```

```markdown
IP TUNNEL 模式：
本质是将 IP 数据报封装在 IP 数据报中的技术，它允许将发往一个 IP 地址的数据报包装并重定向到另一个 IP 地址。

模式：
client -> Director（Virtual IP, VIP）-> (IP Tunnel) -> Real Server -> client

当用户访问 VIP 时，数据包到达 Director 时，Director 会检查数据包的目的地址和端口。如果它们与虚拟服务相配，则根据连接调度算法从集群中选择一个 Real Server，并将该连接添加到记录连接的 hash table 中。Director 会将 IP 数据包封装在 IP 数据包中，并将其转发到选定的服务器。当 Real Server 收到封装后的 IP 数据包，它会对数据包进行解析，并处理请求，最后根据自己的路由表然后将结果直接返回给用户。

缺点：Real Server 必须支持 IP 封装协议。它们的隧道设备都已配置完毕，以便系统可以正确地解封装收到的数据包。
优点：和 DR 模式的优点一样，性能较好。
```

```markdown
FULLNAT(SNAT + DNAT) 模式：
SNAT 源地址转换，内部地址要访问公网上的服务时，内部服务发起连接，内部 ip 转换为公有 ip。网关把这个地址转换称为 SNAT。相反地，外部服务需要访问内部服务时，是由网关接收到的，将目的 ip 转换为内部 ip。这个称为 DNAT。

模式：
client -> LVS -> SNAT -> Real Server -> LVS -> DNAT -> client

首先 Director 上存在一个 localip 池，当 client 流量达到 Director 以后，Director 会根据调度策略在 Real Server 之间选择一个，然后将数据包的目的 IP 改为 Real Server 的 IP。同时从 localip 池中选择一个 ip 作为数据包的源 ip。当 Real Server 发出响应包时，注意此时的 目的 ip 已经是 localip 了，到达 Director 以后，

优点：可以让应答流量经过正常的三层路由回到 Director 上，这样 Director 不再以网关的形式存在于网络中，对网络环境的要求较低。也就是具有较强的网络适应性。
缺点：FULLNAT 比 NAT 多做了 SNAT 和 DNAT，性能要逊色于 NAT 模式。
```


