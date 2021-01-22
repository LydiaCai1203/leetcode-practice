### 8.3.1 MySQL 如何使用索引

MySQL 使用索引进行以下操作：

+ 更快找到 满足 WHERE 条件的行
+ 在查询涉及到多个可能的索引时，MySQL 通常选择 “选择性”更高的索引(也就是哪个索引查出来的行数最小，就是用哪个索引)。
+ index (col1, col2, col3) 中，你可以使用 col1, 也可以使用 col1,col2, 还可以使用 col1, col2, col3
+ 涉及到多表关联的时候，如果关联的字段是同类型同大小 (char(10) = varchar(10) 被认为是同类型) , MySQL 使用索引的效率更高
  + 当遇到非二进制字符串间比较时，做比较的字符串应该是同一字符集，否则不会使用索引？
  + 不同类型的列间比较不会使用索引
+ 有 index(a, b), `select max(b), min(b) from test where a = 1;` MySQL 会为每一个 `MIN()`、`MAX()` 做一次单键查找，把每一个表达式都替换成一个常数值，直到所有的表达式都被替换为常数值了，就立即返回
+ 如果排序或分组都是在索引上完成的，如果是 `order by key_part1, key_part2 desc; ` 则会走索引排序
+ 使用覆盖索引提高查询性能
