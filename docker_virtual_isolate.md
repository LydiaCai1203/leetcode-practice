## Docker 基础技术

### Linux Namespace

Linux Namespace 是 Linux 提供的一种内核级别 **环境隔离** 的方法。

**example**

`chroot` 更改根目录命令，在 Linux 中，系统默认的目录结构都是以 `/` 开始，使用 `chroot` 以后，系统的目录结构将以 **指定位置** 代替 `/` 成为根目录。这样 `chroot` 内部的文件系统无法访问外部的内容。

**Linux 有如下是三个系统调用：**

+ `clone` - 用来创建一个新进程，通过一些参数达到隔离目的。
+ `unshare` - 使某个进程脱离某个 namespace
+ `setns` - 把某个进程加入到某个 namespace

### UTS Namespace

用于设置该命名空间中正在运行的进程可见的 主机名 和 NIS 域名。在容器内运行的进程通常不需要知道主机名和域名，因此不因与主机共享 UTS 命名空间。

```c++
int container_main(void* arg)
{
    printf("Container - inside the container!\n");
    sethostname("container",10);                        /* 设置hostname */
    execv(container_args[0], container_args);
    printf("Something's wrong!\n");
    return 1;
}
int main()
{
    printf("Parent - start a container!\n");
    int container_pid = clone(                          /*启用CLONE_NEWUTS Namespace隔离 */
      container_main,
      container_stack+STACK_SIZE, 
      CLONE_NEWUTS | SIGCHLD,                           /*Mount namespaces*/
      NULL
    );              
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

### IPC Namespace

IPC 是进程间通信的一种方式，有 共享内存、信号量、消息队列等方法。将 IPC 隔离，就是意味着只有在同一个 namespace 下的进程才能互相通信。

```c++
int container_pid = clone(
  container_main,
  container_stack+STACK_SIZE, 
  CLONE_NEWUTS | CLONE_NEWIPC | SIGCHLD,                /*IPC namespaces*/
  NULL
);
```

`ipcmk -Q` 创建 IPC 资源：一个消息队列

`ipcs -q` 显示有关 IPC 设施的信息，-q 就是显示消息队列的信息

```shell
root@b2035168e992:/data# ipcs -q

