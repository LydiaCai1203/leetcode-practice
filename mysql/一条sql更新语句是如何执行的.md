# 第二讲：一条SQL更新语句是如何执行的

[TOC]

    MySQL可以直接恢复到半个月内的任意一秒内的数据；更新流程还涉及到两个重要的日志模块，redo log(重做日志)和bin log(归档日志)。

## 重要的日志模块 redo log

    为了避免每一次更新都将数据写到磁盘里面，磁盘首先需要找到那条记录，然后还要更新
### WAL(Write-Ahead Logging)
    先写日志，再写磁盘。当有一条记录需要更新的时候，InnoDB引擎会先把记录写到redo log里面，并且更新内存，这时候更新就算完成了。然后在适当的时候，将这个记录更新到磁盘里面。这个动作往往是在系统比较空闲的时候做。

    InnoDB的redo log也是固定的，比如可以配置一组为四个文件，一个文件有1G，一组文件就是4G大小。redo log就从头开始写，然后写到末尾，写完了又从头开始写。
![1](https://github.com/LydiaCai1203/leetcode-practice/blob/master/statics/mysql%E9%80%BB%E8%BE%91%E6%9E%B6%E6%9E%84%E5%9B%BE.jpg)

## 重要的日志模块 bin log

## 两阶段提交

## 小结