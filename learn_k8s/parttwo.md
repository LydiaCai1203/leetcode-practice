# PartTwo：k8s实践指南


[TOC]

-----------------------------
## 深入掌握Pod
### Pod定义文件
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: string
  namespace: string
  labels:
    - name: string
  annotations:
    - name: string
spec:
    containers:
    - name: string
      image: string
      imagePullPolicy: [Always | Never | IfNotPresent]  # 获取镜像的策略 是否每次都要尝试重新下载镜像
      command: [string]                                 # 容器的启动命令列表，如果不知地那个，使用镜像打包时使用的启动命令
      args: [string]
      workingDir: string                                # 容器的工作目录
      volumeMounts:
        - name: string
          monthPath: string
          readOnly: boolean
      ports:
      - name: string
        containerPort: int
        hostPort: int
        protocol: string
      env:
      - name: string
        value: string
      resources:
        limits:                                         # 下限
          cpu: string
          memory: string
        requests:                                       # 上限
          cpu: string
          memory: string
      ...
    volumes:
    - name: string
      configMap:
        name: string
        items:
        - key: string
          path: string
```
### Pod的基本用法
    在k8s系统中对长时间运行的容器的要求是：其主程序需要一直在前台执行，如果我们创建的Docker镜像的启动命令是一个后台执行程序，则在kubectl创建包含这个容器的Pod之后运行完该命令，就会认为这个Pod已经执行结束，将立刻销毁该Pod。如果为该Pod定义了ReplicationController，则系统将会监控到该Pod已经终止，之后根据RC定义中Pod的replicas的数量生成一定数量的Pod，然后循环往复。所以说，如果要在Pod里面起一个前端程序的话，就要有一条命令把这个Pod挂住。详情看：run.sh
### Pod内可以存在一个或者多个容器
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: string
  labels:
    name: string
spec:
  containers:
  - name: frontend
    image: string
    ports:
    - containerPort: 80
  - name: redis
    image: string
    port:
      containerPort: 6379
```
### 其它
    一个Pod中的多个容器之间相互访问时仅需要通过localhost就可以通信。

## 静态Pod
    静态Pod是由kubelet进行管理的仅存在于特定Node上的Pod。它们不能通过API Server进行管理，无法与ReplicationController、Deployment进行关联，并且kubelet也无法对它们进行健康检查。静态Pod总是由kubelet进行创建，并且总是在kubelet所在的Node上运行。
### 创建方式
+ 1. 配置文件方式
    + a. 需要设置kubelet的启动参数"--config"，指定kubelet需要监控的配置文件所在的目录
    + b. kubelet会定期扫描该目录，并根据目录中的yaml/json文件进行创建操作
    + c. 等待一会儿就可以查看本机中已经启动的容器了`docker ps`
    + d. `kubectl get pods` 也可以看到这个静态Pod
    + e. 由于静态Pod是无法通过API Server直接管理，所以在Master节点尝试删除这个Pod，只能使其状态变为pending,并不能删除。如果想要删除的话只能去删除对应的yaml文件。
+ 2. HTTP方式
    + a. 通过设置kubelet的启动参数"--manifest-url",kubelet将会定期从该url地址下载Pod的定义文件，并以yaml/json文件的格式进行解析，然后创建Pod。

## Pod容器共享Volume
    在同一个Pod中的多个容器能够共享Pod级别的存储卷Volume。

### example
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-pod
spec:
  containers:
  - name: tomcat
    image: tomcat
    ports:
    - containerPort: 8080
    volumeMounts:
    - name: app-logs
      mountPath: /usr/local/tomcat/logs
  - name: busybox
    image: busybox
    command: ["sh", "-c", "tail -f /logs/catalinas.log"]
    volumeMounts:
    - name: app-logs
      mountPath: /logs
  volumes:
  - name: app-logs
  emptyDir: {}
```

### command
+ `kubectl logs volume-pod -c busybox`这条命令用于查看容器的输出内容。
+ `kubectl exec -it volume-pod -c tomcat -- ls /usr/local/tomcat/logs`
+ `kubectl exec -it volume-pod -c tomcat -- tail`

### Pod的配置管理

#### ConfigMap 容器应用的配置管理
    ConfigMap以一个或者多个key:value的形式保存在kubernetes系统中供应用使用，既可以用于表示一个变量的值，也可以用于表示一个完整配置文件的内容
+ ConfigMap供容器使用的典型用法如下：
    + 1. 生成为容器内的环境变量
    + 2. 设置为容器启动命令的启动参数(需设置为环境变量)
    + 3. 以Volume的形式挂载为容器内部的文件或者是目录

#### ConfigMap的创建： yaml文件方式
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: string
data:
  apploglevel: info
  appdatadir: /var/data
```
#### command
+ 1. `kubectl get configmap configmap_name -o yaml`   # 以yaml的方式显示配置文件，当然也可以写成json
+ 2. `kubectl create -f configmap_filename`           # 创建都还是一样的方法
+ 3. `kubectl describe configmap configmap_name`      # 查看这个configmap的详细信息

#### ConfigMap的创建：kubectl命令行方式
    不使用yaml文件，直接通过kubectl create configmap也可以创建ConfigMap，可以使用参数 --from-file 或者是 --from-literal 指定内容。