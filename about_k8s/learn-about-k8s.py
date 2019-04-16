"""
学习k8s过程中遇到的一些概念问题：
1. kubectl 是 Kubernetes API交互的命令行程序

2. 集群（cluster）
集群是由一组节点组成的 这些节点可以是物理服务器或者虚拟机 在这些节点之上安装了kubernetes平台

3. pod
安排在节点上，包含了一组容器和卷，同一个pod的容器共享一个网络命名空间，可以使用localhost进行
通信，pod是短暂的，不是持续性的实体
a. 创建一份容器的多份拷贝，可以手动创建单个pod, 再使用replication controller拷贝出多份
b. 重启pod的时候可能造成ip地址变化，前端容器如果想要指向后端容器的话就需要使用service
c. 可以使用持久化的卷类型

4. lable
一些pod有label, 一个label是attach到pod的一个键值对，用来传递用户定义的属性
label = (tier=frontend, app=myapp) 用来标记前端容器
label = (tier=backend, app=myapp)  用来标记后台pod
使用selectors选择带有特定label的pod

5. replication controller  --> pod模版 label
确保任意时间都有指定数量的pod副本在运行，如果为某个pod创建了replication controller并且指定
3个副本，它就会创建3个pod，并且持续监控它们，如果某个pod不响应，那么replication controller
会替换它，始终保持总数为3. 如果之前不响应的pod恢复了，replication controller就会将其中一个
进行终止，总之保持总数为3.

6. service
def: 定义一系列pod以及访问这些pod的策略的一层抽象。service通过label找到pod组。
假设现在有两个后台pod, 并且定义后台service的名称为backend-service,label选择器为（tier=backend, app=myapp）

7. node
物理或者是虚拟机器，作为kubernetes worker, 通常称为Minion, 每个节点都有这几个部分
a. kubelet 主节点代理
b. kube-proxy  service使用其将链接路由到pod
c. docker/rocket  kubernetes使用容器的技术来创建容器

8. kubernetes master
cluster中会有一个，拥有一系列组件

"""