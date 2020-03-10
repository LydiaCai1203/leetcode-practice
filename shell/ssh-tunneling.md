# Comprehensive Guide on SSH Tunneling

#####         听豪哥说过不止一次内网穿透，但是不知道其原理到底是什么，觉得很神奇，所以想学习一下。网上找到一篇文章，链接写在这里了👇，用我飘过CET6的渣渣英文水平翻译一下，希望能帮助到看这个笔记的你。

[Comprehensive Guide on SSH Tunneling](https://www.hackingarticles.in/comprehensive-guide-on-ssh-tunneling/)

[来了解一下什么是防火墙](https://m.yisu.com/news/id_398.html)

[socks5稍微了解一下](http://zhihan.me/network/2017/09/24/socks5-protocol/)

[我觉得ss的原理也需要了解一下](https://segmentfault.com/a/1190000011862912)

​    Basically, tunneling is a process which allows data sharing or communication between two different networks privately. Tunneling is normally performed through encapsulating the private network data and protocol information inside the public network broadcast units so that the private network protocol information visible to the public network as data. 

​    基本上，隧道是一个允许两个不同的网络私下进行数据共享和数据交换的过程。隧道通常表现为在公有网络广播单元中封装私有网络数据和协议信息以便于私有网络的协议信息像数据一样对于公有网络可视化。

​    **SSH Tunnel:** Tunneling is the concept to encapsulate the network protocol to another protocol here we put into SSH, so all network communication is encrypted. Because tunneling involves repackaging the traffic data into a different form, perhaps with encryption as standard, a third use is to hide the nature of the traffic that is run through the tunnels.

​    **SSH 隧道**：隧道是将一种网络协议封装到另一种网络协议中的概念。这里就是将某种网络协议封装到SSH中，所以，所有的网络联系都是加密过的。因为隧道会以另一种形式重新包装这些流量数据。以上交待了隧道的两种用途，第三种用途是隐藏通过隧道的流量的特性。

### **Types of SSH Tunneling:**   

1. Dynamic SSH tunneling
2. Local SSH tunneling
3. Remote SSH tunneling

### **几种 SSH 隧道类型**

1. 动态 SSH 隧道
2. 本地 SSH 隧道
3. 远程 SSH 隧道

**Let’s Begin!!**

**让我们开始八八八八八!!**

**Objective:** To establish an SSH connection between remote PC and the local system of the different network.

Here I have set my own lab which consists of three systems in the following network:

**SSH server** (two Ethernet interface) 

IP 192.168.1.104 connected with the remote system

IP 192.168.10.1 connected to local network system 192.168.10.2

**SSH client** (local network) holds IP 192.168.10.2

**Remote system** (outside the network)

In the following image, we are trying to explain the SSH tunneling process where a remote PC is trying to connect to 192.168.10.2 which is on INTRANET of another network. To establish a connection with **an SSH client (raj)**, remote PC will create an SSH tunnel which will connect with the local system via **SSH server (Ignite)**.

**目标**: 对于处于两个不同网络中的 远程PC端 和 本地系统 建立 SSH 连接。我在自己的实验室里建立了以下三种系统。

**SSH 服务端(两个以太网接口)**

IP 192.168.1.104 用于连接远程系统

IP 192.168.10.1 用于连接本地系统 192.168.10.2

**SSH 客户端(本地网络)** IP 192.168.10.2

**远程系统(外部网络)**

在以下图片中，我们会尝试解释 SSH 隧道过程。远程 PC 尝试连接在另一个网络(INTRANET)中的 192.168.10.2。远程 PC 会通过创建 SSH 隧道来和 **SSH 客户端**建立连接，远程PC 和 本地系统 通过 **SSH 服务端** 进行联系。

ps: Internet 指的是因特网/外网；Intranet 指的是内部/内网

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-1.jpg)

​    Given below image is describing the network configuration for **SSH server** where it is showing two IP 192.168.1.104 and another 192.168.10.1

​    下图给出 SSH server 上的网络配置。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunnrling-2.png)

​    Another image given below is describing network configuration for **SSH client** which is showing IP 192.168.10.2

​    以下这张图给出了 SSH client 上的网络配置

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-3.png)

### **Dynamic SSH Tunneling through Windows**

​    **Remote Pc** is trying to connect to **SSH server** (**192.168.1.104**) via **port 22** and get successful login inside the server. Here we had used putty for establishing a connection between SSH server (Ubuntu) and remote user (Windows).

### **动态 SSH 隧道**

​    远程PC 尝试通过 22端口 连接 SSH 服务端，这里我们用PuTTY来建立 SSH服务端(ubuntu) 和 远程PC(Windows) 之间的连接。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-4.png)

​    Similarly now Remote PC trying to connect with **Client PC** (**192.168.10.2**) via **port 22**, since they belong to the different network, therefore, he receives network error.

​    远程PC 尝试通过22端口连接 本地PC(192.168.10.2)，因为它们处于不同的网络，所以远程PC会收到错误连接信息。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-5.png)

### **Dynamic SSH Tunneling through Kali Linux on Port 80**

​    Now we are employing Kali Linux for SSH tunneling and demonstrating how an attacker or Linux user can take the privilege of Tunneling and can establish an SSH connection with client systems.

` ssh -D 7000 ignite@192.168.1.104`

​    Enter the user’s password for login and get access to the **SSH server** as shown below.

