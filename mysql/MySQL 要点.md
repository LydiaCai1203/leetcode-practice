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
>    SELECT col1
>
>    FROM table
>
>    WHERE Match(col1) Against(search_exp, IN BOOLEAN MODE);
>
> 10. 匹配heavy 但是排除rope
>
>      SELECT col1
>
>      FROM table
>
>      WHERE Match(col1) Against('heavy -rope*' IN BOOLEAN MODE);
>
>      -rope* 就是指明要排除任何以rope开头的词
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
> 18. 如果表中的行数少于3行，全文本搜索不回返回结果。
>
> 19. 会忽略词中的单引号，将don't索引为dont
>
> 20. 仅在MyISAM数据库引擎中支持全文本搜索



###### **插入数据**

>1. INSERT INTO table  VALUE(NULL, 'caiqj', 'China', '22', NULL);
>
>2. 自增列只需赋值NULL即可；最好是写成下面这种形式，在表名之后标明列名：
>
>   > INSERT INTO table(col1, col2, col3)
>   >
>   > VALUES(value1, value2, value3);
>   >
>   > 这样写的好处是在表的结构发生变化以后，这样的插入语句还是能得到正确的结果的。
>
>3. 不管使用哪种方法，如果没有给出列名，就要在插入的时候给出所有列的值，如果给出了列名，就要在插入的时候给出所有给出列名的列的值。
>
>4. INSERT可以省略的列必须是可以为NULL，或者在表的定义中给出默认值的。
>
>5. INSERT LOW_PRIORITY INTO 可以降低INSERT语句的优先级.
>
>6. INSERT INTO table(col1, col2, col3)
>
>      VALUE(val11, val12, val13),(val21, val22, val23);
>
>   // 一次性插入多条比一次插一条要快
>
>7. **INSERT SELECT**
>
>   > a. 它可以将一条SELECT语句的结果插入表中,由一条insert和一条select组成
>   >
>   > b. INSERT INTO table(col1, col2, col3)
>   >
>   > ​    SELECT(col1, col2, col3) 
>   >
>   > ​    FROM tabl2;



###### **更新和删除数据**

> 1. UPDATE table
>
>       SET col1=value1
>
>       WHERE col1=condition1;
>
> 2. UPDATE同样可以使用在子查询当中，上例中如果在更新多行的时候出现错误，整个UPDATE操作就会被取消，所有更新了的行都会恢复到它们原本的值。如果希望即使发生错误，也继续更新的话，就可以使用IGNORE关键字。
>
>       UPDATE IGNORE table
>
> 3. SET col1=NULL当然也是被允许的
>
> 4. DELETE FROM table
>
>       WHERE col1=val1;
>
>       // 要注意DELETE删除的是表中的行 不是表本身。
>
> 5. 可以达到删除所有行的语句还有TRUNCATE TABLE语句，它会完成想相同的工作，但是速度更快。因为它相当于是删除原来的表然后重新创建一个表。



###### **创建和操纵表**

> 1. CREATE TABLE table_name
>
> ​        (   stu_id    int    NOT NULL    AUTO_INCREMENT,
>
> ​		    stu_name    char(50)    NOT NULL    DEFAULT    'student_none',
>
> ​		    PRIMARY KEY (cost_id)
>
> ​        )   ENGINE=InnoDB;
>
> 2. 创建一个表的时候有9列，MySQL会忽略空格，语句也可以在一个长行上进行输入。就可以在表名之前添加上IF NOT EXISTS;
>
> ​       CREATE TABLE IF NOT EXISTS table_name
>
> ​       DROP TABLE IF EXISTS table_name
>
> 3. 使用单一列作为主键： PRIMARY KEY (col1)
>
> 4. 使用组合列作为主键： PRIMARY KEY (col1, col2)
>
> 5. 主键值当然是不允许为NULL的
>
> 6. 每个表都只能有一个列被赋予AUTO_INCREMENT，而且它还必须被索引，比如让它成为主键。
>
> 7. 如果自己给了一个值，并且这个值是唯一的话，后续的增量将开始使用该手工插入的值。
>
> 8. 你可以使用last_insert_id()来获取最后一个AUTO_INCREMENT的值
>
> 9. MySQL有一个具体管理和处理数据的内部引擎，在你使用CREATE TABLE的时候，该引擎具体创建表，在你使用SELECT语句或进行其他数据库处理时，该引擎在内部处理你的请求。
>
> 10. 三种引擎的优缺点：
>
>     > a. InnoDB是一个可靠的事务处理引擎，但是不支持全文搜索
>     >
>     > b. MEMORY在功能上等同于MyISAM，但是由于数据存储在内存，而不是磁盘当中，速度很快，适合创建临时表
>     >
>     > c. MyISAM是一个性能极高的引擎，它支持全文本搜索，但是不支持事务处理
>
> 11. 混用引擎的一大缺陷就是外键无法跨越。
>
> 12. 更改表结构可以使用ALERT TABLE:
>
>         ALERT  TABLE  table_name
>
>         ADD  col_n char(20);
>
>         DROP  COLUMN  col_n; 
>
> 13. 使用ALERT 来创建外键：
>
>         ALERT  TABLE  table1_name
>
>         **ADD  CONSTRAINT**  fk_name
>
>         FOREIGN  KEY  (col11)  REFERENCES  table_name1  (col21);
>
> 14. **使用ALERT之前应该对表进行一个备份，因为数据库表的更改不能撤销**
>
> 15. 删除表则使用**DROP** TABLE table_name;
>
> 16. 重命名表就是用RENAME TABLE table_name1 TO table_name2, table_name3 TO table_name2, …..;



