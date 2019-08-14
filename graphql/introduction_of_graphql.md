# GraphQL 介绍

**GraphQL是一种API查询语句，是一种和任何数据库，引擎无关的，之和你的代码和数据有关的查询语句**

[TOC]
## GraphQL Service的组成

### types
```python
type Query{
    me: User
}

type User{
    id: ID
    name: string
}
```

### function for each field on each type
```python
function Query_me(request){
    return request.auth.user;
}

function User_name(user){
    return user.getName();
}
```

### query example
```python
{
    me{
        name
    }
}
```

### query result example
```python
{
    "me": {
        "name": "caiqj"
    }
}
```