### **动态 SSH隧道 通过 Kali 80端口 建立**

​    现在我们使用 Kali Linux 进行 SSH隧道 传输，并演示攻击者或是 Linux 用户如何获取隧道特权，以及如何与本地系统进行 SSH连接。

`ssh -D 7000 ignite@192.168.1.104`

让8080端口的数据，都通过ssh传向 192.168.1.104. SSH 会建立一个socket，去监听本地的 7000 端口，一旦有数据传向7000端口，就自动把它转移到 SSH 连接上面，发往远程主机。现在7000端口变成了一个加密端口。

​    输入使用者的密码登录以获取 SSH服务器 访问权。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-6.png)

Install tsocks through apt repository using the command:

执行 `apt install tsocks`

**tsocks** – Library for intercepting outgoing network connections and redirecting them through a SOCKS server. 

**tsocks** - 用于拦截传出网络的连接并且通过 SOCKS 服务端 来重定向它们。

也就是说，stocks 可以让本机上的任何软件通过 socks 代理上网的工具，它是一个透明的 socks 代理软件，只要你电脑有一个连接到国外服务器的ssh隧道，你就能让任何软件翻墙。shadowsocks 内部也是使用的socks5协议。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-7.png)

Open the **tsocks.conf** file for editing socks server IP and port, in our case we need to mention below two lines and then save it.

Server = 127.0.0.1

Server_port = 7000

打开 /usr/local/etc/tsocks.conf 文件，配置上 server 和 server_port; 在我们的例子中，我们需要注意以下两行并且保存它们。

Ps: 我看过很多教程，对server这行的注释都是"远程服务器的地址", 如果你搭建的是ssh隧道，server应该填的是127.0.0.1；tsocks将数据发到本地7000端口，ssh隧道监听本地7000端口，然后将数据加密，传输到远程服务器，远程服务器解密数据以后将数据转发到正确的目标地址，从而实现翻墙。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-8.png)

Now connect to SSH client with the help tsocks using given below command.

现在在tsocks的帮助下通过ssh连接192.168.10.2

`tsocks ssh raj@192.168.10.2`

Enter the password and enjoy the access of SSH client.

输入密码你就可以获得访问权限了，牛皮。

### **Local SSH Tunneling through Kali Linux**

Now again we switch into Kali Linux for local tunneling which is quite easy as compared to dynamic. Execute given below command for forwarding port to the local machine.

### **本地 SSH 隧道搭建**

现在我们通过 Kali Linux 来进行本地隧道的搭建，这样更易于同动态隧道的搭建做对比。执行以下的命令将端口转发到本地计算机。

`ssh -L port:host:port user@server`

`ssh -L 7000:192.168.10.2:22 ignite@192.168.1.104`

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-9.jpg)

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-10.png)

ps: 这里我摘取了阮一峰老师博文里面的一段话解释一下本地端口转发是什么：有时候绑定本地端口还不够，还必须指定数据传送的目标主机，从而形成点对点的“端口转发”。这里我们把这种情况称为本地端口转发。指定host1是本地主机，host2是远程主机，另外有一台host3可以同时连通前面两台机器。host1通过host3连上host2。

上述命令的意思是指定本地7000端口，指定将192.168.1.104上的所有数据，转发到目标主机192.168.10.2上面的22端口。

Now open a new terminal and type below command for connecting to SSH client.

现在打开终端然后输入一下命令为了于SSH client 建立连接。

`ssh raj@127.0.0.1 -p 7000`

**Awesome!!** We have successfully access SSH client via port 7000 

太棒了，现在我们能通过登录本机的7000端口连上192.168.10.2。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-11.png)

### **Remote SSH Tunneling through Ubuntu**

If you are not willing to use putty for remote tunneling then you can execute the following command

### **远程 SSH 隧道通过 Ubuntu 建立**

如果你不愿意用PuTTY来建立远程隧道，你可以执行一下命令

`ssh -R 7000:192.168.10.2:22 root@192.168.1.108`

Here 192.168.1.10.2 is our local client (raj) IP and 192.168.1.108 is our remote system IP.

这里 192.168.10.2 是本地客户端，192.168.1.108 是远程系统的IP.

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-12.png)

Come back to the remote system and enter the following command to with SSH client machine.

回到远程系统，并在 SSH 客户端计算机上键入以下命令。

`ssh raj@127.0.0.1 -p 7000`

From given below image you can observe that we had successfully connected with SSH client machine via port 7000.

从下面的图像中可以看到，我们已经通过端口7000成功连接到了 SSH 客户端计算机。

![](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/ssh-tunneling-13.png)

Ps: 这里再引用一下阮一峰老师博客里的话来解释一下上面的命令，远程端口转发指的是绑定远程端口的转发。host1与host2之间无法连通，必须借助host3转发，但是特殊情况出现了，host3是一台内网机器，它可以连接外网的host1，反过来不行。外网的host1连不上内网的host3。这时本地端口转发就不能用了。

这时候就用到远程端口转发，也就是在host3上执行

`ssh -R 2121:host2:21 host1` 

让host1监听它自己的2121端口，然后将所有的数据经由host3，转发至host2的21端口。这样绑定以后，我们就可以在host1连接host2了。这里必须指出，"远程端口转发"的前提条件是，host1和host3两台主机都有sshD和ssh客户端。