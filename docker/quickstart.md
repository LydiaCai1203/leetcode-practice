# QuickStart

`docker run --publish 8000:8080 --detach --name bb bulletboard:1.0`
+ --publish 要求 Docker 将主机端口的 8000 上传入的流量转发到容器端口 8080, 如果不这样写，作为默认安全状态，防火墙规则将组织所有网络流量到达容器。
+ --detach 要求 Docker 在后台运行此容器。
+ --name 指定一个容器名称

`docker rm --force bb`
或者
`docker stop bb`
`docker rm bb`
