# PartOne：基本概念和术语


[TOC]

-----------------------------
## Master
    指的是集群控制节点。集群里需要一个Master节点来负责整个集群的管理和控制，基本上Kubernetes所有的控制命令都是发给它的，它来负责具体的执行过程。我们执行的命令几乎基本都是在Master节点上运行的。Master节点通常会占据一个独立的X86服务器。因为它太重要了。
### Master节点上运行着以下一组关键进程
+ 1. Kubernetes API Server
        提供了HTTP REST接口的关键服务进程，是Kubernetes里所有资源的增删改查等操作的唯一入口，也是集群控制的入口进程。
+ 2. Kubernetes Controller Manager
        Kubernetes里所有资源对象的自动化控制中心，可以理解为资源对象的"大总管"
+ 3. Kubernetes Scheduler
        负责资源调度(Pod调度)的进程，相当于公交公司的调度室。

### ps
    master节点上往往还启动了一个etcd server进程，因为kubernetes里面所有资源对象的数据都是保存在etcd中的。

-----------------------------
## Node
    除了Master,Kubernetes集群中的其它机器被称为Node节点。Node节点可以是一台物理机器，也可以是一台虚拟机。Node节点才是Kubernetes集群中的工作负载节点，每个Node都会被Master分配一些工作负载（Docker容器）。当某个Node宕机时，其上的工作负载会被Master自动转移到其它的节点上去。
### Node节点上运行着以下一组关键进程
+ 1. kubelet
        负责Pod对应的容器的创建、启停等任务，同时与Master节点密切写作，实现集群管理的基本功能。
+ 2. kube-proxy
        实现Kubernetes Service的通信和负载均衡机制的重要组件。
+ 3. Docker Engine
        Docker引擎，负责本机的容器创建和管理工作。
### 特点
+ 1. Node节点可以在运行期间动态增加到Kubernetes集群中，前提是这个节点已经正确安装、配置、启动了上述关键进程。
+ 2. 默认情况下kubelet会向Master注册自己。
+ 3. 一旦Node被纳入集群管理范围，kubelet进程就会定时向Master节点汇报自身的情况，例如OS、Docker版本、机器的CPU和内存情况、之前有哪些Pod在运行等。这样Master就可以获知每个Node的资源使用情况，并实现高效均衡的资源调度策略。当某个Node超过指定时间不上报信息，会被Master判定为“失联”,Node的状态会被标记为不可用，随后Master会触发“工作负载大转移”的自动流程。
### 常用的命令
+ 1. kubectl get nodes                   # 查看集群中有多少个node
+ 2. kubectl describe node node_name     # 显示node的详细信息

-----------------------------
## Pod
    Pod由Pause-Container、User-Container1、User-container2...组成。其中Pause容器对应的镜像属于Kubernetes平台的一部分。其它的是用户业务容器。
### 为什么要有Pause容器
+ 1. 引入和业务无关而且不易死亡的Pause容器作为Pod的根容器，以它的状态代表整个容器组的状态。
+ 2. Pod里的多个业务容器共享Pause容器的IP，以及Pause容器挂接的Volume，这样可以简化业务容器之间的通信问题，和文件共享问题。
### PodIP
    Kubernetes为每个Pod都分配一个唯一的IP地址，称为PodIP。一个Pod里的多个容器共享PodIP地址。因为Kubernetes要求底层网络支持集群内任意两个Pod之间的TCP/IP直接通信。通常使用虚拟二层网络技术来实现。
### Pod类型
#### 普通的Pod
    放在Kubernetes的etcd存储里(一旦被创建)。被放倒etcd中的Pod，随后会被Kubernetes Master调度到某个Node上，并且被绑定。随后该Pod 被 对应的Node上的kubelet进程 实例化成一组相关的Docker容器并启动起来。在默认情况下，当Pod里的某个容器停止时，kubernetes会自动检测到这个问题并且重新启动这个Pod(相当于重启Pod里面所有的容器)。如果Pod所在的Node宕机，就会将这个Node上所有的Pod重新调度到其它的节点上。
#### 静态的Pod
    放在某个具体的Node上的一个具体文件中(只在此Node上启动运行)。
### Pod的资源定义文件(yaml or json)
```yaml
apiVersion: v1
kind: Pod
metadata:
    name: myweb                         # Pod的名字
    labels:
        name: myweb
spec:
    containers:
    - name: myweb
      image: kubeguide/tomcat-app:v1
      ports: 
      - containerPort: 8080
      env:
      - name: MySQL_SERVICE_HOST
        value: 'mysql'
      - name: MySQL_SERVICE_PORT
      value: '3306'
      resources:
        requests:                      # 可以分配的最小值 也就是必须要满足的
          memory: "64Mi"
          cpu: "250m"
        limits:                        # 资源配额的最大值 超出这个值kubernetes会kill掉这个pod
          memory: "128Mi"
          cpu: "500m"
```
+ endpoint
        这里Pod的IP加上这里的容器端口就是一个endpoint。它代表的是此Pod里的一个服务进程的对外通信地址。一个Pod存在具有多个endpoint的情况。
+ PodVolume
        定义在Pod之上然后被各个容器挂载到自己的文件系统中去的。
