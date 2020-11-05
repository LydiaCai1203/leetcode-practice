# Docker 开发

## 构建尽量小的 Image

+ 从基础镜像开始
+ 使用多阶段构建。意味着最终 Image 不包括构建所引入的所有库和依赖项，而仅包括运行他们所需要的组件和环境。
    + 如果您需要使用不包含多阶段构建的Docker版本，尽可能将多个命令合并为RUN一行并使用Shell的机制将它们组合在一起来实现此目的。
+ 如果有很多个相似的 Image, 则尝试创建一个基础 Image。这样 Docker 只需要加载一次公共层，然后将它们缓存。这样加载更快。

+ 考虑将生产 Image 作为测试 Image 的基础镜像。
+ 在构建 Image 时，始终打上有意义的 tag, 而不要依赖自动的 lastest tag。比如 prod、test、stability，或其它的 tag 用来区分环境。

## 数据持久化

+ 避免使用存储引擎在 container 的 writable layer 的存储数据。这不仅会增加 container 的大小，还会降低 I/O 读写的效率，甚至还不如使用 volumn 或 绑定挂载。
+ 在开发过程中，当您想挂载源目录或二进制文件时，是适合使用绑定挂载的。但是在生产环境中，请改用 volumn。
+ 在开发环境中，可以使用 config 文件。在生产环境中，请使用 services 的 secrets s去存储敏感应用的数据。

## Docker 网络概述

### 网络驱动器

+ `bridge` 默认的网络驱动器，通常应用在 应用程序运行在独立的 container 中而无须和其它 container 联系。
+ `host` 对于独立的 container 来说，移除了容器和宿主机之间的网络隔离，直接使用的是宿主机的网络。
+ `overlay` overlay network 使得多个 Docker  daemon 连接在一起，并使集群服务能够互相通信。比如集群服务和独立容器之间的沟通，比如不同 Docker daemon 上两个独立容器之间的通信。这种策略消除了在这些容器之间进行操作系统级别的路有需要。
+ `macvlan` 允许为 container 分配 mac 地址，使其在网络上显示为物理设备。Docker daemon 通过 mac 地址将流量路由到指定的容器。
+ `none` 对于此容器禁用所有的网络，通常和自定义网络驱动程序一起使用。
+ `network plugins` 在 Docker 上安装和使用第三方网络插件。

### 网络驱动程序摘要

