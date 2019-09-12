FROM ubuntu:18.04

# 在原文件中进行修改，将archive.ubuntu.com替换成mirrors.aliyun.com
# RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
# 删除所有已经下载的包文件
RUN apt-get clean
# 安装python3 h和 supervisor
RUN apt update -y && apt install python3-pip locales supervisor -y

# 设置语言环境
RUN locale-gen en_US.UTF-8
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
# DEBIAN_FRONTEND 是一个环境变量 noninteractive就是直接运行命令 无须向用户请求输入，这对于在使用apt-get的时候格外有用
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata
# 需要在不同的目录下用到相同的文件时使用。软连接就是只会在你选定的位置生成一个文件镜像，硬链接会在选定的位置上生成一个大小相同的文件。
# 后面的这个目录是软连接指向前面的目录
RUN ln -fs /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
# 显示安装后的包的配置信息 就是看一下tzdata安装了没安装
RUN dpkg-reconfigure --frontend noninteractive tzdata
# 将当前目录下的所有文件都复制到/project目录下
ADD . /project
# 不要pip安装缓存
RUN cd /project && pip3 install --no-cache-dir -r requirements.txt

COPY learn_k8s.conf /etc/supervisor/conf.d/

COPY run.sh /

RUN chmod +x run.sh

CMD ["/run.sh"]

# 创建img的时候使用, 其中.代表的是dockerfile文件在当前目录下
# docker build -t name:tag .