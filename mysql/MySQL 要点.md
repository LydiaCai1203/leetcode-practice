## MySQL 复习大纲

#### 1. 一张表，里面id为子增主键，当insert了17条记录以后，删除了第15， 16， 17条记录，现在把MySQL重启，再insert一条记录，这条记录的id是18还是15？

##### 答： *如果表的的类型是MyISAM, 那么是18，因为MyISAM会把自增主键的最大ID值存在数据文件里面，重启MySQL，自增主键的最大ID也是不会丢失的。如果表的类型是InnoDB，那么是15，因为自增主键的最大ID记录到内存中，所以如果重启数据库的话会导致最大ID丢失。*



#### 2. 简洁描述MySQL中的InnoDB支持的四种事务隔离级别名称，以及逐级之间的区别。

##### 答： *SQL标准定义的四个隔离级别为：*

> 1. Read uncommitted 
>
>    > 所有事务都可以看到其它未提交事务的执行结果，读取到未提交的数据，也称之为脏读。
>
> 2. Read committed 
>
>    > **这不是MySQL默认的隔离级别**，一个事务只能看见已经提交事务所做的改变，这种隔离级别支持所谓的不可重复读，因为同一事务的其它实例在该实例的处理期间可能会有新的commit,所以同一个select语句都可能返回不同的结果。
>
> 3. Repeatable read
>
>    > **这是MySQL默认的隔离级别**，它确保同一个事务的多个实例在并发地读取数据时，会看到同样的数据行，但是会导致另一个问题也就是'幻读'。
>
> 4. Serializable
>
>    > 这是最高的隔离级别,它通过强制事务排序，使之不可能互相发生冲突，也就是说，它是在每个读的数据行上加上共享锁，但是这样做会导致的直接问题就是，可能导致大量的超时现象和锁竞争现象。



#### 3. 主键值规则

> 1. 不更新主键列中的值
> 2. 不重用主键列中的值
> 3. 不在主键列中使用可能会更改的值



#### 4. MySQL是基于客户机-服务器的数据库，服务器的部分是负责所有数据访问和处理的一个软件。关于数据添加、删除、更新的所有请求都由服务器软件完成。这些请求或更改来自运行客户机软件的计算机。客户机软件通过网络提交该请求给服务器软件，服务器软件处理这个请求，再将结果返回给客户机软件。



#### 5. Mysql -h host -P port -u user -p database 回车以后输入password



#### 6. 命令和表名都是不区分大小写的



#### * 常用命令(必须加上;表示语句结束，SQL中的所有)

###### **show**

> 1. USE DATABASES;      # DATABASES CHANGED 代表成功选中数据库
> 2. SHOW DATABSES;  or   SHOW TABLES;  
> 3. SHOW COLUMNS FROM tablename;      # 字段名、类型、是否为空、键信息、默认值、其他信息
> 4. DESCRIBE tablename;    # 等价于3的另一种快捷方式
> 5. SHOW STATUS;                # 显示广泛的服务器状态信息
> 6. SHOW GRANTS;              # 显示授予用户的安全权限
> 7. SHOW ERRORS;    or    SHOW WARNINGS;      # 显示服务器错误和警告消息
> 8. HELP SHOW                    # 显示出所有跟SHOW有关的命令



###### **select/limit**

> 1. SELECT [COLUMN_NAME, ...] FROM TABLE;
> 2. SELECT * FROM TABLE;        # 检索不必要的列会降低检索和应用程序的性能
> 3. SELECT DISTINCT COLUMN FROM TABLE;    # 只返回不同的列名，DISTINCT又是关键字，必须放在列名的前面
>    **不能部分使用DISTINCT,这个关键字应该应用于所有列而不仅仅是前置它的列，除非指定的两个列都不同，否则所有行都将被检索出来**
> 4. SELECT COLUMN FROM TABLE LIMIT NUMER;
> 5. SELECT COLUMN FROM TABLE LIMIT START, NUMBER;     # 第一个数为开始位置，第二个数为要检索的行数。START表示的是第START行，但是实际上第一行的START=0。
>    此外NUMBER表示的能检索出来的最大行数，所以如果总共只又13条数据，LIMIT 10, 5; 最后只会出来三行数据。
> 6. SELECT COLUMN FROM TABLE LIMIT NUMBER OFFSET START;
> 7. SELECT TABLE.COLUMN FROM DB.TABLE;
> 8. SELECT TABLE.COLUMN FROM TABLE; 



###### **order by/is null/not is null/desc** 

