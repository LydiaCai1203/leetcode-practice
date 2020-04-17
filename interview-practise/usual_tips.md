# Usual Tips（随便一些什么问题记录）

## 1. 正是环境的数据库和测试环境的数据库放在一台机器上是通常做法么？

```python
放在一台机器上其实没有什么影响，但是应该考虑以下几点：
1. 正是环境的数据库名字/密码/用户名 应该和 测试环境的数据库配置不一样。不然测试环境的泄漏了正式环境的也泄漏了。
2. 如果从灾备角度来考虑的话，正式环境的数据库和测试环境的数据库应该放在不同的机器上，不同机房。如果机房漏水了或是别的什么。
```

## 2. sqlalchemy bulk update - synchronize_session

```markdown
**问题描述**：
网上很多人说只有在 `in_` 操作的时候才会报错，但其实应该是批量更新的时候就会 raise Exception。还是直接看官方文档比较靠谱。我来翻译一下吧。

----------------------------------------------------
**USAGE EXAMPLE**:
sess.query(
    User
).filter(
    User.age == 25
).update(
    {
        User.name == 'caiqj'
    },
    synchronize_session=False
)

----------------------------------------------------
**DOC**
choose the strategy to update the attributes on objects in the session.
选择一种在会话中做对象属性更新的策略。你可以取以下的值：

*False* - don't synchronize the session.This option is the most efficient and is reliable once the session is expired，which typically occurs after a commit(), or explicity using expire_all().Before the expiration，updated objects may still remain in the session with stale values on their attributes, which can lead to confusing results.
不会同步 session，这个选项是性能最高的而且最可靠的一旦会话里的数据过期。会话中的数据过期则会发生在使用了commit之后，或是使用了 expire_all()之后。在会话中的数据过期之前，原本你以为更新以后的数据，在会话中还是更新以前的数据。这会导致一些困惑。

*fetch* - performs a select query before the update to find objects that are matched by the update query. The updated attributes are expired on matched objects.
在做更新对象之前做一个查询动作，也就是说会做两次查询。这些已经被更新的对象属性会查询出来的这些对象上过期。也就是说 fetch 会去更新会话中的数据。

*evaluate* - Evaluate the Query's criteria in Python straight on the objects in the session. If evaluation of the criteria isn't implemented, an exception is raised.
会评估在 Python 中这些直接作用在会话中的对象上的查询条件是否有被实现，如果没有就会抛出异常。
```

## 3. sqlalchemy insert

```markdown
# 这段时间写插入的时候学到在 sqlalchemy 中插入有很多方法可以实现
# session.add()
place an object in the Session, its state will be persisted to the database on the next flush operation.Repeat calls to `add()` will be ignored.The opposite of `add()` is `expunge()`.
把一个对象放进会话里，当你在 `add()` 之后使用了 `flush()` 它的状态会被持久更新到数据库中，重复调用 `add()` 不会起作用。`expunge()` 可以将某个对象从会话中删除。

# session.bulk_insert_mappings(mapper, mappings, return, default=False, render_nulls=False)
Perform a bulk insert of the given list of mapping dictonaries. The bulk insert feature allows plain Python dictionaries to be used as the source of simple `INSERT` operations which can be more 
```




