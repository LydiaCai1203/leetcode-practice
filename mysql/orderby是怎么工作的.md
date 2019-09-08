# orderby 是怎么工作的


[TOC]
--------------------------------------

```mysql
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `city` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `age` int(11) NOT NULL,
  `addr` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city` (`city`)
) ENGINE=InnoDB;

select city,name,age from t where city='杭州' order by name limit 1000;
```

## 全字段排序
    为了避免全表扫描，city这个字段建立了索引，MySQL会给每一个线程都分配一段内存用于排序，称为sorted_buffer。
+ 1. 初始化sorted_buffer， 确定要放入name, city, age 这三个字段
+ 2. 从索引city中找到第一个满足city='杭州'的主键id
+ 3. 到主键id索引去拿出整行，取出name、city、age这三个字段的值，存到sorted_buffer中
+ 4. 从索引city中找到下一个满足city='杭州'的主键id
+ 5. 重复步骤3和步骤4，直到city的值不满足条件为止
+ 6. 对sorted_buffer中的数据进行快排，
    + 其中可能在sorted_buffer中排序，也可能会使用到外部排序，这取决于sorted_buffer_size。
    + 可以查看是否使用了外部排序的 代码不贴了，感觉不大可能用得上

**缺点：如果select出来的字段过多，放在sorted_buffer中的数据就多，如果内存不能满足快排，就要借助外部排序，性能就会低很多。**

## rowid排序
    `SET max_length_for_sort_data = 16;` 可以改变sorted_buffer的大小。如果单行长度超过sorted_buffer_size的话，MySQL就会
    采用另一种算法。新的算法是：放入sorted_buffer的字段只有要排序的字段和主键id。
+ 1. 初始化sorted_buffer，确定要放入name, 主键id 这两个字段
+ 2. 从索引city中找到第一个满足city='杭州'的主键id
+ 3. 到主键id索引去拿出整行，取出name，主键id 这两个字段的值，存到sorted_buffer中
+ 4. 从索引city中找到下一个满足city='杭州'的主键id
+ 5. 重复步骤3和步骤4，直到city的值不满足条件为止
+ 6. 在sorted_buffer按照name字段进行快排。
+ 7. 遍历排序的结果，取出前1000行，并按照id回到表中去取出city,name,age这个三个字段返回给客户端。

## 两种排序方式的比较