> 1. SELECT COLUMN FROM TABLE ORDER BY COLUMN;     # 如果指定ORDER BY 的 多个COLUMNS 的时候就会先按照所规定的列的顺序执行, ORDER BY COL1, COL2; 先按照COL1进行排序，在多行具有相同COL1的时候，按照COL2进行排序。
>
>    **也就是说如果所有COL1的值都是唯一的话就不会按照COL2进行排序了**
>
> 2. SELECT COLUMN FROM TABLE ORDER BY COLUMN DESC;     # 默认情况是：ASC
>
> 3. SELECT COLUMN FROM TABLE ORDER BY COL1 DESC, COL2;
>
> 4. SELECT COLUMN FROM TABLE ORDER BY COLUMN DESC LIMIT 1;   # **LIMIT必须在ORDER BY的后面,次序错误就会报错**
>
> 5. SELECT COL1 FROM TABLE WHERE CONDITION;
>
> 6. = 等于; <>不等于; !=不等于; BETWEEN; 在指定的两个值之间
>
> 7. SELECT COL FROM TABLE WHERE COL='Col';      # 条件里的字符串是不会区分大小写进行查询的。
>
> 8. SELECT COL1 FROM TABLE WHERE BETWEEN VALUE1 AND VALUE2;
>
> 9. NULL <> 0 or '' or ' ';
>
> 10. SELECT COL FROM TABLE WHERE COL IS NULL;    # IS NOT NULL也是存在的



###### **where/and/or/in/not** 

> 1. WHERE CONDITION1 AND CONDITION2;
>
> 2. WHERE CONDITION1 OR CONDITION2;
>
> 3. WHERE vend_id=1002 OR vend_id=1003 AND prod_price>=10;
>
>    > a. 先看and然后看or
>    >
>    > b. 等价于(WHERE vend_id=1002) OR (vend_id=1003 AND prod_price>=10);
>
> 4. WHERE COL IN (VALUE1, VALUE2);
>
>    > a. IN 一般会比 OR 执行地更快
>    >
>    > b. IN 还可以包含其它的SELECT语句
>    
> 5. WHERE COL NOT IN (VALUE1, VALUE2);



###### **like** 

> 1. SELECT COL FROM TABLE WHERE COL LIKE '%su%'
>
> 2. LIKE 's%e' ； LIKE '%se' ；LIKE 'se%' ；
>
> 3. % 可以匹配任何东西，但是也有一个例外，即NULL，也就是说不能匹配值为NULL作为产品的行
>
> 4. LIKE '_ton anvil';     # _可以匹配一个字符
>
> 5. 通配符的处理一般比前面讨论的其它搜索花的时间更加长。
>
>    > 1. 不要过度使用通配符，如果其它操作符能达到相同的目的，应该使用其它操作符。
>    > 2. 通配符位于搜索模式的开始处，搜索起来是最慢的。



###### **正则表达式** 

> 1. WHERE COL REGEXP '1000';
>
> 2. 关键字LIKE被REGEXP替代，WHERE COL REGEXP '.000'; '.'是一个特殊字符，表示匹配任意一个字符
>
> 3. SELECT COL FROM TABLE WHERE COL LIKE '111' LIMIT 1;   
>
> 4. SELECT COL FROM TABLE WHERE COL REGEXO '111'  LIMIT 1;
>
>    > **LIKE 和 REGEXP的一个重要的区别就是3式不会返回结果，但是使用4式会返回结果**
>
> 5. SELECT COL FROM TABLE WHERE COL REGEXP BINARY 'CQJ .000';
>
>    > 使用BINARY即区分大小写
>
> 6. REGEXP '1000|2000';    # ''或者''操作符
>
> 7. REGEXP '[123]Ton';        # 匹配1Ton，2Ton，3Ton
>
> 8. REGEXP '^1234|4567';  # ^就是取反的意思
>
> 9. REGEXP '[123456789]'  <==>  REGEXP '[1-9]' OR REGEXP '[A-Z]';
>
> 10. 匹配特殊字符的时候使用\\\作为前缀符进行转义
>     1.  '*' 表示0或者多个匹配； '+' 表示1或者多个匹配；'？'表示0或者1个匹配；'{n}'指定数目的匹配；'{n, }' 表示不少于指定数目的匹配；''{n, m}'' 匹配数目的范围；
>     2. REGEXP '\\\\([0-9] sticks?\\\\)'            # 可以匹配到(1 sticks) or (2 stick)
>     3.  REGEXP '[[:digit:]]{4}'.                   # 找到连续四位数字
>    
> 11. '^'表示的是文本的开始; '$'表示的是文本的结尾; '[[:<:]]'词的开始; '[[:>:]]'词的结尾; 当'^'在集合中，用来否定该集合。
>
> 12. 还可以使用不带数据库查询的语句进行正则的简单测试：
>
>     > select 'hello' regex '[0-9]';