###### **使用视图**

> 1. 视图就是虚拟的表，与包含数据的表不一样，视图只包含使用时动态检索数据的查询。就是一个方便查询的临时表。
>
> 2. 使用视图的一个好处就是可以给用户授予表的特定部分的访问权限而不是整个表的访问权限。
>
> 3. 视图必须唯一命名，创建的数量并没有限制，可以从其它的视图中提取数据来构建另一个视图，可以使用ORDER_BY，视图无法索引，也不能有关联的触发器或者是默认值。
>
> 4. **CREATE VIEW** view_name **AS**
>
>       SELECT col1, col2, col3
>
>       FROM table1, table2, table3
>
>       WHERE condition1, condition2
>
> 5. 可以对视图使用INSERT UPDATE DELETE, 但是更新一个视图将会更新其基表。
>
> 6. 如果MySQL无法正确地确定被更新的基数据，就不允许更新，实际上就意味着，如果视图的定义中有分组、联结、子查询、并、聚集函数、DISTINCT就不能在对它进行更新的动作了。



###### **使用存储过程**

> 1. 简单来说就是为以后的使用而保存的一条或者是多条MySQL语句的集合，可以将其视为批文件，但是存储过程的作用并不局限于批处理。
>
> 2. 使用存储过程会比使用单独的SQL语句要快一点
>
> 3. 执行存储过程
>
>    CALL producer_name(@return_val1, @return_val2);
>
>    会将结果回传出来，然后就可以在select语句中使用@来提取变量值。
>
>    存储过程可以显示结果，也可以不显示结果
>
> 4. 创建存储过程
>
>    CREATE PRODUCER producer_name(arg1, arg2)
>
>    BEGIN
>
>    ​		SELECT AVG(score) AS score_avg
>
>    ​		FROM students;
>
>    END;
>
> 5. DROP PRODUCER producer_name;
>
> 6. DROP PRODUCER producer_name IF EXISTS;
>
> 7. CREATE PRODUCER producer_name(
>
>    ​		OUT price_low DECIMAL(8, 2),
>
>    ​		OUT price_high DECIMAL(8, 2),
>
> ​		)
>
> ​		BEGIN
>
> ​				DECLARE total DECIMAL(8, 2);     // 声明一个变量
>
> ​				DECLARE texture INT DEFAULT 6;     // 声明一个变量
>
> ​				SELECT MIN(price)
>
> ​				INTO price_low
>
> ​				FROM table_name;
>
> ​        		SELECT MAX(price)
>
> ​				INTO price_high
>
> ​				FROM table_name;
>
> ​		END;
>
> 8. IN表示传递给存储过程，OUT表示从存储过程传出，INOUT对存储过程的传入和传出类型的参数，INTO可以帮助我们将相应的值保存到对应的变量中。
>
> 9. 所有的MySQL变量都必须以@开始
>
> 10. SELECT @price_low; 就可以搜索出其中的变量。
>
> 11. 存储过程也有IF THEN;
>
> 12. SHOW CREATE PRODUCER producer_name; 
>
>     可以显示当时创建该存储过程的语句



###### **使用游标**

> 1. 游标是一个存储在MySQL-server上的数据库查询，它并不是一条SELECT语句，而是一个检索出来的结果集，存储了游标之后，应用程序可以根据需要来滚动或者是浏览其中的数据。
>
> 2. MySQL的游标只能用于存储过程。
>
> 3. CREATE PRODUCER producer_name()
>
>    BEGIN
>
>    ​		DECLARE cursor_name CURSOR
>
>    ​		FOR
>
>    ​		SELECT col1 FROM table;
>
>    END;
>
> 4. OPEN cursor_name;  // 存储检索出的数据以供浏览和滚动
>
> 5. CLOSE cursor_name; // 释放游标使用的所有内部内存和资源，因此每个游标在不需要的时候都应该关闭。
>
> 6. FETCH cursor_name;  // 会指定检索什么数据，检索出来的数据存储在什么地方，它还向前移动游标中的内部指针，使下一条FETCH语句检索下一行。



###### **使用触发器**

