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