------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages
0xd32b27e4 0          root       644        0            0
```

运行了上述程序以后，再执行 `ipcs -q` 就会发现已经隔离了，看不见创建了的 mq 的信息了。

###PID Namespace

Linux 中，`PID = 1` 的进程是 init 进程，如果某个进程脱离了父进程，init 进程就会负责回收资源并结束这个子进程。所以要做到进程空间的隔离，就要创建出 `PID = 1` 的进程。

```c++
int container_main(void* arg)
{
    /* 查看子进程的PID，我们可以看到其输出子进程的 pid 为 1 ; echo $$ 即可查看*/
    printf("Container [%5d] - inside the container!\n", getpid());
    sethostname("container",10);
    execv(container_args[0], container_args);
    printf("Something's wrong!\n");
    return 1;
}
int main()
{
    printf("Parent [%5d] - start a container!\n", getpid());
    /*启用PID namespace - CLONE_NEWPID*/
    int container_pid = clone(
      container_main, 
      container_stack+STACK_SIZE, 
      CLONE_NEWUTS | CLONE_NEWPID | SIGCHLD, 
      NULL
    ); 
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

### Mount Namespace

即使进行了上述的操作以后，使用 `ps`、`top` 这些命令，还是可以看到所有的进程。因为这些命令会去读 `/proc` 文件系统，而 `/proc` 文件系统在父进程和子进程中都是一样的，所以命令显示的东西也是一样的。

```c++
int container_main(void* arg)
{
    printf("Container [%5d] - inside the container!\n", getpid());
    sethostname("container",10);
    /* 重新mount proc文件系统到 /proc下 */
    system("mount -t proc proc /proc");
    execv(container_args[0], container_args);
    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    printf("Parent [%5d] - start a container!\n", getpid());
    /* 启用Mount Namespace - 增加CLONE_NEWNS参数 */
    int container_pid = clone(
      container_main, 
      container_stack+STACK_SIZE, 
			CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | SIGCHLD, 
      NULL
   	);
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

现在我们使用 `ps` 也只能看到两个进程了。

```shell
hchen@ubuntu:~$ sudo ./pid.mnt
Parent [ 3502] - start a container!
Container [    1] - inside the container!
root@container:~# ps -elf 
F S UID        PID  PPID  C PRI  NI ADDR SZ WCHAN  STIME TTY          TIME CMD
4 S root         1     0  0  80   0 -  6917 wait   19:55 pts/2    00:00:00 /bin/bash
0 R root        14     1  0  80   0 -  5671 -      19:56 pts/2    00:00:00 ps -elf
```

`CLONE_NEWNS` 创建 mount namespace 以后，父进程会把自己的文件结构复制到子进程中，子进程中新的 namespace 中所有的 mount 操作都只会影响自身的文件系统。

### User Namespace

Linux 给每个用户都分配了一个 **UID**，这个数字用于标识系统的用户并确定用户可以访问哪些系统资源。

Linux 给每个组都分配一个 **GID**，每个用户都有一个用户组，系统可以对一个用户组中的用户进行集中管理。

User Namespace 用了 `CLONE_NEWUSER` 这个参数，用了以后，内部看到的 UID 和 GID 就已经与外部不同了，**默认显示 65534**。因为容器找不到真正的 UID，所以设置了一个最大的 UID。要把容器中的 UID 和 真实系统中的 UID 映射在一起，就需要修改 `/proc/<pid>/uid_map` 和 `/proc/<pid>/gid_map` 这两个文件。

*这两个文件格式为：*`ID-inside-ns  ID-outside-ns  length`

`length` 字段表示映射的范围，一般填 1，表示一一对应。`0  1000 1` 就表示把容器内 UID=0 映射为真实系统里的 UID=1000。

```c++
int container_main(void* arg)
{

    printf("Container [%5d] - inside the container!\n", getpid());

    printf("Container: eUID = %ld;  eGID = %ld, UID=%ld, GID=%ld\n",
            (long) geteuid(), (long) getegid(), (long) getuid(), (long) getgid());

    /* 等待父进程通知后再往下执行（进程间的同步） */
    char ch;
    close(pipefd[1]);
    read(pipefd[0], &ch, 1);

    printf("Container [%5d] - setup hostname!\n", getpid());
    //set hostname
    sethostname("container",10);

    //remount "/proc" to make sure the "top" and "ps" show container's information
    mount("proc", "/proc", "proc", 0, NULL);

    execv(container_args[0], container_args);
    printf("Something's wrong!\n");
    return 1;
}

int main()
{
    const int gid=getgid(), uid=getuid();

    printf("Parent: eUID = %ld;  eGID = %ld, UID=%ld, GID=%ld\n",
            (long) geteuid(), (long) getegid(), (long) getuid(), (long) getgid());

    pipe(pipefd);
 
    printf("Parent [%5d] - start a container!\n", getpid());
	
  	// 创建了一个子进程
    int container_pid = clone(
      container_main, 
      container_stack+STACK_SIZE, 
      CLONE_NEWUTS | CLONE_NEWPID | CLONE_NEWNS | CLONE_NEWUSER | SIGCHLD, 
      NULL
    );
    
    printf("Parent [%5d] - Container [%5d]!\n", getpid(), container_pid);

		// UID 映射，都映射为容器中的 root 用户
    set_uid_map(container_pid, 0, uid, 1);
    set_gid_map(container_pid, 0, gid, 1);

    printf("Parent [%5d] - user/group mapping done!\n", getpid());

    /* 通知子进程 */
    close(pipefd[1]);

    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

### Network Namespace

这里的网络隔离还是没有看明白，还需要再做理解！！！！！！！！！！！

**网卡**：

```markdown
一、将电脑的数据封装为帧，并通过网线将数据发送到网络上去。
二、接受网络上其它设备传过来的帧，将帧重新组合成数据，发送到所在的电脑中。

(一般计算机用户不需要用独立网卡，集成网卡即可。不过独立网卡有时也能起到保护主板的作用，比如打雷时，怕闪电的电压烧到主板，网卡就可以起到保护主板的作用。)
```

**网桥**：

```markdown
网桥工作在数据链路层，数据链路层地址就是 mac 地址，网桥与 hub 的区别就在于，网桥会过滤 mac，只有目的 mac 地址匹配的数据才会发送到出口。
```

![](/Users/cqj/project/private/leetcode-practice/docker_network.jpg)

```markdown
1. ip 包会从 container 发往自己默认的网关 docker0，包到达 docker0 的时候就相当于到达了主机。
2. 这时会查询主机的路由表，发现包应该从主机的网卡 eth0 出去。
```

### Linux CGroup

namespace 解决的主要是 环境隔离 的问题，cgroup 解决的是 计算机资源 使用上的隔离。

Linux CGroup 全称为 (Linux Control Group) 是 Linux 内核的一个功能，用来限制、控制、分离一个进程组群的资源(CPU、内存、磁盘输入输出、网络带宽 等)。

+ 隔离一个进程集合，限制它们所消费的资源，比如绑定 CPU 的核
+ 为这组进程分配足够使用的内存
+ 为这组进程分配相应的网络带宽和磁盘存储限制
+ 显示访问某些设备(通过设置设备的白名单)

```markdown
1. CGroup 在 Linux 内部实现是一个文件系统的形式， 比如 “/sys/fs/cgroup/cpuset”

2. 假如你要限制某个进程的 CPU 使用率
	a. echo 20000 > /sys/fs/cgroup/cpu/haoel/cpu.cfs_quota_us     20% 的意思
	b. echo 3529 >> /sys/fs/cgroup/cpu/haoel/tasks
	
3. 假如你要限制内存使用
	a. mkdir /sys/fs/cgroup/memory/haoel
	b. echo 64k > /sys/fs/cgroup/memory/haoel/memory.limit_in_bytes
	c. echo [pid] > /sys/fs/cgroup/memory/haoel/tasks 
```

### CGroup 的术语

**任务**

```markdown
系统的一个进程
```

**控制组**

```markdown
一组按照某种标准划分的进程。CGroup 中的资源控制都是以控制组为单位实现的，一个进程可以加入到某个控制组上，资源的限制都是定义在这个组上。简单来说，CGroup 的呈现就是一个目录带一系列的可配置文件。
```

**层级**

```markdown
控制组可以组织称一棵控制组的树，控制组上子节点继承了父节点的属性。
```

**子系统**

```markdown
一个子系统就是一个资源控制器，比如CPU子系统就是控制CPU时间分配的一个控制器。子系统必须附加到一个层级上才能起作用，一个子系统附加到某个层级以后，这个层级上的所有控制族群都受到这个子系统的控制。Cgroup的子系统可以有很多，也在不断增加中。
```

