# chapter 18 使用asyncio包来处理并发

##### 并发是指一次处理多件事，并行是指一次做多件事
##### 真正的并行需要多个核心，现代的笔记本电脑有四个CPU核心，但是通常不经意之间就有超过100个进程在同时运行
##### 因此实际上大多数过程都是并发处理的，而不是并行处理，计算机始终运行着100多个进程，确保每个进程都有机会取得进展，不过cpu本身同时做的事情就只有四件。

### 我能说我并看不大懂这一章的东西 放着吧 不想看了

## 18.1 线程和协程对比
> 1. Python并没有提供终止线程的API
> 2. 使用asyncio库