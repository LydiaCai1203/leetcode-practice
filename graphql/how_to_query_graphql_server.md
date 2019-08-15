# query of Graqh-Server

[TOC]
## query field

### basic type fild(string int .etc.)

#### query example
```python
{
    hero {
        name
    }
}
```
#### query result
```python
{
    "data": {
        "hero": {
            "name": "iron-man"
        }
    }
}
```

-----------------------------
### fields refer to Objects

#### query example
```python
{
    hero {
        name
        friends {
            name
        }
    }
}
```
#### query result
```python
{
    "data": {
        "hero": {
            "name": "caiqj",
            "friends": [
                {"name": "wuchunling"},
                {"name": "jiaxuan"}
            ]
        }
    }
}
```

-----------------------------
### pass arguments to fields

**GraqhQL中，每一个field 和 object，都可以接受一个arguments集合**

#### query example
```python
{
    human(id: "1000") {
        name
        height
    }
}
```
#### query result
```python
{
    "data": {
        "human": {
            "name": "caiqj",
            "height": 1.52
        }
    }
}
```

-----------------------------
### pass arguments into scalar fields

#### query example
+ unit is a Enumeration type, unit of length, METER or FOOT
+ a GraphQL server can also declare its **own custom types**, as long as they can be serialized into your transport format
```python
{
  human(id: "1000") {
    name
    height(unit: FOOT)
  }
}
```
#### query result
```python
{
  "data": {
    "human": {
      "name": "Luke Skywalker",
      "height": 5.6430448
    }
  }
}
```

-----------------------------
### rename the result of a field to anything you want
+ when the two hero fields would have **conflicted**
#### query example
```python
{
  empireHero: hero(episode: EMPIRE) {
    name
  }
  jediHero: hero(episode: JEDI) {
    name
  }
}
```
#### query result
```python
{
  "data": {
    "empireHero": {
      "name": "Luke Skywalker"
    },
    "jediHero": {
      "name": "R2-D2"
    }
  }
}
```

-----------------------------
### reusable units（fragments）
+ Fragments let you construct sets of fields, and then include them in queries where you need to
+ fragments is frequently used to split complicated application data requirements into smaller chunks
#### query example
```python
{
  leftComparison: hero(episode: EMPIRE) {
    ...comparisonFields
  }
  rightComparison: hero(episode: JEDI) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  appearsIn
  friends {
    name
  }
}
```
#### query result
```python
{
  "data": {
    "leftComparison": {
      "name": "Luke Skywalker",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ],
      "friends": [
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        },
        {
          "name": "C-3PO"
        },
        {
          "name": "R2-D2"
        }
      ]
    },
    "rightComparison": {
      "name": "R2-D2",
      "appearsIn": [
        "NEWHOPE",
        "EMPIRE",
        "JEDI"
      ],
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```

-----------------------------
### Using variables inside fragments

#### query example
+ 只要查询到的前三个结果
```python
query HeroComparison($first: Int = 3) {
  leftComparison: hero(episode: EMPIRE) {
    ...comparisonFields
  }
  rightComparison: hero(episode: JEDI) {
    ...comparisonFields
  }
}

fragment comparisonFields on Character {
  name
  friendsConnection(first: $first) {
    totalCount
    edges {
      node {
        name
      }
    }
  }
}
```
#### query result
```python
{
  "data": {
    "leftComparison": {
      "name": "Luke Skywalker",
      "friendsConnection": {
        "totalCount": 4,
        "edges": [
          {
            "node": {
              "name": "Han Solo"
            }
          },
          {
            "node": {
              "name": "Leia Organa"
            }
          },
          {
            "node": {
              "name": "C-3PO"
            }
          }
        ]
      }
    },
    "rightComparison": {
      "name": "R2-D2",
      "friendsConnection": {
        "totalCount": 3,
        "edges": [
          {
            "node": {
              "name": "Luke Skywalker"
            }
          },
          {
            "node": {
              "name": "Han Solo"
            }
          },
          {
            "node": {
              "name": "Leia Organa"
            }
          }
        ]
      }
    }
  }
}
```

