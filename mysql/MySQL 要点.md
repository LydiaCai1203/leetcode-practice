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
> 3. 