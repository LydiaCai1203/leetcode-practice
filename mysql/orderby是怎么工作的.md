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

**缺点：如果select出来的字段过多，放在sorted_buffer中的数据就多，如果内存不能满足快排，就要借助外部排序，性能就会低很多。外部排序使用的是归并排序算法，MySQL将数据分成12份，每一份都单独排序以后存在这些临时文件中，然后最后再把这些临时文件合并成一个有序的大文件。**

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
+ 1. rowid排序会要求回表，多造成磁盘读，因此不会被优先选择。
+ 2. 并不是所有的order by都会进行排序操作的，MySql之所以要生成临时表，并且在临时表上做排序操作，其原因都是因为原来的数据就是无序的。但是如果能保证从city索引上取下来的数据就是有序的。`alter table t add index city_user(city, name);`建立一个联合索引，只要这个city='杭州'这个字段是满足的，name这个值肯定是有序的。这样就不需要使用到sorted_buffer，也不需要使用到临时文件。

## 思考题
    假设你的表里面已经有了index(city, name)这个联合索引，然后你要查询杭州和苏州这两个城市的所有市民的姓名，并且按照名字排序，只取前面的100条数据。`mysql> select * from t where city in ('杭州'," 苏州 ") order by name limit 100;
    `请问这个过程是否会有排序？如果需要实现一个不需要排序的方案，你会怎么实现。如果有分页需求，使用limit 10000, 100,显示的是第101页的数据，实现方法又是什么呢？