###### **创建计算字段** 

> 1. 说些无聊的话：pandas 来导出excel
> 2. 在数据库服务器上完成(转换和格式化工作)比在客户机中完成要快得多
> 3. SELECT CONCAT(vend_name, '(', vend_contury, ')') FROM TABLE ORDER BY vend_name;     # 相当于字符串拼接
> 4. SELECT Concat(RTrim(vend_name), '(', RTrim(vend_country), ')') FROM vendors  ORDER BY vend_name;     # 相当于去掉右边所有的空格 有LTrim\RTrim\Trim
> 5. 3式和4式得到的拼接以后的列是没有名字的，如果要用到这个结果的话就需要给它用上别名。SELECT CONCAT(vend_name, '(', vend_contury, ')') AS vend_title;
> 6. SELECT quantity*item_price AS expanded_price;
> 7. SELECT Now();   # 返回当前的日期数据



###### **使用 数据处理函数**

> 1. SELECT Upper(COL) AS UP_COL FROM TABLE;      # Lower
>
> 2. SELECT Length(COL) FROM TABLE;
>
> 3. Located()、Soundex()、SubString();
>
> 4. SELECT COL1, COL2 FROM TABLE WHERE COL3='2005-09-01'
>
>    > 这样做有一个问题就是COL3含有具体的时间信息的时候，这样写就不会匹配到任何东西。也就是COL3实际上是一个datetime数据类型。
>
> 5. SELECT COL1 FROM TABLE WHERE Date(COL2)='2005-09-01';
>
>    > AddDate()        Day()                      Now()
>    >
>    > AddTime().       Hour()                   DayOfWeek()   # 对于一个日期，返回对应的星期几  
>    >
>    > CurDate()         Month()
>    >
>    > CurTime()         Minute()
>    >
>    > Date()                Second()
>    >
>    > Time()                Year()
>    >
>    > DateDiff()          # 计算两个日期之差
>    
> 6. WHERE Date(COL) BETWEEN '2005-09-01' AND '2005-09-30';
>
> 7. 一些数据处理函数
>
>    > Abs()        Cos()       Exp()       Mod()        Pi()        Rand()      Sin()       Sqrt()     Tan()



###### **汇总数据**

> 1. 聚集函数：运行在行组上，计算和返回单个值的函数
>
>    > AVG()    COUNT()    MAX()    MIN()     SUM()
>
> 2. SELECT AVG(price) AS avg_price; 
>
>    > a. 这个函数只适用于单个列，如果要求多个列的平均值，就要使用多次
>    >
>    > b. AVG()忽略列值为NULL的行
>
> 3. SELECT COUNT(*) AS num_cust;
>
>    > a. 对表中行的数目进行计数，不会忽略NULL值
>    >
>    > b. COUNT(column) 对特定列中具有值的行进行计数，会忽略NULL值
>    >
>    > example: select count(col) from table; 
>    
> 4. SELECT MAX(COL) FROM TABLE; 
>
>    > MAX() 忽略列值为NULL的行
>
> 5. SELECT MIN(COL) FROM TABLE;
>
>    > MIN() 忽略列值为NULL的行
>
> 6. SELECT SUM(COL) FROM TABLE;
>
>    > SUM() 忽略列值为NULL的行
>
> 7. **以上几个聚集函数都是默认ALL参数，除非指定DISTINCT**
>
> 8. SELECT AVG(DISTINCT price) AS avg_price FROM table;
>
>    > DISTINCT 必须使用列名，不能用于计算或表达式；
>
> 9. SELECT COUNT(DISTINCT price) FROM table;       # COUNT(DISTINCT)是会报错的
>
> 10. SELECT COUNT(*) AS num_items,
>
>    ​              MIN(prod_price) AS price_min,
>
>    ​			  MAX(prod_price) AS price_max,
>
>    ​              AVG(prod_price) AS price_avg
>
>    ​       FROM product;
>
> 11. 这些函数是高效设计，它们返回结果一般比你在自己的客户机应用程序中计算要快得多;



###### **分组数据**

