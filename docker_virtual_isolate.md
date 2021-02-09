## Docker 基础技术

### Linux Namespace

Linux Namespace 是 Linux 提供的一种内核级别 **环境隔离** 的方法。

**example**

`chroot` 更改根目录命令，在 Linux 中，系统默认的目录结构都是以 `/` 开始，使用 `chroot` 以后，系统的目录结构将以 **指定位置** 代替 `/` 成为根目录。这样 `chroot` 内部的文件系统无法访问外部的内容。

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
      CLONE_NEWUTS | SIGCHLD, 
      NULL
    );              
    waitpid(container_pid, NULL, 0);
    printf("Parent - container stopped!\n");
    return 0;
}
```

### IPC Namespace

IPC 是进程间通信的一种方式，有 共享内存、信号量、消息队列等方法。







**example 2**：

`PID Namespace` 对 PID 重新标号，即不同的 `PID Namespace` 下的进程可以有同一个 PID。内核为所有的 `PID Namespace` 维护一个树状结构，最顶层的是系统初始化所建，被称为 `Root Namesoace`，由它创建的新的 `PID Namespace` 称为它的 `Child Namespace`。父节点可以看到子节点中的进程，可以通过信号对子节点的进程产生影响，子节点无法看见父节点 `PID Namespace` 里的进程。

当一个进程的父进程退出后，该进程就会变成孤儿进程，孤儿进程就会被当前 `PID Namespace` 中 PID 为 1 的进程接管，而非最外层系统级别的 init 进程接管。



