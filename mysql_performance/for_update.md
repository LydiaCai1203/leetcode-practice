# MySQL 基础 - InnoDB 并发控制

### 1. MySQL 中的事务

```markdown
避免使用长事务，包含 DML 语句多的工作单元，事务太长会导致一些错误。可能事务数据包大小超过参数 max_allowed_packet 设置会导致程序报错，也可能有事务中某个 SQL 对应数据报错，导致整个服务调用失败。
```

### 2. 事务 ACID 特征

```markdown
1. 原子性：事务开始后所有 DML 操作，要么全部成功，要么全部失败，通过 UndoLog 来实现。
2. 一致性：事务开始前和结束后，数据库的完整性约束没有被破坏。
3. 隔离性：同一时刻，只允许一个事务请求同一数据，不同事务之间彼此没有任何干扰，通过锁机制来实现。
4. 持久性：事务提交后，事务对数据库的所有更新都将被保存到数据库，不能回滚，通过 RedoLog 实现。
```

### 3. 事务的并发问题

```markdown
1. 脏读：事务 A 读取了事务 B 未提交的数据。
2. 不可重复读：事务 A 过程中读两次记录可能读到不同的结果。
3. 幻读：一个事务在读取某个范围内的记录时，另一个事务又在该范围内插入新记录，再次读取会出现换行。

不可重复读侧重于 update 操作，幻读侧重于 insert 或 delete。解决不可重复读的问题只需要锁住满足条件的行，解决幻读则需要锁表。
```

### 4. 事务隔离级别

```markdown
read uncommited
read commited
repeatable read
serializable
```

### 5. MVCC 特性

```markdown
MVCC(Multi-Version Concurrency Control)，意为多版本并发控制，作用是让事务在并行发生时，在一定隔离级别前提下，可以保证在某个事务中能实现一致性读，通俗说就是通过 MVCC 来保存数据的历史版本，根据比较版本号来处理数据是否显示，从而达到读取数据时不需要加锁就可以保证事务隔离性的效果。
```

### 6. MVCC 读操作(snapshot read) 、当前读(current read)

```markdown
快照读 - 不加锁：
example:
select * from table where id = ?

当前读 - 加锁：
exmaple:
select * from table where id = ? lock in share mode
select * from table where id = ? for update
insert into table values(...)
update table set ? where id = ?
delete from table where id = ?
```

### 7. MVCC 快照

```markdown
MVCC 内部使用的一致性读快照称为 Read View，在不同的隔离级别下，事务启动时 或者 SQL 开始时，看到的数据快照版本可能也不同，在 RR、RC 隔离级别下会用到 Read View。

在 InnoDB 中每个事务有一个唯一的事务 ID，称为 TransactionID，它是事务开始的时候向 InnoDB 的事务系统申请的，是按申请顺序严格递增的。每行数据都有多个版本，每次事务更新数据时，都会生成一个新的数据版本 Read View，标记为 row_trx_id。并且把 Transaction ID 赋值给这个数据版本的事务 ID。
```

#### 7.1 InnoDB 行格式

变长字段长度列表、NULL 标志位、记录头信息、事务 ID、回滚指针、列1数据、列2数据...

其中回滚指针指向上一个版本数据在 undo log 里的位置指针。

#### 7.2 隔离级别 和 read view

**Read Uncommited**

```markdown
不会获取 read view 副本
```

**Read Repeatable**

```markdown
设置事务隔离级别：`set session transaction isolation level repeatable read;`

在 RR 下，快照 不是事务发起时创建的，而是在第一个 SELECT 发起后创建的。也就是说，假如事务 A 和 事务 B 同时 `start transaction`, 事务 B 一直没有任何动作，事务 A 修改了 ID = 1001 数据，然后 commit 了。此时事务 B 读取 id=1001 的数据，发现读取的数据是 A 修改
```

**Read Commited 与 快照**

```markdown
在 RC 下，快照 每次 SELECT 后都会生成最新的 Read View，即每次 SELECT 都能读取到已经 COMMIT 的数据。就会存在不可重复读和幻读的现象。
```