> 1. SELECT vend_id, COUNT(*) AS num_prods FROM TABLE GROUP BY vend_id;
>
>    > a. 先将每个vend_id分组，然后再对每个分组的数据量进行汇总
>    >
>    > b. GROUP BY可以包含任意数目的列
>    >
>    > c. GROUP BY列出的每个列都必须是检索列或有效的表达是，但是不能是聚集函数
>    >
>    > d. 如果在SELECT中使用表达式，在GROUP BY中也必须使用相同的表达式，但是不能使用别名
>    >
>    > e. 除了聚集计算语句之外，SELECT中每个列都必须在GROUP BY子句中给出
>    >
>    > f. 如果分组列中具有NULL值，则会将NULL值作为一个分组进行返回
>    >
>    > g. GROUP BY必须出现在 WHERE之后，ORDER BY之前
>
> 2. where是过滤行，但是having是过滤分组
>
> 3. SELECT cus_id, COUNT(*) AS orders
>
> ​       FROM orders
>
> ​       GROUP BY cus_id
>
> ​       HAVING COUNT(*) >= 2
>
> 4. HAVING在分组以后过滤，WHERE在分组前过滤，WHERE排除的行不包括在分组中
>
> 5. SELECT vend_id, COUNT(*) AS num_prods,
>
> ​       FROM products
>
> ​       WHERE prod_price >= 10
>
> ​       GROUP BY vend_id
>
> ​       HAVING COUNT(*) >= 2;
>
> 6. 一般在使用GROUP BY子句时，应该也给出ORDER BY子句，这是保证数据正确排序的唯一方法，千万不要仅仅依赖GROUP BY排序数据
>
> 7. SELECT order_sum, SUM(quantity*item_price) AS ordertotal
>
> ​       FROM orderitems
>
> ​	   GROUP BY order_num
>
> ​       HAVING SUM(quantity*item_price) >= 50;
>
> ​       ORDER BY ordertotal;



###### **联结表**

> 1. 关系表的设计就是要保证把信息分解成多个表，一类数据一个表，各表通过某些常用的值（即关系设计中的关系互相关联）
>
> 2. 一个表的外键就是另一个表的主键
>
> 3. 笛卡尔积：由没有联结条件的表关系返回的结果为笛卡尔积，检索出的行的数目将是第一个表中的行数乘以第二表中的行数
>
> 4. left join(左联接) 返回包括左表中的所有记录和右表中联结字段相等的记录
>
>    > from A left join B on A.aID = B.bID
>
> 5. right join(右联接) 返回包括右表中的所有记录和左表中联结字段相等的记录
>
>    > from A right join B on A.aID = B.bID
>
> 6. inner join(等值连接) 只返回两个表中联结字段相等的行
>
>    > from A inner join B on A.aID = B.bID
>
> 7. 内部联结
>
>    > SELECT vend_name, prod_name, prod_price
>    >
>    > FROM vendors INNER JOIN products
>    >
>    > ON vendors.vend_id = products.vend_id
>    >
>    > > **不要联结不必要的表，联结的表越多，性能也就下降地越厉害**
>    > >
>    > > inner join = join = ,



###### **创建高级联结**

> 1. 自联结
>
>    > a. 自己和自己表联结
>    >
>    > b. SELECT p1.prod_id, p1.prod_name
>    >
>    > ​    FROM products as p1, products as p2
>    >
>    > ​    WHERE p1.bend_id = p2.vend_id AND p2.prod_id=p1.prod_id
>    >
>    > c. 有时候使用联结的时候效率会比子查询要高一些，所以应该尝试一下看看两种方法哪个性能会更高一些
>
> 2. 自然联结
>
>    > a. 标准的联结会返回所有的数据，但自然联结排除多次出现，使每个列都只返回一次
>    >
>    > b.  SELECT  p.*, v.*
>    >
>    > ​     FROM productinfo AS p NATURAL  JOIN vendors AS v;
>
> 3. 外部联结
>
>    > a. 联结包含了那些在相关表中没有关联行的行，这种联结就是外部联结
>    >
>    > b. SELECT 
>    >
>    > ​    FROM customer LEFT OUTER JOIN orders
>    >
>    > ​    ON customers.cust_id = orders.cust_id;
>    >
>    > c. 外部联结的话 没有的结果也会被选出来



###### **组合查询**

> 1. 任何具有多个WHERE子句和SELECT语句都可以作为一个组合查询给出，这两种技术在不同的查询中性能也不同，因此应该试一下这两种技术，以确定哪一种查询的性能会更加优秀。
>
> 2. SELECT vend_id, prod_id, prod_price
>
> ​       FROM products
>
> ​       WHERE prod_price <= 5
>
> ​       UNION
>
> ​       SELECT vend_id, prod_id, prod_price
>
> ​       FROM products
>
> ​       WHERE vend_id IN (1001, 1002)
>
> 3. 上一个例子中，第一个查询语句返回4行，第二个查询语句返回5行，UNION了以后返回的是8行而不是9行，因为在使用UNION的时候，重复的行会被自动去除。
> 4. 如果想返回所有的结果，就可以使用UNION ALL;
> 5. ORDER BY必须放在最后一行，而且是作用于全部的查询结果的



