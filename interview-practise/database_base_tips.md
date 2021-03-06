## REVIEW OF DATABASE

------------------
### 1. ★★☆ 范式理论。
    1. 属性（字段）是最小的单位不可以再分。
    2. 在满足第一范式的前提下，每个非主属性都完全依赖于主键。
    3. 在满足第二范式的前提下，每个非主属性都不依赖于其它的非主属性。
    4. 在满足第三范式的前提下，属性之间不能有非平凡且非函数依赖的多值依赖。

------------------
### 2. 数据库的事务
    1. 事务是 是访问和更新数据库的程序执行单元 是用户定义的一个数据库操作的原子序列，要么全做，要么全都不做 事务一旦提交了，它对数据库的改变就是永久性的，接下来的其它操作或者故障不应该对其有任何的影响。
    2. 事务的四大特性：原子性、隔离性、一致性、持续性
    3. MyISAM是不支持事务的，InnoDB是支持事务的

------------------
### 3. ★★★ 四大隔离级别，以及不可重复读和幻影读的出现原因
+ 并发情况下 写操作可能对读操作引发的问题
    + **脏读**：当前事务A可以读到事务B没有提交的数据。(事务提交前)
    + **不可重复读**：事务A在读取数据的时候，第一次读取得到的数据和第二次读取得到的数据都不一样。(事务提交以后)
    + **幻读**：在事务A中按照某个条件两次查询数据库，两次查询的结果条数都不一样。(不可重读是数据变了，但是幻读是数据的行数变了)
+ 事务的隔离级别（级别越高，开销越高，可支持的并发越低）
    + **读未提交** 可以读到别的事务未提交的(脏读)
    + **读已提交** 只能看见已经提交了的事务所做出的改变，脏读(no way)  不可重读(probably) 幻读(probably)
    + **可重复读** MySQL默认的隔离级别，确保多个数据库实例在并发读取数据的时候，可以看到同样的数据行。脏读(no way) 不可重复读(no way) 幻读(probably)
    + **可串行化** 通过强制事务排序，使之不可能互相发生冲突，就是说会在每个读的数据行上加上共享锁。这样做会导致大量的超时现象和锁竞争现象。脏读(no way) 不可重复读(no way) 幻读(no way)

------------------
### 4. MySQL InnoDB 有哪些索引类型？
    1. 聚簇索引(主键索引、唯一索引)
    2. 辅助索引(单列索引、联合索引、前缀索引)
    3. 其它索引(全文索引、空间索引)

------------------
### 4. 数据库索引的实现有哪些数据结构
    1. 索引是帮助MySQL高效获取数据的数据结构。
    2. 常见的索引有两种结构：Hash索引和B+Tree索引，如果我们使用的是InnoDB,默认的是B+Tree（这里有可能会问一些和存储引擎相关的问题）

------------------
### 5. 你知道为什么采用B+Tree吗？和Hash索引比较起来有什么优缺点吗
    1. Hash索引的底层是哈希表，哈希表是一种以key-value存储数据的结构，所以多个数据在存储关系上是完全没有任何的顺序关系的。对于区间查询是无法直接通过索引查询的，就需要进行全表扫描。所以哈希索引只适用于等值查询的场景。
    2. B+Tree是一种多路平衡查找树，所以他的节点是天然有序的，左子节点小于父节点，父节点小于右子节点，对于范围查询的时候不需要做全表扫描。
    3. Hash索引没有办法利用索引完成排序, 因为hash索引里面的key都是经过计算后的值。
    4. Hash索引不支持多列联合索引的最左匹配排序。也就是说，联合索引，要么都用，要么就都不用。
    5. 如果有大量重复键值的情况下，Hash索引的效率会很低，因为存在Hash碰撞的问题。

-----------------
### 6. ★★★ 索引的缺点是什么
    1. 创建索引和维护索引要耗费时间，这种时间随着数据量的增加而增加。
    2. 索引需要占用物理空间，除了数据表占用数据空间以外，每一个索引都要占据一定的物理空间，
    3. 对表中的数据进行增加、删除和修改的时候，索引也需要动态维护。

+ 什么情况下不建议建立索引

        第一种情况：表记录比较少的时候 记录不超过2000的时候可以不建立索引。
        第二种情况：索引的选择性较低 就是说重复的值比较多的时候 并不建议建立索引
