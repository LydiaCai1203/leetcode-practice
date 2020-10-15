# MySQL 基础：LOCKING READS

​		如果你要在同一个事务里面先查数据，再进行插入或者更新数据的动作，其它事务依旧是可以更新或删除你查询的那几行数据。也就是说 `select * from table; ` 这句是快照读，也就是不会加锁。

## 1.1 SELECT ... FOR SHARE

​		给任何你需要读取的行上一个共享锁。在你的事务 commit 之前，其它事务对上锁的行只能读，不能修改。如果有另一个尚未 commit 的事务对这些行进行了修改，你的查询则需要等待这些事务结束，然后你使用最新的数据值。

​		SELECT ... FOR SHARE  等价于 SELECT ... LOCK IN SHARE MODE

​		文档里说到至少应该有 `SELECT` 和 `DELETE` 、`UPDATE`、`l`

​		

​		