###### **全文本搜索**

> 1. 并非所有的引擎都支持全文搜索，两个最常用的引擎MyISAM和InnoDB，前者支持全文本搜索，但是后者不支持。
>
> 2. 比较使用 通配符和正则表达式匹配 与 全文本搜索：
>
>   > a. 通配符和正则表达式匹配通常要求MySQL尝试匹配表中的所有行，这些搜索极少使用表索引，因此，由于被搜索行数不断增加，这些搜索会非常地耗时。
>   >
>   > b. 通配符和正则表达式匹配都是明确控制，比较具体。
>   >
>   > c. 返回的结果不够智能，并不会区分只匹配了一次的行，和匹配了多次的行。
>
> 3. 为了使用全文本搜索，必须索引被搜索的列，而且要随着数据的改变不断地重新索引，在对MySQL进行适当的设计以后，将会自动进行所有索引和重新索引。
>
> 4. 一般在创建表的时候创建全文索引：
>
>    > CREATE TABLE table_1
>    >
>    > (
>    >
>    > ​		note_id  int  not null auto_increament,
>    >
>    >  	   prod_id  char(10)  not null,
>    >	
>    >  	   note_date  datetime  not null,
>    >
>    > ​        note_text text  null,
>    >
>    > ​        primary key(note_id),
>    >
>    > ​        **fulltext(note_text)**
>    >
>    > ) engine=MyISAM;
>
> 5. Fulltext 可以索引单个列也可以索引多个列，此外在定义之后，会自动维护该索引。
>
> 6. SELECT note_text
>
> ​       FROM productnotes
>
> ​       WHERE Match(note_text) Against('rabbit');
>
>   > a. Match()指定要被搜索的列，Against()指定要使用的搜索表达式
>   >
>   > b. Match()的值必须与Fulltext()的值相同，包括顺序
>   >
>   > c. 除非使用BINARY的方式，否则不被区分大小写
>
> 7. 使用全文搜索返回的结果会按照匹配程度等级进行降序排列返回，因此结果更加智能。
>
> 8. SELECT note_text
>
> ​       Match(note_text)  Against('rabbit') as rank
>
> ​       FROM productnotes;
>
>   > a. 在select中使用Match()将返回所有的结果
>   >
>   > b. 全文搜索会计算出等级值，等级值越高越符合搜索，根据词中的匹配数目，唯一次的数目，整个索引中词的总数，以及包含该词的行的数目。
>   >
>   > c. 由于搜索是基于索引的，所以全文搜索极快。
>   >
>
> 9. Boolean mode(slow)
>
> SELECT col1
>
> FROM table
>
> WHERE Match(col1) Against(search_exp, IN BOOLEAN MODE);
>
> 10. 匹配heavy 但是排除rope
>
>  SELECT col1
>
>  FROM table
>
>  WHERE Match(col1) Against('heavy -rope*' IN BOOLEAN MODE);
>
>  -rope* 就是指明要排除任何以rope开头的词
>
> 11. 下面是全文本布尔操作符
>
>  '+': 此必须存在； '-':此必须排除；'>':包含，而且增加等级值；'<':包含，而且减少等级值；'～'：取消一个词的排序值；'*': 词尾的通配符；'""':定义一个短语。
>
> 12. SELECT col1
>
> ​       FROM table
>
> ​       WHERE Match(col1) Against('+rabbit +bait' IN BOOLEAN MODE);
>
> ​       // 将会搜索所有包含rabbit&bait的行
>
> 13. SELECT col1
>
>     FROM table
>
>     WHERE Match(col1)  Against('rabbit bait' IN BOOLEAN MODE);
>
>     // 会匹配至少包含两个词中的一个词的所有行
>
> 14. SELECT col1
>
>     FROM table
>
>     WHERE Match(col1) Against('"rabbit bait"' IN BOOLEAN MODE);
>
>     // 会包含含有rabbit bait这个短语的行，这两个单词加上一个空格就是一个简单的短语
>
> 15. SELECT col1
>
>     FROM table
>
>     WHERE Match(col1) Against('>rabbit <carrot' IN BOOLEAN MODE);
>
>     // 匹配两个词，但是抬高rabbit的等级，降低carrot的等级
>
> 16. SELECT col1
>
>     FROM table
>
>     WHERE Match(col1) Against('+safe +(<combination)' IN BOOLEAN MODE);
>
> 17. 在布尔方式中，返回的结果是不会按照等级值降序排序返回的。
>
> 18. 