+ 当多个 container 需要在 Docker host 上进行通信时，最好使用 **user-defined bridge network** [user-defined bridge network](https://docs.docker.com/network/network-tutorial-standalone/)
+ 当网络栈不应该和 Docker host 隔离，但是你希望容器和其它方面隔离时，最好使用 **host network** 
+ 当跑在不同的 Docker host 上的不同的 containers 之间需要通信时，或者是许多应用程序运行在集群服务上时，最好使用 **overlay network**
+ 当你要从 VM 设置迁移或需要容器看上去像物理主机，且每一个都有自己的 mac address, 最好用 **macvlan**
+ **第三方网络插件** 使您可以将 Docker 与专用网络堆栈集成。

### 与独立 container 联网

+ **using default bridge** 适合在开发环境中使用。
+ **using user-defined bridge** 适合在生产环境中使用。

#### 使用默认的网桥网络

1. `docker network ls` 列出当前网络。
2. `docker network inspect bridge`检查 bridge 网络 以查看连接了哪些容器。(alpine1: 172.17.0.2/16 | alpine2: 172.17.0.3/16)
3. 使用 `docker attach` 来连接 `alpine1`, `docker attach alpine1` 次时进入到容器内部。
4. `ip addr show` 显示 alpine1 的网络接口 和 它们在容器外部看上去的样子。
5. `ping -c 2 google.com `  `-c 2` 标志将命令限制为两次 ping 尝试。看和外网同不同。
6. 在 alpine1 中ping alpine2 `ping -c 2 172.17.0.2` ， 发现可以 ping 通。
7. 在 alpine1 中尝试用 alpine2 的名称 ping, `ping -c 2 alpine2`, 发现不可以 ping 通。
8. 如果想退出容器则先 ctrl + p 随后按 q。

#### 使用用户自定义网桥

1. `docker network create --driver bridge alpine-net` 创建用户自定义网桥。

2. `docker network ls` 

3. `docker network inspect alpine-net` 会发现网关地址已经不同。(172.18.0.1)

4. ```shell
   $ docker run -dit --name alpine1 --network alpine-net alpine ash
   $ docker run -dit --name alpine2 --network alpine-net alpine ash
   $ docker run -dit --name alpine3 alpine ash
   $ docker run -dit --name alpine4 --network alpine-net alpine ash
   $ docker network connect bridge alpine4
   ```

   也就是说 alpine1、alpine2、alpine4 都连接在 alpine-net 网桥中， 但是 alpine3 和 alpine4 连接在 bridge 网桥中。

5. `docker container ls` 可以看到四个容器都是正常执行

6. `docker network inspect bridge` (alpine4: 172.17.0.1/16 | alpine3: 172.17.0.2/16)

7. `docker network inspect alpine-net`(alpine1: 172.18.0.2/16 | alpine2: 172.18.0.3 | alpine4: 172.18.0.4)

8.  在 user-defined bridge network 中，容器不仅可以通过 IP 地址进行通信，**还可以通过容器名称进行通信**。此功能被称为 **自动服务发现**。

   ```shell
   # 在 alpine1 中 ping alpine3 是不行的，因为它不在 alpine-net 上
   ping -c 2 alpine3
   # 在 alpine1 中 ping alpine3 的 IP 也是不行的
   ping -c 2 172.17.0.2
   # alpine1 可以通过名称和 alpine2 还有 alpine4 还有自己进行通信
   ```

9. 在 user-defined bridge network, 容器依旧可以连接到外网。

#### 使用网桥网络

在网络术语中，网桥网络是一个链路层设备，负责在网段间转发流量。一个网桥可以是运行在主机内核上的硬件设备 或 软件设备。

在 Docker 中，网桥网络是一个软件，允许同一个网桥中的容器相互访问。同时与未连接到该网桥网络的容器隔离。

#### user-defined bridge 和 default bridge 之间的区别

+ user-defined bridges 在container 间访问提供自动的 DNS 解析。
  + default bridge 上的容器只能通过 IP 相互访问，除非你使用 --link, 但是官方不推荐，这是旧用法，可能被剔除
+ User-defined bridge 可以提供更好的隔离，只有连接到该网络的才可以相互访问。
+ container 可以随时从 user-defined bridge network 中分离或连接。但是如果是 default bridge， 需要改变网络的话就要删除容器，重新跑。
+ 每个 user-defined bridge network 都会创建一个可配置网桥
+ default bridge 上的容器共享环境变量。
  + user-defined bridge network 上的容器可以通过挂载包含共享信息的文件或目录， 使用 Docker 的 volumn.
  + 多个 containers 之间可以用 docker-compose 和 compose-file 进行管理和定义共享变量
  + 使用群体服务来代替独立容器。
+ 连接到同一 user-defined bridge network 的容器，所有端口对彼此公开。

#### 基础使用和配置

`docker network create my-net`

`docker network rm my-net`

`docker create --name nginx --network mt-net --publish 8080:80 nginx:latest`

`docker network connect my-net my-nginx`

`docker network disconnect my-net my-nginx`

#### host 网络教程

本教程处理 独立容器直接绑定 docker 宿主机的主机网络，不存在网络隔离。

**目标**

开启一个直接绑定宿主机 80 端口的 nginx container，从网络的角度看，这个和 nginx 直接跑在宿主机上是一样的，不一样的是 存储、命名空间、nginx 进程和主机进程的隔离。host mode network 在容器需要处理大量端口时很有用，因为她不需要网络地址转换，并且也不会为每个端口创建 userland-proxy。

**前提准备**

+ host 网络驱动器只支持 Linux 主机。
+ 需要主机 80 端口可用。让 nginx 监听其它端口。

**过程**

1. `docker rm --rm -d --network host --name nginx nginx` --rm 表示一旦 container 退出或停止就删除容器
2. 访问  [http://localhost:80/](http://localhost/) 以访问 nginx
3. 检视你的 network stack
   + `ip addr show`  检查所有网络接口确保没有新的网络接口生成
   + `sudo netstat -tulnp | grep 80` 确认 nginx 绑定的是 80 端口
4. `docker container stop my_nginx`

#### 覆盖网络（我猜 k8s 用的就是覆盖网络了）

**前提准备**

需要你至少有一个节点的集群，意味着你先要在主机上执行 `docker swarm init` 。

**使用默认的覆盖网络**

本教程需要三台可以互相访问的物理或虚拟的 Docker 主机。假定现在这三台主机在同一网络运行，并且不涉及防火墙。这三台主机分别是 worker-1, worker-2, manager, 其中 manager 即可以充当 manager, 也可以充当 worker, 也就是说既可以运行服务任务，又可以管理集群。三台 docker 主机在一个集群，它们会通过一个名为 ingress 的覆盖网络来连接彼此。

**演练**

+ 创建一个集群

  1. 在 manager 上，初始化一个集群。如果 host 只有一个网络接口，则 --advertise-addr 可有可无. 记录下下面这条命令结束所打印的文本。其中包含用于将 worker-1 和 worker-2 加入集群中的令牌。最好将令牌存储在密码管理器中。

     ```shell
     docker swarm init --advertise-addr=<IP-ADDRESS-OF-MANAGER>
     ```

  2. 让 worker-1 加入集群，如果 host 只有一个网络接口，则 --advertise-addr 可有可无

     ```shell
     docker swarm join --token <TOKEN> \
     --advertise-addr<IP-ADDRESS-OF-WORKER-1> \
     <IP-ADDRESS-OF-MANAGER>:2377
     ```

  3. 让 worker-2 假如集群，如果 host 只有一个网络接口，则 --advertise-addr 可有可无

     ```SHELL
     docker swarm join --token <TOKEN> \
     --advertise-addr<IP-ADDRESS-OF-WORKER-2> \
     <IP-ADDRESS-OF-MANAGER>:2377
     ```

  4. 在 manager 上，罗列出所有的节点

     ```shell
     docker node ls
     ```

     ```shell
     docker node ls --filter role=manager
     docker node ls --filter role=worker
     ```

  5. 现在三个节点每个节点上都有一个覆盖网络称为 ingress 还有一个桥接网络称为 docker_gwbridge. docker_gwbridge 将 ingress 网络连接到 docker 主机的网络接口，以便与流量可以往返于 manager 和 worker.

     ```shell
     # 在 manager 上执行下列语句 
     docker network ls
     ```

  **创建 services**

  1. 在 manager 上，创建一个新的覆盖网络 - nginx-net。无须在其它节点上再创建覆盖网络了，因为当其中一个节点开始运行需要该服务的服务任务时，该网络会自动创建。

     ```shell
     docker network create -d overlay nginx-net
     ```

  2. 在 manager 上，创建具有 5 个副本的 nginx 服务，并连接到 nginx-net 上。这个服务会开放 80 端口给外部，所有的服务任务容器都可以彼此通信，无须开发任何端口。这意味着如果访问 manager、worker-1、worker-2 上的 80 端口，你会连接到 5 个 服务中的一个 80 端口上，即使现在没有任务运行在你浏览的这个节点上。

     ```shell
     docker service create \
     --name my-nginx \
     --publish taiget=80, published=80 \
     --repicas=5 \
     --network nginx-net \
     nginx
     ```

  3. `docker service ls` 

  4. 检视在 manager、worker-1、worker-2 上的 nginx-net 网络，这个输出会很长，需要关注 Containers 和 Peers 部分，Containers 部分会列出所有的从主机连到覆盖网络上的所有服务任务。

  5. `docker service inspect my-nginx` 可以找到服务使用的 端口 和 endpoint 信息

  6. `docker network create -d overlay nginx-net-2`

  7. ```sh
     docker servcie update \
     --network-add nginx-net-2 \
     --network-rm nginx-net \
     my-nginx
     ```

  8. `docker service ls`  去确认服务已被更新 `docker network inspect nginx-net` 确认已经没有容器连接在上面

  9. `docker service rm my-nginx` 和 `docker network rm nginx-net nginx-net-2` 清理服务和网络资源

**使用用户自定义的覆盖网络**

1. 在 manager 所在的主机上创建覆盖网络

   `docker network create -d overlay my-overlay`

2. ```sh
   docker service create \
   --name my-nginx \
   --network my-overlay \
   --replicas 1 \
   --publish published=8080,target=80 \
   nginx:lastest
   ```

3. `docker network inspect my-overlay`

4. `docker service rm my-nginx`

5. `docker network rm my-overlay`