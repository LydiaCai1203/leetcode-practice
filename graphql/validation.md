# Validation

    通过使用类型系统，可以预先确定GraphQL查询是否有效。这允许服务器和客户端在创建无效查询时有效地通知开发人员，而不必依赖于运行时检查。
    
#### named fragment
```python
{
  hero {
    name
    ...DroidFields
  }
}

fragment DroidFields on Droid {
  primaryFunction
}
```

#### inline fragment
```python
{
  hero {
    name
    ... on Droid {
      primaryFunction
    }
  }
}
```

#### query result
```python
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "primaryFunction": "Astromech"
    }
  }
}
```