```MySQL
    SELECT count(DISTINCT(title))/count(*) AS Selectivity 
    FROM employees.titles;
```
    上面这条语句可以查看索引的选择性大小，如果不足0.0001的话就没有必要建立索引了。

-----------------
### 7. 说一下redis和MongoDB的区别
    1. 性能
        Redis的性能要优于MongoDB 
    2. 存储的数据结构
        Redis的数据结构有Set、String、List、Dict、等多种数据结构。MongoDB里面每个collections都是由一个个dict组成的。
    3. 存储空间
        MongoDB所有的数据实际上都是放在硬盘上面的，所有操作的数据都是映射到内存上，然后再进行操作的。
        Redis所有的数据都是放在内存上的，如果断电的话，数据就会消失，所以需要做数据持久化。
        MySQL所有的数据都是放在硬盘上面的，要使用的时候才会交换到内存，能够处理远超过内存总量的数据。
    4. 还有可说的，暂时不写 因为说出什么就是引导面试官往什么方向上去问。

-----------------
### 8. redis为什么没有索引？
    这道题我的回答不好 首先是因为上一道在Redis 和 MongoDB的区别里面，我说了Redis是没有索引的，但是MongoDB里面有。Redis没有索引我说的也是，因为建立索引的目的是为了达到更高效的搜索，Redis本身的数据就是存在内存里面的，所以没有必要建索引了。但是我总觉得面试官是希望我从建立索引的结构层面来解释。所以下一步我要开始全面复习MySQL了。ß

-----------------
### 9. ★★★说一下乐观锁和悲观锁的区别
    乐观锁：
        在关系型数据库里面，乐观并发控制是一种并发控制的方法，它假设用户并发的事务在处理的时候不会相互影响，各事务能够在不产生锁的情况下处理各自影响的那部分数据。在提交数据更新之前，每个事务都会检查在该事务读取数据以后，有没有其它事务又修改了该数据。如果其它事务有对数据进行更新的话，正在提交的事务就会进行回滚。适合用于度多写少的情况。
    悲观锁：
        在关系型数据库里面 ，悲观并发控制是一种并发控制的方法。它可以阻止一个事务以影响其它用户的方式修改数据，如果一个事务执行的操作读某行数据应用了锁，只有当这个事务把锁释放，其它的事务才能修改数据。

