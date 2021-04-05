## 第七章：中断和中断处理

```markdown
为了让处理器和外部设备(硬盘、蓝光碟机、键盘、鼠标等)能协同工作。

有一种方法是，让处理器向硬件发出一个请求，专门等待回应的方法，显然不行。应为处理器的速度和外围硬件设备的速度不再一个数量级上。因此内核该在此区间处理其他事务，等硬件完成了请求的操作后，再回头处理。

另一种方法是，让硬件在需要的时候再向内核发出信号，这就是中断机制。
```

### 7.1 中断

```markdown
硬件设备产生中断信号，直接送入中断控制器的输入引脚中。中断控制器就是一个简单的电子芯片，作用是将多路中断管线采用 复用技术 只通过一个和处理器相连的管线与处理器通信。中断控制器给处理器发送一个电信号，处理器接收此信号后，中断自己的当前工作，然后通知 OS 产生中断，让 OS 对中断进行处理。中断随时都可以产生，内核随时可能因为新到来的中断而被打断。
```

```markdown
每个中断都有一个唯一的数字标志，从而使得 OS 能对中断进行区分，知道是哪个硬件设备产生的。这样 OS 才能给不同的中断提供对应的中断处理程序。这些中断值通常被成为中断请求(IRQ)线。比如 IRQ0 是时钟中断，IRO1 是键盘中断。但是对于连接在 PCI 总线上的设备而言，中断是动态分配的。特定的中断总是与特定的设备相关联，并且内核要知道这些信息。
```

**异常**

```markdown
异常在产生时必须考虑与处理器时钟同步，因此，异常也常常被称为是同步中断。在处理器执行到由于编程失误而导致的错误指令时，或者在执行期间出现特殊情况(缺页)，必须靠内核来处理的时候，处理器就会产生一个异常。
```

### 7.2 中断处理程序

```markdown
在响应一个特定中断的时候，内核会执行一个函数，这个函数叫做中断处理程序(interrupt handler) 或 中断服务例程(interrupt service routine, ISR)。产生中断的每个设备都有一个相应的中断处理程序。设备驱动程序就是用于对设备进行管理的内核代码，包括了针对该设备产生的中断处理程序。
```

```markdown
在 Linux 中，中断处理程序就是普通的 C 函数，只不过必须按照特定的类型声明，以便内核以标准的方式传递处理程序的信息。它与内核函数的真正区别在于，中断处理程序是被内核调用来响应中断的，运行于中断上下文中。
```

```markdown
中断可能随时发生，中断处理程序也就随时可能执行。因此必须保证中断处理程序能够快速执行，才能保证尽可能地恢复中断代码的执行。中断处理程序需要做到：1.通知硬件设备中断已被接收。2.完成大量其他的工具(网络设备的中断处理程序需要将来自硬件的网络数据包拷贝到内存，对其进行处理再交给合适的协议栈或者应用程序)。
```

### 7.3 上半部 和 下半部 的对比

```markdown
目标：1. 希望处理器即使对中断进行响应。2. 希望中断处理程序尽快执行完成，才能尽快恢复被中断的代码的执行。这两个目标是有冲突的。

中断处理程序的上半部，接收到一个中断，它就立即开始执行，只做有严格时限的工作。例如对接收的中断进行应答或复位硬件。

中断处理程序的下半部，负责处理能够被允许稍后完成的工作。此后，在合适的时机，下半部会被执行。
```

```markdown
例子：
当网卡接收到来自网络的数据包时，需要通知内核数据包到了。网卡需要立即完成这件事(发出中断)，从而优化网络的吞吐量和传输周期，以避免超时。内核通过执行网卡已注册的中断处理程序来作出应答。

中断开始执行后，通知硬件，拷贝最新的网络数据包到内存，读取网卡更多的数据包。内核需要快速拷贝，因为网卡上接收网络数据包的缓存大小是固定的。相比系统内存要小很多，拷贝动作延迟的话，必定会造成缓存溢出，后续的网络包只能丢弃。当网络数据包拷贝到系统内存后，中断的任务算是完成了，这时它将控制权交换给之前被中断的程序。而操作数据包的其他操作会放在下半部中执行。
```

### 7.4 注册中断处理程序

