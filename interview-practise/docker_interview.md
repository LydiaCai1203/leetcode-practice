## Docker

### 1. Docker 是什么？

```markdown
Docker 是一个开源的、轻量级的容器化技术。它在 云 和 应用程序 包装领域广泛流行。它使您可以自动在轻量和便携式容器中部署应用程序。
```

### 2. 什么是容器？什么是镜像？

```markdown
镜像 是一种静态的结构，可以看成是面向对象里的类。包含软件运行所需的所有内容：代码、运行时环境、系统工具、系统库和设置。它是一种分层结构，每一层都是 read-only 的。构建镜像时，前一层是后一层的基础，这种结构适合镜像的复用和定制。
每个 Docker 镜像都存储在 Docker 仓库中。
```

```markdown
容器可以理解为是镜像的一个实例。构建容器时，通过在镜像的基础上添加一个 wirtable layer, 用于保存容器在运行过程中的修改。
```

### 3. Docker 的优点是什么？

```markdown
1. 部署方便
常见的流程可能是，打包好的镜像上传到远程镜像仓库，再加一个控制部署流程的执行脚本。
2. 部署安全
可以将开发环境和测试环境以及生产环境保持版本和依赖上的统一，从而保证代码在一个高度统一的环境上执行。这样可以把很多因为人工配置环境产生的失误降到最低。
3. 隔离性好
可能在同一台机器上需要部署多个服务，服务之间可能需要使用同一个依赖，而服务需要的依赖之间可能会有一些冲突。容器就是一个隔离的环境。
4. 快速回滚
容器的回滚机制支持基于上个版本的应用重新部署，这个过程非常快速和简单。
5. 成本低
容器技术小巧轻便，只需要给一个容器内部构建应用需要的依赖即可。
6. 管理成本更低
Docker Swarm，Kubernetes，Mesos 等容器管理和编排技术，使得容器的管理成本更低。

```

### 4. 什么是 Docker Engine？

```markdown
Docker 守护程序/Docker 引擎（dockerd）侦听 Docker API 请求并管理 Docker 对象，例如图像、容器、网络、卷。守护程序可以和其它的守护程序通信以管理 Docker 服务。
```

### 5. 什么是镜像仓库？

```markdown
仓库有两种类型：
1. 公共仓库（Docker 公共仓库称为 Docker Hub），您可以存储数百万个镜像。
2. 私人仓库（Azure 容器仓库、本地专用仓库等）
	私人镜像仓库保密，镜像不可被公开分享。
	在镜像和部署环境之间，可以保持网络延迟最低。

涉及命令：
docker pull
docker push
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
使用 docker build 命令通过 Dockerfile 创建镜像时，会产生一个 build context。这个 context 就是 docker build 中指定的 PATH 或 URL 中的文件集合。

# 表示指定 /home/nick/hc 为 build 的上下文
docker build -t testx /home/nick/hc
```

**COPY 和 ADD 不能拷贝 context 之外的本地文件**

```markdown
在执行 build 命令时，docker 客户端会把 context 中的所有文件发送给 docker daemon。如果 docker 客户端 和 docker daemon 不在同一台机器上，build 命令只能从 context 中获取文件了。否则会报错。
```

**与 WORKDIR 协同工作**

```markdown
WORKDIR 为后续的 RUN、COPY、ADD 等命令配置工作目录.

WORKDIR /app
COPY checkredis.py .        # 意思是 checkredis.py 会在容器的 /app 目录下
```

**COPY**

```markdown
格式：
COPY <src> <dest>

用途一：
COPY nickdir ./nickdir

用途二：
# 通过 --from=0 把前一阶段构建的产物拷贝到当前 image 中，即 multi-stage 所阶段构建
COPY --from=0 /go/src/github.com/sparkdevo/href-counter/app .
```

**ADD**

```markdown
格式：
ADD <src> <dest>

用途一：
# 解压压缩文件并且把它们添加到镜像中
ADD nickdir.tar.gz .

用途二：
# 从 URL 拷贝文件到镜像中，但是官方建议不要这样用，应该使用 curl 或者 wget 代替
# 因为这样用会在 image 中新加一层，image 会变得更大
ADD http://example.com/big.tar.xz /usr/src/things/
```

### 9. Docker 容器在任何给定时间点处于什么状态？什么命令可以查看？

```markdown
Docker 可能有四种状态：运行、暂停、重启、已退出。
使用 `docker ps -a` 可以查看列出所有状态的容器列表。
```

### 10. Dockerfile 中最常见的指令是什么？

```markdown
FROM
# 为后续指令设置基本镜像，它都是第一条指令。
FROM <image>:<tag>

LABEL
# 添加元数据到镜像这种，一个 LABEL 是一个 key-value 对，比如声明构建信息、作者、机构、组织等
LABEL version="1.0" description="felord.cn" by="Felordcn"

RUN
# 用来执行构建镜像时执行的命令，RUN 指令创建的中间镜像会被缓存，会在下次构建中使用
# 如果不想使用缓存镜像，在构建的时候使用 --no-cache
RUN <command>
RUN apk update
RUN ["executable", "param1", "param2"]

CMD
# 构建容器后执行的命令
CMD command param1 param2  
CMD ["executable","param1","param2"]  
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

### 14. docker commit

```markdown
docker 可以将容器的 读写层 保存下来成为一个新的镜像，运行这个新镜像的话，就会拥有容器最后的文件变化。

格式：
docker commit [选项] <容器ID或容器名> [<仓库名>[:<标签>]]

使用：

```







































































































