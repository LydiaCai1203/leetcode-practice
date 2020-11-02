# 概述

Docker 是一个用于开发，发布和运行应用程序的开放平台。通过利用 Docker 的方法来快速交付，测试和部署代码。

## Docker 平台

Docker 提供了容器中打包和运行应用程序的功能。隔离性和安全性使您可以在给定主机上同时运行多个容器。

## Docker 引擎

Docker-engine 是具有以下主要组件的 客户端-服务器 应用程序：

+ 服务端(守护进程) - dockerd
+ REST API，它指定程序可以用来与守护程序进行通信并指示其操作的接口
+ 客户端 - docker 命令

## Docker 架构

### Docker 守护程序

dockerd 侦听 Docker API 请求并管理 Docker 对象。例如 图像，容器，网络和卷。守护进程之间可以相互通信，以管理 Docker 服务。

### Docker 客户端

使用 docker 命令使用 Docker API 与 dockerd 进行交互。

### Docker 仓库

仓库存储 Docker image, Docker Hub 是任何人都可以使用的公共仓库，并且默认情况下，Docker 已配置为在 Docker Hub 上寻找 image, 当然也可以运行私人的仓库。

### Docker 对象

**IMAGES**

一个 image 是创建一个 container 的只读模版，通常一个 image 基于另一个 image 创建，然后带上一些自定义配置。Dockerfile 每条指令都会在 image 中创建一个层, 当您要更改 Dockerfile 并重建 image 时，仅重建那些已更改的层。

**CONTAINERS**

container 是 image 的可运行实例，可以使用 Docker API 或 Docker CLI 创建、启动、停止、移动或删除。可以将容器连接到一个或多个网络，将存储连接到它，甚至根据其当前状态创建一个新的 image。

**example**

```shell
docker run -it ubuntu /bin/bash
```

+ 如果本地没有该 image，Docker 会将其从已配置的仓库中拉出, 等价于 `docker pull ubuntu`
+ Docker 会创建一个新的 container, 等价于`docker create contaienr`
+ **Docker 会将一个读写文件系统分配给容器，作为最后一层。**这允许运行中的容器在其本地文件系统中创建或修改文件或目录
+ **Docker 创建了一个网络接口，将容器连接到默认的网络。**默认情况下，容器可以使用主机的网络连接到外部网络
+ Docker 启动容器并执行 `/bin/bash` 
+ 当键入 `exit` 时，即终止 `/bin/bash` ，容器会停止不会被删除，可以重新启动或删除

**SERVICES**

service 允许你在多个 Docker 守护程序之间扩展容器。service 允许你定义在任何时间必须可用的服务副本的数量。默认情况下，多个工作节点是负载均衡的。

### 底层技术

Docker 使用 Go 编写

**Namespaces**

运行容器时，Docker 会为该容器创建一组 Namespaces, 提供了一层隔离。

+ pid命名空间：进程隔离（PID：进程ID）。
+ net命名空间：管理网络接口（NET：网络）。
+ ipc命名空间：管理访问IPC资源（IPC：进程间通信）。
+ mnt命名空间：管理文件系统挂载点（MNT：摩）。
+ uts命名空间：隔离内核和版本标识符。（UTS：Unix时间共享系统）。

**Control Groups**

将应用程序限制为一组特定的资源，控制组允许 Docker Engine 将可用的硬件资源共享给容器，并有选择地实施限制和约束。例如可以限制特定容器的可用内存。

**Union file systems**

Union file systems 或 UnionFS, 是通过创建 layer 进行操作的系统。Docker Engine 通过其为 container 提供构建 block。Docker Engine 还可以使用 AUFS、brfs、vfs、DeviceMapper.

**Container format**

Docker Engine 将 Namespaces、Control Group、UnionFS 组合到一个成为 Container format 的包装器中。