```markdown
每一个设备都有相关的驱动程序，如果设备使用中断，它的驱动程序就要注册一个中断处理程序。驱动程序是通过 `request_irq()` 注册的。注册的时候传入 要分配的中断号 和 指向中断处理程序的指针。OS 收到中断，该函数就会被调用。
```

#### 7.4.1 中断处理程序标志

```markdown
`request_irq()` 的第三个参数 flag, 是中断处理程序标志，可以是 0，可以是以下值：

`IRQF_DISABLED` - 内核在处理中断程序本身期间，禁止其他所有中断。
`IRQF_SAMPLE_RANDOM` - 表明这个设备产生的中断对内核熵池有贡献。
`IRQF_TIMER` - 特别为系统定时器的中断处理而准备的。
`IRQF_SHARED` - 表明可以在多个中断处理程序之间共享中断线。

后面还有两个参数，第四个参数 `name` 是与中断相关的设备的名字，第五个参数 `dev` 提供唯一的标志信息，以便从共享中断线的诸多中断处理程序中删除指定的那一个。这个函数可能会睡眠，内部会调用 `kmalloc()` 请求分配内存。就是这里堵塞的。
```

#### 7.4.2 一个中断例子

```markdown
例子略。

有一点很重要，初始化硬件 和 注册中断处理程序 的顺序必须正确，防止中断处理程序在设备初始化完成之前就开始执行。
```

#### 7.4.3 释放中断处理程序

```markdown
卸载驱动程序之后需要注销相应的中断处理程序，释放中断线。调用 `void free_irq(unsigned int irq, void *dev)`。如果指定的中断线并不是共享的，函数删除处理程序时会同时禁用这条中断线。如果中断线是共享的，则仅删除 dev 所对应的处理程序。
```

### 7.5 编写中断处理程序

略

### 7.6 中断上下文

```markdown
进程上下文：
是一种内核所处的操作模式，此时内核代表进程执行。例如，执行系统调用。因为进程是以进程上下文的形式连接到内核中的，因此进程上下文可以睡眠，也可以调用调度程序。

中断上下文：
当执行一个中断处理程序时，内核处于中断上下文。因为没有后备进程，中断上下文不可以睡眠，否则又怎能再对它重新调度？因此不能从中断上下文中调用某些函数(可以睡眠的函数)。?
```

```markdown
曾经，中断处理程序共享所中断的进程的内核栈，内核栈的大小是两页，在 32bit 上是 8KB, 在 64bit 上是 16KB。中断处理程序在获取空间时是非常节约的。

另外除了节省使用空间，由于中断处理程序打断了其他的进程，因此要十分快速地执行完才可以。
```

### 7.7 中断处理机制的实现

```markdown
硬件产生一个中断 --> 电信号 --> 中断控制器 --> 处理器(立即停止当前正在做的事情) --> 跳到内存中预定义的位置执行中断处理程序 --> 中断处理程序执行完以后再执行被中断的那个进程。

后面是一些具体系统调用的介绍，不记录了。
```

### 7.8 proc/interrupts

```markdown
略
```

### 7.9 中断控制

```markdown
Linux 内核提供了一组接口用于操作机器上的中断状态。使用这些接口，我们可以禁止当前处理器的中断系统，或屏蔽掉整个机器的一条中断线的能力。

一般来说，控制中断系统的原因归根结底是需要提供同步。通过禁止中断，可以确保某个中断处理程序不会抢占当前的代码。也就是说，禁止中断可以禁止内核抢占。但是禁止中断并没有提供任何保护机制来防止来自其它处理器的并发访问。

Linux 支持多处理器，因此内核代码一般都需要获取某种锁，防止来自其它处理器对共享数据的并发访问。而禁止中断提供保护机制，则是防止来自其它中断处理程序的并发访问。
```

### 7.10 小结

```markdown
大多数现代硬件都是通过中断与操作系统进行通信。管理硬件的驱动程序 注册 中断处理程序，以此来响应硬件发出的中断。

中断过程所做的工作包括了：1. 应答并重新设置硬件 2. 从设备拷贝数据到内存 && 从内存拷贝数据到设备 3. 处理硬件请求 4. 发送新的硬件请求。

内核提供的接口包括了：1. 注册和注销中断处理程序 2. 禁止中断 3. 屏蔽中断线 4. 检查中断系统状态。

因为中断打断了其它代码的执行，它们必须赶快执行完。它们必须在大量的工作与快速执行之间求得一种平衡。
```





































































































































































































































































































































