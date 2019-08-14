# 第二讲：一条SQL更新语句是如何执行的 
- [重要的日志模块 redo log](#重要的日志模块-redo-log)
    - [WAL(Write-Ahead Logging)](#WAL(Write-Ahead-Logging))
    - [redo log 结构分析](#redo-log-结构分析)
        - [write pos](#write-pos)
        - [checkpoint](#checkpoint)
- [重要的日志模块 bin log](#重要的日志模块-bin-log)  
- [redo log和bin log的三点不同](#redo-log和bin-log的三点不同)
- [一条更新语句在MySQL里面是怎么进行的](#一条更新语句在MySQL里面是怎么进行的)
- [两阶段提交](#两阶段提交)
- [小结](#小结)
-----------------------
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

    最开始的时候MySQLl里面并没有InnoDB引擎，它自带的引擎是MyISAM, 但是MyISAM没有crash-safe的能力。bin log只能用于归档。所以在引入InnoDB的时候也使用了redo log，来实现crash-safe的能力。

## redo log和bin log的三点不同
+ redo log 是 InnoDB特有的；bin log是Server层面实现的，所有的存储引擎都可以使用。
+ redo log 是 物理日志(记录的是在什么数据页上做了什么修改)；bin log是逻辑日志(记录的是语句的原始逻辑，比如修改了ID=ID+1)
+ redo log 是 循环写的，空间固定，会用完的。bin log是追加写入的，就是说，bin log写到一定文件大小的时候会切换到下一个，并不会覆盖以前的日志。bin log其实就是之前说的，MySQL可以恢复到半年以内任意一个时刻的状态

## 一条更新语句在MySQL里面是怎么进行的
```MySQL
update T set c=c+1 where id=2;
```
+ 1. 执行器会调用存储引擎的接口来检索id=2的行数据
+ 2. 存储引擎会检索id=2这一行，看是否在内存中，如果在内存中，就直接返回数据页；否则 set data from dist to memory, 然后在返回数据页
+ 3. 执行器拿到行数据以后，会对其进行c=c+1的操作
+ 4. 调用存储引擎接口，将更新后的行数据写入内存
+ *5. 于此同时更新的动作会写入redo log中 然后redo log处于prepare的状态，告诉存储引擎现在可以提交事务
+ 6. 执行器会生成这个操作的bin log，并把bin log写入磁盘当中
+ *7. 执行器会调用存储引擎的事务提交接口，引擎则会把刚刚redo log里的状态改成commit, 更新完成

## 两阶段提交
    是为了让两个日志之间保持逻辑一致。保持一致的原因是为了当发生crash-safe的时候，保持数据一致。
## 小结
+ innodb_flush_log_at_trx_commit=1的时候，每次事务的redo log都会持久化到磁盘，这样MySQL异常重启以后不会丢失数据。
+ sync_binlog=1的时候，每次事务的bin log都会持久化到磁盘。
+ Binlog有两种模式，statement 格式的话是记sql语句， row格式会记录行的内容，记两条，更新前和更新后都有。