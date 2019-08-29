# MySQL为什么有时候会选错索引

[TOC]
----------------------------
## Example
```mysql
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `a` (`a`),
  KEY `b` (`b`)
) ENGINE=InnoDB；

// 插入10万条数据
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=100000)do
    insert into t values(i, i, i);
    set i=i+1;
  end while;
end;;
delimiter ;
call idata();

// 查询语句
mysql> select * from t where a between 10000 and 20000;
// 这条语句优化器会通过索引a进行查询
```

### 问题
    我们经常会 删除表中的数据 和 插入表中的数据 对应查询时候 是否用错索引导致查询过慢的情况。
```mysql
// 事务A                                                 // 事务B
start transaction with consistent snapshot;
                                                        delete from t;
                                                        call idata();

                                                        explain select * from t where a between 1000 and 2000;
commit;

// 这时候这条select语句就不会走索引了
```

### 优化器的逻辑

#### 扫描行数、是否用临时表、是否会进行排序
+ 扫描行数是怎么判断的
    + 根据”索引的区分度“来预估记录数。
+ 索引的区分度
    + 一个索引上不同的值越多，“索引的区分度”就越高。
    + 基数：就是指一个索引上不同的值的个数是多少。这个值可以在show index中看见，但是这是统计数值，并不是准确的。
+ 基数的抽样采集
    + InnoDB会抽样选择N个数据页，统计这些数据页上面的不同值，然后取平均值。再乘以这个索引所占的数据页数。
    + 这个数值不是一直不变的，当变更的行数达到一定的程度，会自动触发重新做一次抽样采集。
    + innodb_stats_persistent 来设置统计信息是否持久化存储，还可以设置N和M的大小，来判断什么时候进行重新抽样采集。
+ 预估的扫描行数
    + 可以使用show index 来查看table中的rows是多大。

#### example
```mysql
explain select * from t where a between 10000 and 20000;
explain select * from t force index(a) where a between 10000 and 20000;
```

#### 分析
    走索引所要扫描的记录表行数显然要少很多，只有37000多行，但是不走索引的话要进行全表扫描。这是因为索引a并不是聚簇索引，最后还有一个回表的动作。这也是额外的代价，优化器也是要算在里面的。
    而第一条select是直接走的主键索引，这是聚簇索引。优化器会认为走主键索引花费的开销要更加小一点。

#### 避免方法
    所以说出现这种情况的原因还是因为mysql错误预估了扫描行数，这时候使用`analyze table t`以后，再解释一下第一条select语句，发现预估行数对了。

#### 为什么会错误预估扫描行数文章中并没有作出过多的解释。
----------------------------------------------------------------

#### 

#### example
```mysql
// 发现优化器又又又选择错了索引
explain select * from t where (a between 1 and 1000)  and (b between 50000 and 100000) order by b limit 1;
```

#### 分析
    如果使用索引a进行查询，那么就是扫描索引a的前1000个值，最后还要进行一个回表的动作。然后再根据b的值进行扫描.显然要扫描1000行。

    如果使用索引b进行查询，那么就是扫描索引b的最后50001行，最后依然还要进行一个回表的动作。


### 索引选择异常和处理
    大多数情况下，优化器都会选择错索引。你可以采用以下的方法进行解决。

#### 采用force index强行选择一个索引
+ 缺点
    + 1. 语句不优美
    + 2. 索引名字变了还要改sql语句
    + 3. 如果换了别的数据库这个语法还不一定管用

#### 修改语句，引导MySQL使用我们期望它使用的索引
```mysql
explain select * from t where (a between 1 and 1000)  and (b between 50000 and 100000) order by b, a limit 1;
```
+ 选错索引原因再分析
    因为优化器认为选择了索引b可以避免排序，因为在建索引b的时候本身就需要进行排序，所以优化器认为只要遍历就可以了,躲过了排序。
+ 为什么选择了索引a
    现在不管选哪个索引都需要排序，所以只能选择扫描行数最少的那个索引了。
+ 这样修改要注意逻辑
    这条语句中因为有limit，所以这样修改的时候逻辑并没有发生变化。

```mysql
mysql> select * 
       from  (
           select * 
           from t 
           where (a between 1 and 1000)  and (b between 50000 and 100000) order by b limit 100)
        alias limit 1;
```
+ 为什么选择了索引a
    当使用了limit 100 的时候，这里优化器会选择索引a。

#### 建一个更加合适的索引给MySQL使用 or 删除错误的索引


### 思考题
    通过sessionA的配合，让sessionB删除数据以后又重新插入一遍数据，然后就发现explain的结果中，rows的结果从10000 变成了 37000
    但是如果没有sessionA的配合，使用sessionA进行delete、callidata、explain 会发现rows还是正确的结果。这是为什么呢？