> 1. 保持每个数据库的触发器名是唯一的
>
> 2. CREATE TRIGGER trigger_name AFTER INSERT ON table
>
>    FOR EACH ROW SELECT 'Product added';
>
>    上面的例子将会在insert语句执行成功以后，启动触发器，代码对每个插入行执行，都会显示一次Product added
>
> 3. 只有表才支持触发器
>
> 4. 每个表最多支持6个触发器，每条insert\update\delete前后可以执行一次
>
> 5. DROP TRIGGER trigger_name;
>
> 6. 关于INSERT TRIGGER:
>
>    > a. 在INSERT触发器代码中，可引用一个名为NEW的虚拟表，访问被插入的行。
>    >
>    > b. BEFORE INSERT中，NEW中的值是可以被修改的。
>    >
>    > c. 对于自增列，NEW在INSERT执行之前包含0，在INSERT执行之后包含新的自动生成的值。
>    >
>    > d. CREATE TRIGGER trigger_name AFTER INSERT ON table_name
>    >
>    > ​    FOR EACH ROW SELECT NEW.col1;
>    >
>    > e. BEFORE在于数据的验证和精华，目的是为了保证插入表中的数据确实是需要的数据。
>
> 7. 关于DELETE TRIGGER:
>
>    > a. 在DELETE触发器中，有一个名OLD的虚拟表，来访问被删除的行。
>    >
>    > b. OLD表是只读的，不能更新的。
>    >
>    > c. CREATE TRIGGER trigger_name BEFORE DELETE ON table_name
>    >
>    > ​    FOR EACH ROW
>    >
>    > ​    BEGIN
>    >
>    > ​		INSERT INTO TABLE_NAME(col1, col2, col3)
>    >
>    > ​        VALUES(val1, val2, val3);
>    >
>    > ​	END;
>    >
>    > d. 在任意订单被删除前都会执行此触发器，他会将OLD中将要被删除的订单保存到另外一张表中。
>
> 8. 关于UPDATE TRIGGER：
>
>    > a. 在UPDATE触发器中，有一个名OLD的虚拟表来访问以前的值， 有一个名为NEW的虚拟表来访问新的更新的值。
>    >
>    > b. CREATE TRIGGER trigger_name BEFORE UPDATE ON table
>    >
>    > ​    FOR EACH ROW SET NEW.col1=Upoer(NEW.col1);



###### **管理事务处理**

> 1. 事务处理可以用来维护数据库的完整性，它可以保证成批的MySQL操作要么完全执行，要么就完全不执行。
>
> 2. **事务**：指一组SQL语句
>
> 3. **回退**：指撤销指定SQL语句的过程
>
> 4. **提交**：指将为存储的SQL语句结果写入数据库表
>
> 5. **保留点**： 指事务处理中设置的临时占位符，你可以对它发布回退。
>
> 6. 管理事务处理的关键在于将SQL语句分解为逻辑块，并明确规定数据何时应该会退，何时不应该会退。
>
> 7. SELECT * FROM table1;
>
>    START TRANSACTION;
>
>    DELETE FROM table1;
>
>    SELECT * FROM table1;
>
>    ROLLBACK;    // 只能用在一个事务当中，但是不能会退CREATE和DROP操作
>
>    SELECT * FROM table1;
>
> 8. **COMMIT**
>
>    > START TRANSACTION;
>    >
>    > DELETE FROM table1 WHERE condition1;
>    >
>    > DELETE FROM table2 where condition2;
>    >
>    > COMMIT;
>
> 9. 当COMMIT&ROLLBACK执行完毕以后，事务就会自动关闭；
>
> 10. 保留点有点游戏存档的意味，savepoint delete1;  rollback delete1;
>
> 11. 如果你想要只是MySQL不自动提交更改的话：
>
>     SET autocommit=0;



###### **全球化和本地化**

> **字符集**：字母和符号的集合；
>
> **编码**：某个字符集成员的内部表示；
>
> **校对**：规定字符如何比较的指令；

> 1. SHOW CHARACTER SET;   // 可以显示所有可用的字符集以及每个字符集的描述和默认校对。
>
> 2. CREATE TABLE table_name
>
>    (Col1 int, col2 varchar(10))DEFAULT CHARACTER SET hebrew
>
>    COLLATE hebrew_general_ci;



###### **MySQL是一个多用户多线程的DBMS，它经常同时执行多个任务，如果这些任务中的某一个任务执行缓慢，所有的请求都会执行缓慢，所以你可以kill掉某个process**

1. 使用explain语句来让mysql解释它是如何执行的各条语句
2. 在导入数据的时候，应该关闭自动提交
3. 必须使用数据库表以改善数据检索的性能。
4. 使用多条SELECT语句然后用UNION进行连接，代替WHERE中使用多个OR，可以大大提升速度。
5. like很慢，最好使用fulltext而不是like
6. MySQL有变长串和定长串，有些变长数据类型具有最大的定长，有些则是完全变长的，不管是哪种，只有指定的数据会得以保存.
7. MySQL处理定长列比变长列要快，而且变长列不允许进行索引，因为会影响性能。
8. 其实varchar(n) n<=255