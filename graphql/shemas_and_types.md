# Schemas and Types

**it describes what data can be queried**
[TOC]

### Object types and fields

#### query example
```python
type Character {
  name: String!
  appearsIn: [Episode!]!
}
```

+ `Character` is a GraphQL Object Type, meaning it's a type with some fields.
+ `name` and `appearsIn` are fields on the Character type.
+ `String!` means that the field is non-nullable, meaning that the GraphQL service promises to always give you a value when you query this field.
+ `[Episode!]!` represents an array of Episode objects. it is also non-nullable. 

-----------------------------
### Arguments

#### query example
```python
type Starship {
  id: ID!
  name: String!
  length(unit: LengthUnit = METER): Float
}
```

##### All arguments are named.
    the length field has one defined argument, unit.
##### can define a default value
    if the unit argument is not passed, it will be set to METER by default.

-----------------------------
### The Query and Mutation types

#### query example
```python
schema {
  query: Query
  mutation: Mutation
}
```

##### very GraphQL service has a query type and **may or may not** have a `mutation` type.

#### query example
```python
query {
  hero {
    name
  }
  droid(id: "2000") {
    name
  }
}
```
##### That means that the GraphQL service needs to have a Query type with hero and droid fields

#### query example
```python
type Query {
  hero(episode: Episode): Character
  droid(id: ID!): Droid
}
```

-----------------------------
### Scalar types(标量类型)

#### GraphQL comes with a set of default scalar types out of the box:
+ `Int`: A signed 32‐bit integer.
+ `Float`: A signed double-precision floating-point value.
+ `String`: A UTF‐8 character sequence.
+ `Boolean`: true or false.
+ `ID`: The ID scalar type represents a unique identifier, often used to refetch an object or as the key for a cache.

#### specify custom scalar types
+ `scalar Date`

-----------------------------
### Enumeration types
    enumeration types are a special kind of scalar that is restricted to a particular set of allowed values

#### query example
```python
enum Episode {
  NEWHOPE
  EMPIRE
  JEDI
}
```

-----------------------------
### Lists and Non-Null

#### type example
```python
type Character {
  name: String!
  appearsIn: [Episode]!
}
```

#### query example
```python
query DroidById($id: ID!) {
  droid(id: $id) {
    name
  }
}
{
  "id": null
}
```

#### query result
```python
{
  "errors": [
    {
      "message": "Variable \"$id\" of required type \"ID!\" was not provided.",
      "locations": [
        {
          "line": 1,
          "column": 17
        }
      ]
    }
  ]
}
```

##### myField: [String!]
+ myField: null // valid
+ myField: [] // valid
+ myField: ['a', 'b'] // valid
+ myField: ['a', null, 'b'] // error

##### myField: [String]!
+ myField: null // error
+ myField: [] // valid
+ myField: ['a', 'b'] // valid
+ myField: ['a', null, 'b'] // valid

-----------------------------
### Interfaces

#### query example
```python
interface Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
}
```
#### query example
```python
type Human implements Character {
  id: ID!
  name: String!
  friends: [Character]
  appearsIn: [Episode]!
  starships: [Starship]
  totalCredits: Int
}
```

#### query example
```python
query HeroForEpisode($ep: Episode!) {
  hero(episode: $ep) {
    name
    primaryFunction
  }
}
{
  "ep": "JEDI"
}
```

#### query result
```python
{
  "errors": [
    {
      "message": "Cannot query field \"primaryFunction\" on type \"Character\". Did you mean to use an inline fragment on \"Droid\"?",
      "locations": [
        {
          "line": 4,
          "column": 5
        }
      ]
    }
  ]
}
```

-----------------------------
### Union types
+ `union SearchResult = Human | Droid | Starship`

#### query example
```python
{
  search(text: "an") {
    __typename
    ... on Human {
      name
      height
    }
    ... on Droid {
      name
      primaryFunction
    }
    ... on Starship {
      name
      length
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
        "name": "Han Solo",
        "height": 1.8
      },
      {
        "__typename": "Human",
        "name": "Leia Organa",
        "height": 1.5
      },
      {
        "__typename": "Starship",
        "name": "TIE Advanced x1",
        "length": 9.2
      }
    ]
  }
}
```

-----------------------------
### Input types

#### query example
```python
input ReviewInput {
  stars: Int!
  commentary: String
}
```

#### query example
```python
mutation CreateReviewForEpisode($ep: Episode!, $review: ReviewInput!) {
  createReview(episode: $ep, review: $review) {
    stars
    commentary
  }
}
```

#### query result
```python
{
  "data": {
    "createReview": {
      "stars": 5,
      "commentary": "This is a great movie!"
    }
  }
}
```
s