-----------------
### 10. ★★★ B+Tree 原理，与其它查找树的比较
[看这篇](https://mp.weixin.qq.com/s/faOaXRQM8p0kwseSHaMCbg)

```markdown
1. 首先索引里面存的指针存的是数据库里面数据的物理地址 索引里面还有一个索引键值
2. 真实世界的索引并没有使用二叉树或者是红黑树的实现 大部分都是B-Tree或者是B+Tree的实现
```
#### 10.1 B-Tree
```markdown
1. 平衡多叉树，所有的叶子节点都在同一层(注意这里和平衡树的定义还是有点不同的)。
2. 每个节点都存储着一行所有的数据，因此一页存储区域存储的数据会少，树高会变高。树高变大就意味着磁盘 I/O 的次数会变多。
3. 叶子节点之间不存在指针指向，因此对范围查找很不友好。
```

#### 10.2 B+Tree
```markdown
1. 平衡多叉树，所有的叶子节点都在同一层(注意这里和平衡树的定义还是有点不同的)。
1. 非叶子节点都只有key, 没有data。
2. 所有的叶子节点之间都有两个双向指针。
3. 数据记录都存放在叶子节点中。(这里只是针对 InnoDB 是这样的，MyISAM 里存的就是磁盘地址)
```

#### 10.3 评判标准

    一般来说，索引本身也很大，是不可能全部存在内存中的，因此索引往往以索引文件的形式存储在磁盘上面。这样在索引查找的过程中就要产生I/O磁盘消耗，相对于内存的存取，I/O存取的消耗要高几个数量级。所以，评价一个索引的优劣最重要的指标就是在查找过程中磁盘I/O操作次数的渐进复杂度。

+ 主存存取原理

    目前计算计算机使用的主存都是随机读写存储器，主存是一系列的存储单元组成的矩阵，每个存储单元存储固定大小的数据，每个存储单元都有唯一的地址，这里是一个二维地址。主存的存取过程如下：当系统需要读取主存的时候，会将地址信号放到地址总线上传给主存，主存读到信号以后，解析信号并且定位到指定的存储单元，然后将读到的数据放到地址总线上面，供其它的部件读取。
    <br>
    sum: 所以主存存取的时间消耗，只和存取次数有关系，和要存取的数据之间的距离并没有关系。


+ 磁盘存取原理

    磁盘I/O存在机械运动耗费，所以磁盘I/O的消耗是巨大的，索引一般又是以磁盘文件的形式存储在磁盘上的。
    一个磁盘是以几个同轴且大小相等的圆片组成的，每个磁盘都必须同步转动，在磁盘的一侧有磁头支架，磁头支架固定了一组磁头，每一个磁头都负责存取一个磁盘的内容。磁头是不能转动的，但是可以沿着磁盘的半径方向运动。从正下方看，所有的磁头在每一个时刻都应该必须是重叠的。目前已经有多磁头独立的技术了。

    每一个扇区是磁盘存取的最小单元。当需要进行磁盘读取的时候，系统会将数据逻辑地址传给磁盘，磁盘的控制电路会将逻辑地址变成物理地址，寻找对应的磁道时间叫做寻道时间，寻找对应的扇区的时间叫做旋转时间。
    <br>
    sum: 所以磁盘存取的时间消耗和寻道时间以及旋转时间有关系。


+ 局部性原理和磁盘预读

    磁盘每次读取都会进行预读，即使只需要一个字节，磁盘也会从这个位置开始向后读取一定的长度放入内存。由于磁盘顺序读取的时候效率高，不需要花费寻道时间，只需要花费少量的旋转时间，预读的长度一般为页的整数倍。页是计算机管理存储器的逻辑块，页的大小通常是4K，主存和磁盘都是以页为单位进行数据交换的。当要读取的数据不在主存中的时候，会发起一个缺页信号，然后系统就会和磁盘发起读盘信号。磁盘会找到数据起点，然后将之后的一页或者几页，读取出来存进内存里面。


#### 10.4 进入正题 为什么要使用B-Tree/B+Tree来实现索引

    1. 根据B-Tree的定义，检索一次至多会访问h个节点，数据库的设计者将一个节点设置为磁盘中的一个页，这样每个节点需要一次I/O就可以完全载入。所以每次在新建一个节点的时候，就会直接申请一个页的空间。由于根节点常驻内存，所以在B-Tree中检索一次最多需要h-1次I/O.
    
    2. 红黑树的深度要深，且逻辑上很近的父子节点物理上可能隔很远，无法利用局部性。红黑树的效率要差很多。
    
    3. B+Tree因为去掉了内节点的data部分，因此可以拥有更大的出度，所以B+Tree其实更加适合外存索引。

*所有的非聚集索引实际上都可以被称为辅助索引。非聚集索引的叶子节点实际上放的不是行的地址，而是主键键值。这样就能通过主键键值去找到相应的数据行*
*覆盖索引就是把索引对应那列的值存在索引里面，这样直接找到索引就能渠道相应列的值*

-----------------
### 12. ★★★ InnoDB 与 MyISAM 比较

+ MyISAM(B+Tree)
```markdown
1. MyISAM 中没有聚簇索引的概念，认为 主键索引 和 辅助索引 的结构是一样的。
1. MyISAM 中索引文件和数据文件是分开存储的，因此 主键索引 和 辅助索引 的叶子节点中存的 data 都是磁盘地址。
2. 主键索引要求 key 是唯一的且非空，辅助索引是可重复可空的。
```

+ InnoDB(B+Tree)
```markdown
1. InnoDB 的数据文件本身就是索引文件, 因此主键索引（聚簇索引）的叶子节点中保存的是完整的数据记录。
2. InnoDB 的辅助索引叶子节点的 data 中保存的是主键值。
3. 因为InnoDB的数据文件本身是按照主键聚集，所以会要求InnoDB表必须有主键，如果不存在这种列，MySQL会自动生成一个隐含的字段作为主键。这个字段的长度为6个字节。类型是长整型的。
```

#### 12.1 为什么不建议主键过长
```markdown
1. 因为所有的辅助索引都引用主索引，使用辅助索引搜索的时候会通过辅助索引找到主键，然后再通过主键索引找到数据。所以过长的主索引，会让辅助索引也变得很大。
2. 同样节点过大也会导致一页存储的节点个数变少，树高就变大，IO 次数也会变多吧。
```

#### 12.2 使用非单调的字段作为主键在InnoDB表中 并不是一个好的做法
```markdown
因为InnoDB的数据文件就是索引文件，底层实现是B+Tree。非单调的字段在插入的时候会导致树不断旋转分裂调整。十分低效，所以用自增字段作为主键是一个很好的选择。
```

-----------------
### 13. ★★★ MySQL 索引以及优化

+ 联合索引
    MySQL中的索引可以以一定的顺序引用多列，这样的索引就叫做联合索引。一般来说，一个联合索引就是一个有序元组，其中各个元素均为表中的一列。
+ index(emp_no, title, from_date)

#### 13.1 全列匹配
```MySQL
    EXPLAIN SELECT * 
            FROM employees.titles 
            WHERE emp_no='10001' AND title='Senior Engineer' AND from_date='1986-06-26';

    EXPLAIN SELECT * 
            FROM employees.titles 
            WHERE from_date='1986-06-26' AND emp_no='10001' AND title='Senior Engineer';
```
    emp_no是主键。MySQL的查询优化器会自动调整where子句的条件顺序以使用适合的索引，所以上面的两条语句效果是一样的。

#### 13.2 最左前缀匹配
[知乎一个例子 说的挺好的](https://www.zhihu.com/question/36996520)

注意：mysql5.6里，如果where cid=1是不会走索引的，但是mysql5.7里面是会走索引的。这个要看下面的例子才会理解。

    在mysql建立联合索引时会遵循最左前缀匹配的原则，即最左优先，在检索数据时从联合索引的最左边开始匹配.
    MySQL在创建联合索引的时候，会从左到右对字段进行排序，如果(name, cid)两个字段为一个联合索引，就会先对name进行排序，再对cid进行排序。显然cid的值就不可能做到有序。通常情况下直接使用第二个字段查询，是用不到索引的。在B+Tree里面，什么时候用cid才会使用到索引呢？就是cid有序的时候，cid什么时候会有序，就是name等值的情况下。

#### 13.3 查询条件用到了索引中列的精确匹配，但是中间某个条件未提供
```MySQL
    EXPLAIN SELECT * 
            FROM employees.titles _
            WHERE emp_no='10001' AND from_date='1986-06-26';
```
    只使用到了索引的第一列(emp_no)。from_date字段不符合最左前缀匹配。如果也想让from_date使用索引的话，不应该使用where子句进行过滤，而应该使用辅助索引。
```MySQL
    EXPLAIN SELECT * FROM employees.titles
            WHERE emp_no='10001'
                AND title IN ('Senior Engineer', 'Staff', 'Engineer', 'Senior Staff', 'Assistant Engineer', 'Technique Leader', 'Manager')
                AND from_date='1986-06-26';
```

#### 13.4 查询条件没有指定索引第一列
```MySQL
    EXPLAIN SELECT * 
            FROM employees.titles 
            WHERE from_date='1986-06-26';
```
    不是最左前缀，from_date是复合索引的一部分，没有问题，可以进行index类型的索引扫描方式。explain显示结果使用到了索引，是index类型的方式。

#### 13.5 匹配某列的前缀字符串
```MySQL
    EXPLAIN SELECT * 
            FROM employees.titles 
            WHERE emp_no='10001' AND title LIKE 'Senior%';
```
    此时可以用到索引，如果通配符不出现在开头的话就可以用到。

#### 13.6 范围查询
```MySQL
    EXPLAIN SELECT * 
        FROM employees.titles 
        WHERE emp_no < '10010' and title='Senior Engineer';
```
    范围列在符合最左前缀原则的前提下还是可以用到索引的，但是范围列后面的列无法用到索引。索引最多用于一个范围列，所以如果条件中有两个范围列，则无法用到索引。“between”并不意味着就是范围查询。

#### 13.7 查询条件中含有函数或表达式
```MySQL
    EXPLAIN SELECT * 
            FROM employees.titles 
            WHERE emp_no='10001' AND left(title, 6)='Senior';
```
    但是由于使用了函数left，则无法为title列应用索引， 

#### 13.8 前缀索引
    有一种与索引选择性有关的索引优化策略叫做前缀索引，就是用列的前缀代替整个列作为索引key，当前缀长度合适时，可以做到既使得前缀索引的选择性接近全列索引，同时因为索引key变短而减少了索引文件的大小和维护开销。下面以employees.employees表为例介绍前缀索引的选择和使用

```MySQL
    SELECT count(DISTINCT(concat(first_name, left(last_name, 3))))/count(*) AS Selectivity FROM employees.employees;
```
    前缀索引兼顾索引大小和查询速度，但是其缺点是不能用于ORDER BY和GROUP BY操作，也不能用于Covering index（即当索引本身包含查询所需全部数据时，不再访问数据文件本身）。

#### 13.9 使用InnoDB的时候，务必使用一个与业务无关的键作为主键。
    由于InnoDB使用的是聚集索引，所有的数据都是存放在叶子节点中的。这就要求同一个叶子节点中的内的各条数据记录的主键顺序有效。因此每当插入一条数据的时候，就会在当前索引节点的后续插入。当一页写满了以后，就会开辟新的一页。每次插入的时候也不需要移动位置，效率就高。如果不是单调有序的列的话，此时MySQL不得不为了将新记录插到合适位置而移动数据，甚至目标页面可能已经被回写到磁盘上而从缓存中清掉，此时又要从磁盘上读回来，这增加了很多开销，同时频繁的移动、分页操作造成了大量的碎片，得到了不够紧凑的索引结构，后续不得不通过OPTIMIZE TABLE来重建表并优化填充页面。

-----------------
### 14. ★★★ ACID 的作用以及实现原理

[先看这个](https://www.cnblogs.com/kismetv/p/10331633.html)

[实际应用中看这个](https://liuyueyi.github.io/hexblog/2018/03/23/mysql%E4%B9%8B%E9%94%81%E4%B8%8E%E4%BA%8B%E5%8A%A1%E8%AF%A6%E8%A7%A3/)

#### 15.1 MySQL结构
    1. 第一层：处理客户端的连接，授权验证等等。
    2. 第二层：服务器层，负责查询语句的解析，优化，缓存，内置函数的实现，存储过程等等。
    3. 第三层：存储引擎，负责MySQL中数据的存储与提取。

<br/>

#### Atom（原子性）实现原理：undo log
    InnoDB提供了两种事务日志，分别是redo log(重做日志) 和 undo log(回滚日志)。redo log用于保持事务的持久性。undo log是事务原子性和隔离性实现的基础。
    
    当事务对数据库进行修改时，InnoDB会生成undo log,如果事务执行失败或者调用了rollback,导致事务要发生回滚的时候，就会利用undo log将数据变成修改前的样子。
    
    undo log 属于逻辑日志，记录的是sql执行的相关信息，发生回滚的时候，会根据undo log里面的内容做相反的动作。

<br/>

#### Constancy(持久性) 实现原理：redo log
    数据存放在磁盘中，InnoDB提供了缓存，缓存中包含了磁盘中部分数据页的映射，从数据库中读取数据的时候，会先从缓存里面读取，如果缓存里面也没有，就会从磁盘读取，然后放入缓存。当向数据库中写入数据的时候，会先写入缓存， 缓存中的数据会定期刷新到磁盘中。

**但是缓存也带了新的问题：** 如果MySQL出现宕机，此时在buffer中修改的数据还没有被刷新到磁盘当中，就会出现数据丢失的问题。那么事务的持久性也就无从保证了。

    有了redo log以后，所有的修改都会现在redo log里面中记录，当事务提交的时候，会进行事务刷盘，也就是将buffer对应的脏数据页写到磁盘里面。如果MySQL出现宕机，读取redo log里的信息对数据库进行恢复。

**另外刷脏是以页为单位的，但是redo log只会对要修改的数据进行修改，可以减少无效的I/O**

<br/>

#### Isolated(隔离性) 实现原理：
 
    事务内部的操作和其它的事务之间是相互隔离的，也就是并发执行的事务之间不能相互打扰。

+ 一个事务的写操作对另一个事务的写操作的影响：**锁机制保证隔离性**

        事务在修改数据的时候，需要获得相应的锁，在事务操作期间，这部分数据是锁定的，其它的事务如果需要修改数据，需要等待事务提交以后，或者 回滚以后 释放了锁。
    
        性能：表锁 < 行锁  # 表锁的并发性能差

+ 一个事务写操作对另一个事务读操作的影响：**MVCC(多版本控制并发协议)保证隔离性**
    + 优点：不加锁，所以读写不冲突，并发性能好。
    + 脏读：pass
    + 不可重复读：pass
    + 幻读：pass

<br/>

#### Constancy(一致性) 实现原理：
    指事务结束以后，数据库的完整性约束没有被破坏，事务执行的前后都是合法的数据状态。数据库的完整性包括但是不限于（主键存在且唯一，列完整性，外键约束，用户自定义完整性(如转账前后用户账户余额之和应该保持不变)）

-----------------
### 15. ★★☆ drop、delete、truncate 比较
+ drop
    + drop语句删除表结构及所有数据，并将表所占用的空间全部释放
    + drop语句将删除表的结构所依赖的约束，触发器，索引，依赖于该表的存储过程/函数将保留,但是变为invalid状态
+ delete
    + 执行delete操作时，每次从表中删除一行，并且同时将该行的的删除操作记录在redo和undo表空间中以便进行回滚（rollback）和重做操作
+ truncate
    + 一次性地从表中删除所有的数据并不把单独的删除操作记录记入日志保存，删除行是不能恢复的。并且在删除的过程中不会激活与表有关的删除触发器。执行速度快

-----------------
### 16. ★☆☆ redo、undo、binlog 日志的作用
+ binlog
    + Server层面的日志(任何数据引擎都可以用)，记录了数据在逻辑层面的修改，即ID=ID+1, **主要用于主从备份，数据恢复**。
    + 追加写入，一个文件写完，就开辟一块新的空间。
+ redolog
    + 数据库引擎层面的日志，记录了数据操作在物理层面的修改,即在哪个数据页上做了什么操作。**当数据库异常重启的时候，用来进行数据恢复的**。
    + 两部分组成：内存中的日志缓冲(易失)；磁盘中的日志文件(持久)。
    + force log at commit。
        + 当事务commit的时候，会先把该事务的事务日志从内存刷到磁盘上，进行持久化。
    + 循环写入，只有固定的空间，用完了剩下的空间，就覆盖之前的空间。
+ 为了保证binlog和redolog的一致性，还采用了**两阶段提交**.
+ undo log
    + 数据库引擎层面的日志，记录的是数据修改时候的反向操作。**主要用于事务的回滚，可以根据undolog回溯到过去的某个特定的版本，实现MVCC**
        + 如果是插入数据进数据表，那在undolog中记录的就是删除数据的操作。

-----------------
### 17. ★★★ MVCC(多版本并发控制)原理，当前读以及快照读，Next-Key Locks 解决幻影读
[MVCC原理 && 间隙锁](https://github.com/LydiaCai1203/leetcode-practice/edit/master/mysql_performance/mvcc_next_key.md)

-----------------
### 18. ★★★ MySQL 数据库调优 - 面试套路
+ [数据库调优](https://mp.weixin.qq.com/s/e0CqJG2-PCDgKLjQfh02tw)
+ [Explain 结果中每个字段的含义说明](https://www.jianshu.com/p/8fab76bbf448)

-----------------
### 14. “N叉树”的N值在Mysql是否可以被调整

-----------------
### 15. ★★★ 线程安全问题

-----------------
### 16. ★★☆ 手写 SQL 语句，特别是连接查询与分组查询

-----------------
### 17. ★★☆ 连接查询与子查询的比较

-----------------
### 19. ★★☆ 视图的作用，以及何时能更新视图

-----------------
### 20. ★☆☆ 理解存储过程、触发器等作用

-----------------
### 22. ★★☆ 封锁的类型以及粒度，两段锁协议，隐式和显示锁定

-----------------
### 24. ★★★ SQL 与 NoSQL 的比较

-----------------
### 25. ★★☆ 水平切分与垂直切分

-----------------
### 26. ★★☆ 主从复制原理、作用、实现

-----------------
### 28. ★★★ 与 Memchached 的比较

-----------------
### ★★☆ 字典和跳跃表原理分析 以及 使用场景。
### ★★★ 与 Memchached 的比较。
### ★☆☆ 数据淘汰机制。
### ★★☆ RDB 和 AOF 持久化机制。
### ★★☆ 事件驱动模型。
### ★☆☆ 主从复制原理。
### ★★★ 集群与分布式。
### ★★☆ 事务原理。