### 7.4 Undo 回滚段

查看 undo 情况：`show engine innodb status \G`

```markdown
保证事务进行 rollback 时的原子性和一致性，当事务进行回滚时可以用 undo log 的数据进行恢复。用于 MVCC 快照读的数据，通过读取 undo log 的历史版本数据可以实现不同事务版本号有拥有自己的独立的快照数据版本。同时 Undo Log 是循环覆盖使用的。

过程：
1. 开启一个事务 A，对 user_info 表执行更新动作, `update user_info set name='李四' where id = 1;`
2. 获得事务编号 104
3. 把 user_info 表修改前的数据拷贝到 undo log
4. 修改 user_info 表中 id = 1 的数据
5. 把修改后的数据事务版本改成 104, 并把 db_roll_ptr 地址指向 undo log 数据地址
```

![](/Users/caiqingjing/project/private/leetcode-practice/statics/undo_log.jpg)

![](/Users/caiqingjing/project/private/leetcode-practice/statics/undo_log2.jpg)

#### 7.5 回滚记录

```markdown
insert 的反向操作是 delete，undo 里记录的就是 delete 相关信息
update 的反向操作是 update，undo 里记录的是 update 前的相关信息
delete 的反向操作是 insert，undo 里记录的是 insert values 相关的记录

tips:
不建议物理 delete 删除数据，会产生大量的 Undo Log，Undo 快被写满就会发生切换，在次期间会有大量的 IO 操作，导致业务的 DML 都会变得很慢。
```

#### 7.6  Read View

```markdown
在每个 SQL 语句执行前都会得到一个 Read View, 副本主要保存了当前数据库系统中正处于活跃(还未 commit) 的事务的 ID 号。

几个重要属性：
1. trx_ids: 当前系统活跃(未提交)事务版本号的集合。
2. low_limit_id：创建当前 read view 时当前的系统最大事务版本号+1
3. up_limit_id: 创建当前 read view 时系统正处于活跃的最小事务版本号
4. creator_trx_id: 创建当前 read view 的事务版本号
```

#### 7.7 Read View 匹配条件

```markdown
1）如果某数据的 事务 ID < up_limit_id 则显示
如果数据事务 ID 小于 read view 中的最小活跃事务 ID，则可以肯定该数据是在当前事务启动之前就已经存在了的。

2）如果某数据的 事务 ID >= low_limit_id 则不显示
如果数据事务 ID 大于 read view 中的最大事务 ID，则说明该数据是在当前 read view 创建之后才产生的，所以数据不予显示。

3）up_limit_id < 某数据的 事务ID < low_limit_id 则去 trx_ids 中进行匹配
如果数据的事务 ID 大于最小的活跃事务 ID，且小于等于系统最大的事务 ID，说明该条数据可能在当前事务开始的时候还未提交的。
    a. 如果事务 ID 不存在于 trx_idx 集合，则说明在 read_view 产生的时候已经 commit 了。
    b. 如果事务 ID 存在于 trx_idx，说明在 read_view 产生时该事务还未提交，如果数据的事务 ID 等于 creator_trx_id，说明这个数据是自己生成的，所以可以显示。
    c. 如果事务 ID 存在于 trx_idx，说明在 read_view 产生时该事务还未提交，如果数据的事务 ID 不等于 creator_trx_id，则不可以显示。
    
4）当不满足 read view 显示条件的时候，从 undo log 里面获取数据的历史版本，拿到历史的事务版本号，再从 1）步骤开始匹配，直到找到一条满足条件的历史数据进行显示，找不到则返回空结果。
```

### 8. 快照读 和 当前读

```markdown
快照读：
快照读是指读取数据时不是读取最新版本的数据，而是基于历史版本读取的一个快照信息，快照读可以使普通的 select 读取数据不用对表数据加锁，解决了因为对数据加锁导致的读写不能同时进行的问题。

当前读：

```