+ Event
        是一个事件的记录，记录了事件的最早产生时间、最后重现时间、重复次数、发起者、类型，以及导致此次事件的原因等众多的信息。Event通常会被关联到某个具体的资源对象上，是排除故障的重要参考信息。当我们发现一个Pod迟迟无法创建成功的时候，我们可以使用`kubectl get describe pod pod_name`来查看它的描述信息，用来定位原因。
+ CPU/Memory配额
        在Kubernetes里，通常以千分之一的CPU配额为最小单位,用m来表示。通常一个容器的CPU配额被定义为100-300m，即占用0.1-0.3个CPU。 这个配额值无论是在只有1核还是48核的电脑上，都是一样的大小。Memory的大小也是绝对值，单位是内存字节数。

-----------------------------
## Label
    一个Label是以一个key=value的形式存在的，可以附加到各种资源对象上，如Node、Pod、Service、RC等等。一个资源对象也可以定义任意数量的Label，同一个Label可以被添加到任意数量的资源对象上去。Label通常在资源对象定义时确定，也可以在对象创建后动态添加或者删除。Label的功能是给资源管理对象分组管理。

    事实上，当我们给资源对象打上标签以后，就可以通过Label Selector来查询和筛选拥有某些Label的资源对象。实现一种类似SQL的简单又通用的对象查询机制。
### 使用
+ 1. `name=redis-slave`
+ 2. `env!=production`
+ 3. `name in (redis-master, redis-slave)`
+ 4. `name not in (redis-master, redis-slave)`
+ 5. `` name=redis-slave, env=production`                       # 逗号就相当于and

-----------------------------
## Replication Controller
    它其实是定义了一个期望的场景，即声明某种Pod的副本数量在任意时刻都符合某个预期值。RC的定义会包含以下几个部分：Pod期待的副本数(replicas)、用于筛选目标Pod的Label Selector、当Pod的副本数量小于预期的数量时，用于创建新Pod的Pod模版(Template)
### example
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    tier: frontend
  template:
    metadata:
      labels:
        app: app-demo
        tier: frontend
    spec:
      containers:
      - name: tomcat-demo
        image: tomcat
        imagePullPolicy: IfNotPresent
        env:
        - name: GET_HOST_FROM
          value: dns
        ports:
        - containerPort: 80
```
```yaml
apiVersion: extensions/v1beta1
kind: ReplicaSet
metadata:
  name: frontend
spec:
  selector:
    matchLabels:
      tier: frontend
    matchExpressions:
      - {key: tier, operator: In, values: [frontend]}
  template:
    ......
```

        当我们定义了一个RC并提交到kubernetes集群中后，Master节点上的Controller Manager组件就会得到通知，定期地巡检系统中当前存活的额Pod，并确保目标Pod实例的数量刚好等于此RC的期望值。上面的这个例子就是确保tier=frontend标签的这个Pod在整个Kubernetes集群中始终只有一个副本。删除RC并不会影响已经创建好的Pod，如果要删除Pod,只要将replicas设置为0即可。kubectl也提供stop和delete来一次性删除RC和RC所控制的全部Pod。

### command
+ 1. `kubectl scale rc redis-slave --replicas=3`
### 总结
    Replica Set 和 Deployment这两个重要资源对象逐步替换了之前RC的作用。
+ 1. 大多数情况下我们通过定义一个RC实现Pod的创建过程以及副本数量的自动控制。
+ 2. RC里面包括完整的Pod定义模版。
+ 3. RC通过Label Selector机制实现对Pod副本的自动控制。
+ 4. 通过改变RC里面Pod模版中的镜像版本，可以实现Pod的滚动升级功能。

-----------------------------
## Deployment
    Deployment是Kubernetes1.2引入的新概念。Deployment在内部使用了Replica Set来实现目的，可以将Deployment看成是RC的一次升级。
### Deployment的典型使用场景
+ 1. 创建一个Deployment对象来生成对应的Replica Set并完成Pod副本的创建过程
+ 2. 检查Deployment的状态来看部署动作是否完成
+ 3. 更新Deployment以创建新的Pod
+ 4. 如果当前Deployment不稳定，则回滚到一个早先的Deployment版本
+ 5. 刮起或者恢复一个Deployment
### Deployment和Replica Set的区别
```yaml
apiVersion: extensions/v1beta1                         apiVersion: v1
kind: Deployment                                       kind: ReplicaSet
metadata:                                              metadata:
  name: nginx-deployment                                 name: nginx-repset
```
### example
```yaml
apiVersion: extensions/v1beta
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 1
  selector:
    matchLabels:
      tier: frontend
    matchExpressions:
    - {key: tier, operator: In, values: [frontend]}
  template:
    metadata:
      labels:
        app: app-demo
        tier: frontend
    spec:
      containers:
      - name: tomcat-demo
      image: tomcat
      imagePullPolicy: IfNotPresent
      ports:
      - containerPort: 8080
```
### command
+ 1. `kubectl create -f tomcat-deployment.yaml`     # 在当前路径下存在这个文件
+ 2. `kubectl get deployment`
    + DESCRIBE: Pod副本数量的期望值 Deployment文件中的Replica
    + CURRENT: 当前Replica的值，这个值会一直增加直到到达DESCRIBE
    + UP-TO-DATE: 最新版本的Pod的副本数量，在滚动升级中，有多少个Pod副本已经成功升级
    + AVAILABLE: 当前集群中可用的Pod的副本数量，也就是存活的Pod的数量
+ 3. `kubectl get rs`
+ 4. 