-----------------------------
### operatoration name
+ the keyword query as operation type and HeroNameAndFriends as operation name
+ The operation type **is required** 
+ **unless** you're using the query shorthand syntax, in which case you can't supply a name or variable definitions for your operation.
+ its use **is encouraged** because it is very helpful for debugging and server-side logging. 
+ 
#### query example
```python
query HeroNameAndFriends {
  hero {
    name
    friends {
      name
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
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```

-----------------------------
### variables 
+ pass these dynamic arguments directly in the query string
+ Replace the static value in the query with $variableName
+ Declare $variableName as one of the variables accepted by the query
+ Pass variableName: value in the separate, transport-specific (usually JSON) variables dictionary

#### query example
```python
query HeroNameAndFriends($episode: Episode) {
  hero(episode: $episode) {
    name
    friends {
      name
    }
  }
}

{
  "episode": "JEDI"
}
```

#### query result
```python
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```

-----------------------------
### Variable definitions
+ All declared variables must be either scalars, enums, or input object types


#### Default variables
```python
query HeroNameAndFriends($episode: Episode = JEDI) {
  hero(episode: $episode) {
    name
    friends {
      name
    }
  }
}
```

-----------------------------
### Directives
+ withFriends can not be none
+ dynamically change the structure and shape of our queries using variables
+ `@include(if: Boolean)` Only include this field in the result if the argument is true.
+ `@skip(if: Boolean)` Skip this field if the argument is true.

#### query example
```python
query Hero($episode: Episode, $withFriends: Boolean!) {
  hero(episode: $episode) {
    name
    friends @include(if: $withFriends) {
      name
    }
  }
}
{
  "episode": "JEDI",
  "withFriends": false
}
```

#### query result(withFriends is false)
```python
{
  "data": {
    "hero": {
      "name": "R2-D2"
    }
  }
}
```

#### query result(withFriends is true)
```python
{
  "data": {
    "hero": {
      "name": "R2-D2",
      "friends": [
        {
          "name": "Luke Skywalker"
        },
        {
          "name": "Han Solo"
        },
        {
          "name": "Leia Organa"
        }
      ]
    }
  }
}
```

-----------------------------
### Mutations
+ any operations that cause writes should be sent explicitly via a mutation.

#### query example
```python
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
  createReview(episode: $ep, review: $review) {
    stars
    commentary
  }
}
{
  "ep": "JEDI"
  "review": {
    "stars": 7,
    "commentary": "This is a great movie!"
  }
}
```

#### query result
```python
{
  "data": {
    "createReview": {
      "stars": 7,
      "commentary": "This is a great movie!"
    }
  }
}
```

##### Multiple fields in mutations
+ While query fields are executed in parallel, mutation fields run in series

-----------------------------
### Inline Fragments
+ If you are querying a field that returns an interface or a union type, you will need to use inline fragments to access data on the underlying concrete type
+ the first fragment is labeled as `... on Droid`, the `primaryFunction` field will only be executed if the Character returned from hero is of the Droid type. 

#### query example
```python
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    ... on Droid {
      primaryFunction
    }
    ... on Human {
      height
    }
  }
}
{
  "ep": "JEDI"
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

-----------------------------
### Meta fields
+ GraphQL allows you to request __typename, a meta field, at any point in a query to get the name of the object type at that point.

#### query example
```python
{
  search(text: "an") {
    __typename
    ... on Human {
      name
    }
    ... on Droid {
      name
    }
    ... on Starship {
      name
    }
  }
}
```

#### query result
```python
{
  "data": {
    "search": [
      {
        "__typename": "Human",
        "name": "Han Solo"
      },
      {
        "__typename": "Human",
        "name": "Leia Organa"
      },
      {
        "__typename": "Starship",
        "name": "TIE Advanced x1"
      }
    ]
  }
}
```