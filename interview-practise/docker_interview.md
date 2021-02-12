## Docker

[Docker 从入门到实践](https://yeasy.gitbook.io/docker_practice/introduction/what)

### 1. Docker 是什么？

```markdown
Docker 最初是 dotCloud 公司的一个内部项目，该项目由 Golang 开发实现，基于 Linux 内核的 CGroup、Namespace、UnionFs 等技术，对进程进行封装隔离(操作系统层面的虚拟化技术)。由于隔离的进程独立于宿主机和其它进程，因此也成为容器。最初的实现基于 LXC(Linux Container)，后来使用自行开发的 libcontainer，后来使用了 runC 和 containerd。runc 是一个 Linux 命令行工具，用来创建和运行容器。containerd 是一个守护程序，管理程序的生命周期，提供了在一个节点上执行容器和管理镜像的最小功能集。
```

### 2. Docker 架构

![](/Users/cqj/project/private/leetcode-practice/statics/docker_architecture.jpeg)

### 3. Docker 和 VM 的区别？

```markdown
VM：
传统的虚拟机是虚拟出一套硬件之后，在其上运行一个完整的操作系统，然后在该系统上运行所需应用进程。

Docker:
容器内的应用进程直接运行于宿主机的内核，容器内没有自己的内核，而且也没有进行硬件虚拟，因此容器比传统的虚拟机更为轻便。
```

![](/Users/cqj/project/private/leetcode-practice/statics/vm_docker.jpeg)

### 4. Docker 的优点是什么？

```markdown
1. 一致的运行环境，排除环境不一致导致的 Bug，也使得应用的迁移更加轻松。
2. 持续交付和部署，一次创建和配置，就可以在任意地方正常运行。
3. 更加轻松的维护和扩展。由于分层存储以及镜像技术，使得应用重复部分的复用更为容易，也使得应用的维护更新更加简单。
```

### 5. 什么是镜像、容器、仓库？

```markdown
镜像：
镜像是一个特殊的文件系统，除了提供容器运行时所需要的程序、库、资源、配置等文件外，还包含了一些为运行时准备的一些配置参数(如匿名卷、环境变量、用户等)。镜像不会包含任何动态数据，其内容在构建之后也不会被改变。镜像并不是一个文件，而是由多层文件系统联合而成的。

-----------------------
容器：
镜像是静态的定义，容器是镜像运行时的实体，容器可以被创建、启动、停止、删除、暂停等。容器的实质是进程，容器进程运行于属于自己的独立的 Namespace。所以容器可以拥有自己的 root 文件系统、网络配置、进程空间、用户ID空间。所以容器内的进程是运行在一个隔离的环境里。

每一个容器在运行时，以镜像为基础层，在上创建一个当前容器的存储层，我们成这个为容器运行时读写而准备的存储层成为，容器存储层。容器存储层的生命周期和容器一样。

根据《Docker 的最佳实践》，容器不应该向其存储层内写入任何的数据，容器存储层要保持无状态话，所有文件写入操作都应该使用数据卷(volume)、绑定宿主目录,在这些位置的读写会跳过容器存储层，直接对 宿主/网络存储 发生读写，性能和稳定性都将会更高。

------------------------
仓库：
镜像仓库是一个集中存储、分发镜像的服务。通常一个仓库会包含一个软件不同版本的镜像，tag 用于对应软件的版本。对应格式为 <仓库名>:<标签>。如果不给出标签，则默认 tag=latest。仓库名经常以 两段式路径 的形式出现，如 caiqj/nginx-procy, 前者是用户名，后者是软件名。
```

### 6. 公有仓库 && 私有仓库

```markdown
公有仓库：
一般允许所有用户免费上传、下载公开的镜像，允许用户管理自己的镜像。最常用的有 Docker Hub,里面有大量高质量的官方镜像。

私有仓库：
用户可以自己本地搭建私有的镜像仓库，Docker Hub 提供私有仓库服务。

除了官方的 Docker Registry 以外，还有第三方软件实现了 Docker Registry API, 甚至还提供了用户界面以及一些高级功能，比如 Harbor、Sonatype Nexus。
```

### 4. 什么是 Docker Engine？

```markdown
Docker 守护程序/Docker 引擎（dockerd）侦听 Docker API 请求并管理 Docker 对象，例如图像、容器、网络、卷。守护程序可以和其它的守护程序通信以管理 Docker 服务。
```

### 6. Docker 实现隔离机制的底层技术是什么？

[详细笔记](https://github.com/LydiaCai1203/leetcode-practice/blob/master/docker_virtual_isolate.md)

```markdown
Docker 具有以下隔离机制：
1. 容器进程是隔离的。在容器内部是无法看到宿主机的进程。
2. 容器文件系统是隔离的。在容器内修改文件并不能影响宿主机上对应目录的文件。
3. 容器的网络是隔离的，每个容器都拥有独立的 IP。

以上隔离机制都不是 Docker 的新技术，而是通过 Linux Kernel 现有的技术实现的：
1. 资源控制(CGroups)
2. 访问控制(Namespace)
3. 文件系统隔离(UnionFS)
```

### 7. 什么是 memory-swap 标志?

**什么是内存溢出？**

```markdown
不允许正在运行的容器占用过多的主机内存，在 Linux 主机上，如果内核检测到没有足够的内存来执行重要的系统功能，则会抛出 `Out Of Memory Exception`，并开始终止进程以释放内存，如果杀死错误的进程，严重会导致整个系统的瘫痪。
```

**限制容器可以访问的内存大小**

```markdown
docker 可以强制限制容器使用的内存大小。在启动的容器的时候配置以下参数达到不同的效果：

1. -m --memory=: 设置容器可以使用的最大内存量，最小值是 4m

2. --memory-swap: 该标志仅在设置 --memory 的时候才有意义，就是当内存不足时，把一部分硬盘空间虚拟成内存来使用，从而解决内存不足的问题。--memory-swap 表示的是可以使用的 内存 和 交换 的 总量。所以假如 --memory-swap='1g'， --memory='300m', 则表示可用内存为 300m, 可用的交换内存为 700m。
    a. --memory-swap == --memory：不能使用交换内存
    b. --memory-swap == 0: 忽略该设置
    c. --memory-swap == -1: 允许容器无限交换。最高不超过主机系统上可用的数量。
```

### 8. Dockerfile 中 ADD 和 COPY 的区别？

**docker build 上下文**

```markdown
表示指定 /home/nick/hc 为 build 的上下文，-f 指定 Dockerfile 的位置
`docker build -t testx /home/nick/hc -f ../Dockerfile`

Docker 运行时分为 Docker Engine 和 Docker Client。
前者提供 REST API, 后者通过 Docker 命令与 engine 进行交互。所以镜像实际并不是在本地构建的，而是在服务器，那么在构建过程中，就需要指定构建镜像上下文的路径。如果有不想被传输的文件，就可以使用 .dockerignore 进行剔除。

docker build 还具有以下功能：
1. 给定 repo-url，直接从 repo 中拉取。
2. 给定 tar-url，docker engine 会下载这个包，自动解压缩，以其作为上下文开始构建。
3. 从标准输入中读取 dockerfile 进行构建
`docker build - < Dockerfile`
`cat Dockerfile | docker build -`
4. 从标准输入中读取上下文压缩包进行构建
`docker build - < context.tar.gz`
```

**COPY 和 ADD 不能拷贝 context 之外的本地文件**

```markdown
所以当用户指定了构建镜像上下文的路径，`docker build` 会将该路径下的所有内容打包，上传给 docker engine，docker engine 收到这个上下文包后，展开会获得构建镜像所需要的一切文件。

`COPY ./package.json /app/` 意思并不是复制当前目录下的 package.json 文件，而是复制 上下文目录下的 package.json。所以如果要复制超越上下文目录的文件，就会报错或者不生效哦。
```

**与 WORKDIR 协同工作**

```markdown
WORKDIR 为后续的 RUN、COPY、ADD 等命令配置工作目录。下面的例子意思是 checkredis.py 会复制到容器的 /app 目录下。

`WORKDIR /app`
`COPY checkredis.py .`

为什么不能用 `RUN cd /app` 来实现呢？
RUN cd /app
RUN echo "hello" > world.txt

第一层 RUN 的执行仅仅是当前进程的工作目录的变更，一个内存上的变化而已，不会造成任何结果文件的变更。
第二层 RUN 的执行时候是一个全新的容器，和第一层的构建完全没关系，达不到变更目录的过程。
```

**需要注意**

```markdown
WORKDIR /a
WORKDIR b
WORKDIR a
RUN pwd              # 输出结果：/a/b/c
```

**COPY**

```markdown
COPY 指令会保留源文件的各种元数据，比如读、写、执行的权限，文件的变更时间等等。
执行的时候还可以通过 --chown=<user>:<group> 来改变文件所属的用户以及组。一般用法就是复制 源文件/源目录下的文件 到 目的文件/目的目录下

格式：
`COPY <src> <dest>`

用途一：
`COPY nickdir ./nickdir`

用途二：
通过 --from=0 把前一阶段构建的产物拷贝到当前 image 中，即 multi-stage 所阶段构建。
`COPY --from=0 /go/src/github.com/sparkdevo/href-counter/app .`
```

**ADD**

```markdown
性质和 COPY 基本一致，在此基础上新增了一些功能。ADD 指令会令镜像构建缓存失效，从而可能使得镜像构建变得缓慢。因此不建议使用 ADD。

格式：
`ADD <src> <dest>`

用途一：
解压压缩文件并且把它们添加到镜像中，底层相当于添加了一层 RUN, 做解压缩的动作。因此使用 ADD 会让镜像更加的臃肿。所以如果不需要解压缩的话，用 COPY 就可以。
`ADD nickdir.tar.gz .`

用途二：
从 URL 拷贝文件到镜像中，下载后的文件权限自动设置为 600。如果这不是想要的权限，需要增加一层额外的 RUN 进行权限调整。
`ADD http://example.com/big.tar.xz /usr/src/things/`
```

### 10. FROM

```markdown
为后续指令设置基本镜像，它都是第一条指令。
`FROM <image>:<tag>`

如果需要一个完全空白的镜像, 使用 scratch 特殊镜像，有一些静态编译的程序并不需要操作系统提供运行时支持，使用 go 语言开发的应用很多会用这种方式制作镜像,这就是为什么很多人认为 Go 特别适合容器微服务架构的语言原因之一。
`FROM scratch`
```

### 11. RUN && CMD

**RUN**

```markdown
构建镜像时，用来执行命令行命令的
每一个 RUN 都是启动一个容器、执行命令、提交存储层文件变更。
`RUN <command>`

shell 格式
`RUN apk update`

exec 格式
`RUN ["executable", "param1", "param2"]`

*UnionFS 是有最大层数限制的，曾经最大不超过 42 层，现在最大不超过 127 层。

错误写法
`RUN set -x; buildDeps='gcc libc6-dev make wget'`
`RUN apt-get update`
`RUN apt-get install -y vim`
`RUN apt-get purge -y --auto-remove $buildDeps`

正确写法
`RUN set -x; buildDeps='gcc libc6-dev make wget' \`
`&& apt-get update \`
`&& apt-get install -y vim \`
`&& apt-get purge -y --auto-remove $buildDeps`

注意最后一句删除了为了编译构建所需要的软件，清理了所有下载、展开的文件，还清理了 apt 缓存文件，确保每一层都只添加真正需要添加的东西，任何无关的东西都应该被清理掉。
```

**CMD**

```markdown
CMD 就是用于指定默认的容器主进程的启动命令的。只能写一次，写多个只有最后一个生效。
`CMD <command>`

shell 格式
这种格式在解析的时候，会被包装成 sh -c 的形式执行
`CMD command param1 param2`

exec 格式（推荐使用）
这种格式在解析时会被解析为 json 数组，因此一定要用 " 而不是 '。
`CMD ["executable","param1","param2"]`

如果我们直接 `docker run -it ubuntu` 等价于 `docker run -it ubuntu /bin/bash`。一进入镜像就直接进入 bash。如果写成 `docker run -it ubuntu cat /etc/os-release` 就是自动输出系统版本信息。

需要注意，`docker run -it ubuntu /bin/bash` 会代替掉 dockerfile 里面的 CMD 值。
```

**CMD service nginx start**

```markdown
首先, `service nginx start` 是希望以后台守护进程的形式启动 nginx。

容器是为了主进程而存在的，主进程如果退出，容器就是去存在的意义，其它的辅助进程并不是它所关心的东西。`CMD service nginx start` 会被解释成 `CMD["sh", "-c", "service", "nginx", "start"]`，实际上主进程是 sh, 那么当 `service nginx start` 结束以后，sh 作为主进程也就结束了。

正确做法是，`CMD ["nginx", "-g", "daemon off;"]` 以前台形式执行 nginx 可执行文件。
```

### 12. ENTRYPOINT

```markdown
使用：
ENTRYPOINT [ "curl", "-s", "http://myip.ipip.net" ]

只能写一次，写多个只有最后一个生效。
存在 ENTRYPOINT 之后，CMD 的内容会作为参数传给 ENTRYPOINT, 可以达到叠加使用的效果。
```

### 13. ENV 和 ARG 的区别是什么？

```markdown
ENV 使用：
# 设置环境变量
ENV NODE_VERSION 7.2.0
ENV NODE_VERSION=7.2.0 DEBUG=on NAME="Happy Feet"  # 如果有空格就用双引号括起来

ARG 使用：
# 构建参数，在容器运行时是不会存在这些环境变量的，docker history 还是可以看到
ARG DOCKER_USERNAME=library
# 如果在 --build-arg 总定义，必须在 Dockerfile 中使用到，会显示警告信息，继续构建
# 如果 Dockerfile 定义了相同的参数，则在 --build-arg 中的参数值会将其覆盖
docker build --build-arg <参数名>=<值>

注意：
如果 ARG 在 FROM 之前使用，则 ARG 只能在 FROM 中使用。如果想要在 FROM 之后使用，必须再次指定 ARG。
```

### 14. EXPOSE 声明端口

```markdown
格式：
EXPOSE <端口1> [<端口2>...]

EXPOSE 是声明运行时容器提供服务的端口，这只是一个声明，在运行时并不会因为这个声明应用就会开启这个端口的服务。

这样写有两个好处：
1.帮助镜像使用者理解这个镜像服务的守护端口 
2.在运行时使用随机端口映射时，`docker run -p <宿主端口>:<容器端口>`，则会自动随机映射 EXPOSE 的端口。 
```

### 13. 匿名卷

```markdown
格式：
VOLUME ["<路径1>", "<路径2>"...]
VOLUME <路径>

使用：
`VOLUME /data`

容器运行时应该尽量保持容器存储层不发生写操作，为了防止运行时用户忘记将动态文件所保存目录挂载为卷，在 Dockerfile 中，可以事先指定某些目录挂载为匿名卷。这样在运行时，用户不指定挂载，应用也可以正常进行。
```

### 14. USER 切换用户

```markdown
改变之后层执行 RUN、CMD、ENTRYPOINT 之类的命令的用户身份。

用法：
# 第一条用的是 ROOT 用户的身份
RUN groupadd -r redis && useradd -r -g redis redis
USER redis
# 第二条用的是 redis 用户的身份
RUN [ "redis-server" ]
```

### 15. HEALTHCHEK 健康检查

```markdown
格式：
# 设置检查容器健康状况的命令
HEALTHCHECK [选项] CMD <命令>
# 如果基础镜像有健康检查指令，这行可以屏蔽掉其健康检查指令
HEALTHCHECK NONE

只能写一次，写多个只有最后一个生效。
在 Docker1.12 之前，Docker Engine 根据容器内主进程是否退出来判断容器是否状态异常。但是如果程序进入死锁状态，或是死循环状态，应用进程不会退出，容器也无法提供服务。
在 Docker1.12 之后，HEALTHCHECK 指令提供，判断容器主进程服务是否正常。

当指定了 HEALTHCHECK 之后，容器初始状态是 starting, 健检成功以后是 healthy，连续多次失败以后则是 unhealthy。

使用：
FROM nginx
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*
HEALTHCHECK --interval=5s \     # 健检之间的间隔实践
    --timeout=3s \              # 健检最长时间，超过则视为失败
    CMD curl -fs http://localhost/ || exit 1
```

### 16. LABEL 为镜像添加元数据

```markdown
格式：
LABEL <key>=<value> <key>=<value> <key>=<value> ...

使用：
LABEL org.opencontainers.image.authors="yeasy"
```

### 16. Dockerfile 多阶段构建

```markdown
通常做法：
将所有的构建过程包含在一个 Dockerfile 中，包括项目及其依赖库的编译、测试、打包等流程。
可能带来的问题：
1. 镜像层次多，体积较大，部署时间变长
2. 源代码存在泄露风险

多阶段构建：
1. 使用 as 来为某一阶段命名
   `FROM golang:1.9-alpine as builder`
   当只想构建 builder 阶段镜像时，增加 --target=builder 即可
   `FROM golang:1.9-alpine as builder`
2. 构建时从其它镜像复制文件
   `COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf`
   或者是从上一个阶段的镜像中复制文件
   `COPY --from=0 /go/src/github.com/go/helloworld/app .`

3. 完整的例子(这样会比所有的层都写在一个阶段要小很多很多)
   FROM golang:1.9-alpine as builder
   RUN apk --no-cache add git
   WORKDIR /go/src/github.com/go/helloworld/
   RUN go get -d -v github.com/go-sql-driver/mysql
   COPY app.go .
   RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o app .

   FROM alpine:latest as prod
   RUN apk --no-cache add ca-certificates
   WORKDIR /root/
   COPY --from=0 /go/src/github.com/go/helloworld/app .
   CMD ["./app"]
   
4. 多阶段构建就相当于是将原来的一个 Dockerfile 拆分成两个，然后将一个 Dockerfile 中的项目及其依赖库编译测试打包好后，再将其拷贝到运行环境中。
```

### 11. Docker 的命名空间是什么？

```markdown
Docker 命名空间会为每个容器创建一组 namespace, 这些 namespace 为容器提供了一层隔离，每个容器都在不同的 namespace 中运行。
```

### 12. Docker 默认哪些网络可用？

[Docker 网络概述](https://github.com/LydiaCai1203/leetcode-practice/blob/master/docker/docker_develop.md)

```markdown
看一下 bridge、host、overlay、none、macvlan 都是什么意思
```

### 13. 容器是怎么做持久化的？

**持久化到目录**

```shell
格式：
docker run -itd --name [容器名字] -v [宿主机目录]:[容器目录] [镜像名称] [命令(可选)]

使用：
# 在宿主机 /Users/ethanyan/dockerdata 下添加文件，会发现容器内的 /data 目录下也出现相应的文件
docker run -itd --name nginx -v /Users/ethanyan/dockerdata:/data nginx
```

**持久化到文件**

```markdown
格式：
docker run -itd --name [容器名字] -v [宿主机文件]:[容器文件] [镜像名称] [命令(可选)]

使用：
# 宿主机要映射的文件与容器内的文件，名称可以不同，类型必须相同
# 在容器内修改文件，会发现宿主机的文件也被修改了
docker run -itd --name nginx_test -v /Users/li/dockerdata/NG/testdata.txt:/data/testdata.txt nginx
```

**持久化到数据卷(最好的方式)**

```markdown
1. 数据卷存储在宿主机文件系统中的某个区域 docker volume ls && docker inspect volume_id
2. Docker 管理数据卷，非 Docker 进程不应该随意修改
3. 没有显示创建，Docker 会创建一个随机命名的 volume，当容器停止时，卷也仍然存在，除非显式删除
4. 多个容器可以通过 read-write 或 read-only 的方式使用同一个卷
5. 如果非空卷挂载到容器内的空目录，则卷内的内容会拷贝到空目录中；如果非空卷挂载到容器内的非空目录，则卷内的内容会被隐藏
```

```shell
# 创建卷
docker volume create volume1

# 挂载卷 -v 方式
docker run -d --name redis_test -v volume1:/data_volume redis

# 挂载卷 --mount 方式
# -v 可以做的 --mount 都可以做，--mount 更灵活，支持更多复杂操作，且不需要严格按照参数顺序，通过 kv 方式配置，可读性也越高
docker run -d --name redis_test --mount type=volume,source=volume1,target=/data_volume redis

# 清理所有无用的数据卷
docker volume prune
```

**持久化到容器**

如果不想这些数据直接暴露在宿主机上，可以使用数据卷容器的方式。**将数据卷容器挂载到其它容器**，就可以多个容器之间共享数据了，还可以实现持久化的保存数据。步骤如下：

1. 创建数据卷容器

```shell
# 格式
docker create -v [容器数据卷目录] --name [容器名字] [镜像名称] [命令(可选)]
# 使用
docker create -v /data/ --name data nginx
```

2. 将数据卷容器挂载到其它容器，使用数据卷是在容器间共享数据。

```shell
# 格式
docker run --volumes-from [数据卷容器 id/name] -itd --name [容器名字] [镜像名称] [命令(可选)]
# 使用
docker run  --volumes-from db847d3fc055 -itd --name nginx_test1 nginx /bin/bash
docker run  --volumes-from db847d3fc055 -itd --name nginx_test2 nginx /bin/bash
```

3. 测试

```markdown
在 nginx-test1 - /data - 创建 test.txt 文件，在 nginx-test2 - /data 下也能看见
```

4. 备份

```shell
# 该命令是加载数据卷容器并将容器内的 /data 目录打包，然后把压缩包保存到 映射到容器内 的新数据卷，本地目录为 /Users/ethanyan/dockerdata/ 。执行完后，会在本地该目录出现压缩包 backup.tar。
docker run -it --volumes-from data -v /Users/ethanyan/dockerdata/:/backup nginx tar cvf /backup/backup.tar /data
```

5. 恢复

```shell
# 创建一个新的数据卷容器 data_new
docker create -v /data/ --name data_new nginx

# 恢复之前的备份文件
# 格式
docker run --volumes-from [新创建的数据卷容器id或者name] -v [宿主机存放备份文件的目录]:[容器内存放备份文件目录] [镜像] tar xvf [备份文件]
# 使用
docker run --volumes-from data_new -v /Users/ethanyan/dockerdata/:/backup nginx tar xvf /backup/backup.tar
data/
data/file.txt
```

### 15. 查看镜像所占存储空间大小？

```markdown
$ docker images ls

REPOSITORY    TAG       IMAGE ID       CREATED         SIZE
redis         latest    235592615444   8 months ago    104MB

Docker Hub 中的镜像是压缩后的大小，docker image ls 显示的大小是下载到本地，解压缩以后的大小。但是由于镜像是分层存储的，不同镜像使用到相同的层，是只存储一层的。如果要看 image 的总存储，使用 docker system df 即可。
```

### 16. 虚悬镜像

```markdown
既没有仓库名，也没有标签名，即都是 none 的镜像，称为虚悬镜像。比如 build 一个新镜像，但是新镜像和旧镜像的名字一样，这样旧镜像就会变成虚悬镜像。可以使用以下命令删除。

# 显示虚悬镜像 -f 就是 --filter
docker image ls -f dangling=true
# 清理虚悬镜像
docker image prune
```

### 17. 中间层镜像

```markdown
为了加速镜像构建、重复利用资源，Docker 还会利用中间镜像。在使用一段时间后，可能会看到一些依赖的中间层镜像。`docker image ls` 只会列出顶层镜像，`docker image ls -a` 就可以显示包括中间镜像在内的所有镜像。`docker image ls ubuntu` 可以帮助只列出和 ubuntu 相关的镜像。

这些中间层镜像的 仓库名 和 标签 也都是 none，和虚悬镜像不同，它们是其它镜像依赖的镜像，所以不应该也没必要被删除。如果依赖他们的镜像被删除了，中间镜像也会被一起删除的。
```

### 18. 如何批量删除镜像

```markdown
# 可以批量删除所有名字为 redis 的镜像
$ docker image rm ${docker image ls -q redis}

# 可以批量删除所有在 mongodb:3.2 之前的镜像
$ docker image rm ${docker image ls -q -f before=mongo:3.2}
```

### 14. docker commit

```markdown
docker 可以将容器的 读写层 保存下来成为一个新的镜像，运行这个新镜像的话，就会拥有容器最后的文件变化。可以通过 `docker diff <registry>:<tag>` 来查看具体的改动。或者使用 `docker history <registry>:<tag>` 查看镜像内的提交记录。

格式：
docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]

使用：
docker commit \
    --author "Tao Wang <twang2218@gmail.com>" \       # 指定修改的作者
    --message "修改了默认网页" \                        # 记录本次修改的内容
    webserver \
    nginx:v2

sha256:07e33465974800ce65751acc279adc6ed2dc5ed4e0838f8b86f0c87aa1795214
```

**docker commit 并不建议使用**

```markdown
1. 所有对镜像的操作都是黑箱操作，生成的镜像也是 黑箱镜像。除了镜像制作人，谁也不知道执行过什么命令，对维护来说非常不便。
2. 如果修改的层仅仅是在当前层标记、添加、改动，而不会改动到上一层。每次修改都制作一次镜像，到最后镜像就会十分臃肿，即便这一次删除了上一次的修改，在镜像里的东西也不会消失。
```

### 20. Docker 镜像是怎么实现增量的修改和维护的？

```markdown
通常 UnionFS 有两个用途：
1. 在不借助 LVM、RAID 的情况下，将多个 disk 挂载到同一个目录下。
2. 将一个只读的分支和一个可写的分支联合在一起。

LiveCD 正是基于此方法允许在镜像不变的基础上，允许用户进行一些写操作。Docker 在 OverlayFS 上构建容器也是利用了类似的原理。
```

### 21. 启动容器时 -it 参数代表什么含义

```markdown
-i：让容器的标准输入始终打开
-t: 让 Docker 分配一个伪终端并绑定到容器的标准输入上
```

### 22. docker run 命令之后做了什么？

```markdown
1. docker engine 会检查本地是否存在指定镜像，不存在就去仓库下载
2. 利用镜像创建一个容器
3. 分配一个文件系统，在只读镜像外层挂载一个可读写层
4. 从宿主机配置的网桥接口中桥接一个虚拟接口到容器中去
5. 从地址池配置一个 ip 地址给容器
6. 执行用户指定的应用程序
7. 执行完毕后容器被终止
```
