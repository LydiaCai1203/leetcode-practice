# MySQL 数据库性能调优

### 1. 排除缓存干扰，定位耗时较长的查询语句

```markdown
MySQL 8.0 之前是存在查询缓存的，如果缓存失效(更新数据清缓存)的话，就可能出现 Response time 变高。执行 SQL 的时候加上 NoCache 去跑，跑出来的就是真实的查询时间。
```

### 2. Explain 查询执行计划

**说知道 explain 就要防止面试官问 - -**

```markdown
1. 首先肯定要知道 Explain 都有哪些字段。重要的记住三个：type, rows, extra。
    a. type: 显示查询使用了何种类型
        + const: 最多只有一行记录匹配(唯一索引扫描)
        + eq_ref: 多表 join 时，对于前面表的每一行，在当前表中也只能找到一行。使用的也是唯一索引。
        + ref: 多表 join 时，对于前面表的每一行，在当前表中能找到多行。
        + range: 索引范围查询(<,>,in,like,between等)
        + index: 索引全表扫描，把索引从头到尾都扫了一遍
        + all: 全表扫描性能最差
    
    b. rows: MySQL 估算的需要扫描的行数（因为是抽样统计）这个值可以非常直观地显示 SQL 的效率好坏。当然也可能有不精准的时候。
    c. extra：额外信息。
        + distinct: 在 select 部分使用了 distinct 关键字
        + using filesort: 出现这个时说明 MySQL 需要额外的排序操作，不能通过索引顺序达到排序效果。一般都是建议优化掉的。
        

一个小场景：
    当你发现 rows 不对，没有用到正确的索引时，可以使用 analyze table tablename 进行重新统计索引信息。或者直接使用 force index 强制走正确的索引。
```

### 3.  使用覆盖索引避免回表操作

```markdown
禁止使用 select *
```

### 4. 遵循最左匹配原则

### 5. 联合索引重建 或 修改等价 SQL 使其可以使用上索引

```markdown
当前表：student(id, name, age, sex, course)
当前表索引: name_age_course = (name, sex, course)

举个例子：
-- 这时 name 会用走索引，但是 course 就不符合最左前缀了
-- 观察到 sex 只有两个值，'male' 和 'female', 我知道要搜的是个女生
select id, name, age 
from student
where name = 'caiqj' and course = '语文'；

-- 优化后，三个字段都可以使用到联合索引
select id, name, age
from student
where name = 'caiqj' and sex = 'female' and course = '语文'；
```

### 6. 利用索引下推

```markdown
索引下推是 MySQL 5.6 之后官方出的特性。还是上面那个例子，假如说我们写了一条 SQL:

    `select * from student where id between 1 and 4 and name like '阿菜%';`
    
在 MySQL 5.6 之前，需要进行 4 次回表操作。由于 id 是范围查询，name 是不会走索引的。结果就是找出 id in (1, 2, 3, 4) 的四条记录，然后回表去搜索叫 '阿菜XXX' 的记录。

在 MySQL 5.6 及以上的版本，依旧是只有 name 会走索引，但是在走索引的过程中，MySQL 会先筛选出其中叫 '阿菜XXXX' 的记录。然后再进行回表操作。这样就可以有效减少回表次数了。

索引下推可以显示关闭，但是这么好的特性我们当然要使用它。
```

### 7. 选择 唯一索引 还是 普通索引？

[重点要回答到 change buffer，看这篇笔记](https://github.com/LydiaCai1203/leetcode-practice/blob/master/mysql_performance/unique_idx_common_idx.md)

```markdown
总结：
1. 查询性能：唯一索引和普通索引都差不多。
2. 更新性能：唯一索引无法利用 change buffer, 普通索引 + change buffer 更加适合写操作以后不会马上对该记录查询的场景，比如账本系统。如果说存在上面说的就要显式关闭 change buffer。
```

### 8. 适当使用前缀索引

```markdown
主键长度不宜过长，首先过长占用的空间大，磁盘所能存储的节点就少，那么树高就会变高，磁盘 IO 次数就会增多。可以定义字符串的一部分作为索引。或者引申到对于数据库中过长的字段该如何优化的问题(1.hash 2.比如一些固定的前缀或者后缀，就可以去掉再存储等等)。

场景：
www.domain.com 的存储优化，可以去掉 www（一级域名), 如果前缀不容易区分但是后缀容易区分，可以 reverse 一下再 `alter table {tablename} add index title_pre({column_name}(100))`

优点：
1. 节省空间
2. 不用额外增加太多的查询成本

缺点：
1. 只要用了前缀索引不管符不符合覆盖索引的条件都会进行回表操作。
```

### 9. 注意条件字段函数操作导致未走索引

```markdown
对索引字段做函数操作，比如 cast, convert 等等，可能会破坏索引值的有序性，因此优化器就会决定放弃走树搜索功能。但是并不是放弃索引。
```

### 10. 避免隐式类型转换 和 隐式字符集转换

```markdown
1. 比如 id: integer，你非要 `where id = '1'`。
2. 比如 name 的字符集是 utf8mb4，但是比较的时候非要用 utf8 比较，这时 MySQL 内部就会有 convert(name using utf8mb4) 的隐式转换的动作了。

上面两种情况都会导致不走索引。
```

### 11. redo log flush - 告诉 MySQL 可以 flush 多快

```markdown
莫名其妙的问题：
有时发现 MySQL 突然变得很慢。可能是因为正在 redo log flush。

概念：
redo log 是我们对数据库的操作日志，他存在与内存中，每次操作一旦写了 redo log 就会立即返回结果。把 redo log 上的操作刷新到磁盘上就是 flush 了。

什么时候会 flush?
1. redo log 写满了。(这时系统会停止所有的更新操作)
2. 系统内存不足，需要新的内存页，当内存不够用的时候，需要淘汰一些旧的数据页，如果淘汰的是 "脏页", 这时就需要将脏页中的数据 flush 到磁盘了。
3. MySQL 认为空闲的时候，就会 flush 一点脏页。
4. MySQL 正常关闭的时候，会把所有内存的脏页都 flush 到磁盘上。

把握 flush 时机：
1. 告诉 InnoDB 所有主机的 IO 能力，这样 InnoDB 才知道可以 flush 多快。设置 innodb_io_capacity 参数，建议设置为磁盘的 IOPS。
```








































































































