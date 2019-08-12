# 第二讲：一条SQL更新语句是如何执行的

[TOC]

    MySQL可以直接恢复到半个月内的任意一秒内的数据；更新流程还涉及到两个重要的日志模块，redo log(重做日志)和bin log(归档日志)。

## 重要的日志模块 redo log 
+ **引擎层面的日志**

    为了避免每一次更新都将数据写到磁盘里面。减少磁盘I/O次数。因为redo log, 是的MySQL发生异常重启，之前提交的数据也不会丢失，这个能力成为crash-safe.

### WAL(Write-Ahead Logging)
    先写日志，再写磁盘。当有一条记录需要更新的时候，InnoDB引擎会先把记录写到redo log里面，并且更新内存，这时候更新就算完成了。然后在适当的时候，将这个记录更新到磁盘里面。这个动作往往是在系统比较空闲的时候做。

    InnoDB的redo log也是固定的，比如可以配置一组为四个文件，一个文件有1G，一组文件就是4G大小。redo log就从头开始写，然后写到末尾，写完了又从头开始写。

### redo log 结构分析
![1](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/redo_log%E7%A4%BA%E6%84%8F%E5%9B%BE.jpg)

#### write pos
    当前记录的位置，一边写一边后移，写到第三号文件的末尾就相当于写到了第零号文件的首部。

#### checkpoint    
    checkpoint是需要擦除的部分，也是往后移动并且循环的，擦除记录之前要先把记录更新到数据文件。

## 重要的日志模块 bin log
+ **Server层面的日志**

    

### 

## 两阶段提交

## 小结