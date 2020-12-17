# Elasticsearch2.x 权威文档 （摘抄）

很多用法都已经过时，看完这个我打算再看一下 7.x。仅作为快速查阅的工具文档使用，可能不会和原文一致。希望尽量做到精简。

## 面向文档

Elasticsearch 是 *面向文档*  的，意味着它存储整个对象或文档，Elasticsearch 不仅存储文档，而且 *索引* 每个文档的内容，使之可以被检索。在 Elasticsearch 中，我们对文档(而不是对行列数据)进行索引、检索、排序、过滤，这也是 Elasticsearch 能支持复杂全文检索的原因。

## JSON

Elasticsearch 使用 JavaScript Object Notation (JSON) 作为文档的序列化格式。具体可以看 serialization 和 marshalling 两个处理模块。

## 几个名词

+ 索引 .n
  + 一个索引类似于一个数据库，是一个存储文档的地方。
+ 索引 .v
  + 索引一个文档就是存储一个文档到一个索引中以便于被检索或是被查询。类似于 insert, 当文档已存在时(_id已有) 会进行更新。
+ 倒排索引
  + 倒排索引被作用在文档上，以便于提升数据的检索速度。默认的，文档中的每一列都有倒排索引，没有倒排索引的属性是不可能被搜索到的。

## 检索文档

+ *GET* - **/index/mapping/id** 即可检索出 ID 对应的对象

* *GET* - **/index/mapping/_search** 用于检索所有的对象(一个搜索默认返回十条结果, 放在 hits 中)

+ *GET* - **/index/mapping/_search?q=alst_name:Smith** -- URL 查询参数查询

+ *GET* - **/index/mapping/_search** -- 进行查询表达式搜索(部分匹配)

```json
{
  "query": {
    "match": {
      "last_name": "Smith"
    }
  }
}
```

+ *GET* - **/index/,apping/_search** -- 组合过滤查询

```json
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "last_name": "smith"
        }
      },
      "filter": {
        "range": {
          "age": {"gt": 30}
        }
      }
    }
  }
}
```

+ *GET* - **/index/mapping/_search** -- 全文搜索

```json
{
  "query": {
    "match": {
      "about": "rock climbing"
    }
  }
}
```

Elasticsearch 默认按照相关性得分来进行排序，即每个文档跟查询的匹配程度。而且上面这个查询甚至会把只有 rock, 没有 climbing 的也匹配出来。**这是完全区别于传统关系型数据库的一个概念，一条记录并不是要么全匹配，要么全不匹配，es 是部分匹配。**

+ *GET* - **/index/mapping/_search** -- 短语搜索

**精确匹配一系列的单词或者短语**，可以使用 **match_phrase** 

```json
{
  "query": {
    "match_phrase": {
      "about": "rock climbing"
    }
  }
}
```

+ *GET* - **/index/mapping/_search** -- 高亮搜索

```json
{
  "query": {
    "match_phrase": {
      "about": "rock climbing
    },
    "highlight": {
      "fields": {
        "about": {}
     	}
    }
  }
}
```

返回的结果 hits 里会包含一个 highlight 的部分，这个部分包含了 about 属性匹配的文本片段，并且会以 `<em></em>`标签进行封装。

+ *GET* - **/index/mapping/_search** -- 分析聚合

```json
-- 结果返回所有人中受欢迎的兴趣爱好排行
{
  "aggs": {
    "all_interests": {
      "terms": {"field": "interests"}
    }
  }
}
```

```json
-- 支持 last_name 是 smith 的人中，排出最受欢迎的兴趣
{
  "query": {
    "match": {
      "last_name": "smith"
    }
  },
  "aggs": {
    "all_interests": {
      "terms": {"field": "interests"}
    }
  }
}
```

```json
{
  "aggs": {
    "all_interests": {
      "terms": {"field": "interests"},
      "aggs": {
        "avg_age": {
          "avg": {"field": "age"}
        }
      }
    }
  }
}
```

输出的依旧是一个兴趣及数量的列表，只不过每个兴趣都有了一个附加的 avg_age 的属性，代表了有这个兴趣爱好的所有员工的平均年龄。

## 分布式特性

Elasticsearch 可以横向扩展至数百甚至数千的服务器节点，同时可以处理 PB 级别的数据，Elasticsearch 天生就是分布式的，并且在设计时屏蔽了分布式的复杂性。Elasticsearch 尽可能地屏蔽了分布式系统的复杂性，这里列举了一些在后台自动执行的操作。

+ 分配文档到不同的 容器/分片 中，文档可以存储在一个或多个节点中。
+ 按集群节点来均衡分配这些分片，从而对索引和搜索过程中进行负载均衡。
+ 复制每个分片以支持数据冗余，防止硬件故障导致的数据缺失。
+ 将集群中的任一节点的请求路由到存有相关数据的节点。
+ 集群扩容时无缝整合新节点，重新分配分片以便从离群节点回复。

## 集群内的原理

**Elasticsearch 的主旨是随时可用和按需扩容。**而扩容可以通过购买性能更强大或者数量更多的服务器来进行实现(有横向扩容和纵向扩容)。

### 空集群

如果我们启动了一个单独的节点，里面不包含任何的数据和索引，那我们的集群看起来就是一个 Figure1.包含空内容节点的集群。

一个运行中的 Elasticsearch 实例称为一个节点，而集群是由一个或者多个拥有相同 `cluster.name` 配置的节点组成，它们共同承担数据和复杂的压力。当有节点加入到集群中，或者从集群中移除节点时，集群将会重新平均分布所有的数据。

当一个节点被选举为主节点时，它将负责管理集群范围内的所有变更，例如增加、删除索引，或者增加、删除节点等。而**主节点并不需要涉及到文档级别的变更和搜索等操作**，所以当集群只拥有一个主节点的情况下，即使流量的增加它也不会成为瓶颈。任何节点都可以成为主节点。（疑惑的表述，只有一个主节点的话那................ 谁查找文档啊？）

作为用户，我们可以将请求发送到集群中的任何节点，包括主节点。每个节点都知道任意文档所处的位置，并且能够将我们的请求直接转发到存储我们所需文档的节点。**无论我们将请求发送到哪个节点，它都能负责从各个包含我们所需文档的节点收集回数据，并将最后的结果返回给客户端。**

### 集群健康

*GET* - **_cluster/health**

Elasticsearch 的集群监控信息中包含了许多的统计数据，其中最重要的一项就是 **集群健康**。它在 status 字段中展示为 `green` `yellow` `red`。内容类似于。

```json
{
   "cluster_name":          "elasticsearch",
   "status":                "green", 
   "timed_out":             false,
   "number_of_nodes":       1,
   "number_of_data_nodes":  1,
   "active_primary_shards": 0,
   "active_shards":         0,
   "relocating_shards":     0,
   "initializing_shards":   0,
   "unassigned_shards":     0
}
```

+ **green** 所有的主分片和副本分片都正常运行
+ **yellow** 所有的主分片都正常运行，但不是所有的副本分片都正常运行
+ **red** 有主分片没有正常运行

### 添加索引

**索引**实际上是指向**一个或者多个物理分片**的**逻辑命名空间**。

**一个分片是一个底层的工作单元**，它仅保存了全部数据中的一部分。我们的文档被存储和索引到分片内，但是**应用程序是直接与索引(而不是分片)进行交互**。Elasticsearch 是利用分片将数据分发到集群内各处的。分片是数据的容器，文档保存在分片内，分片又被分配到集群内的各个节点里，当你的集群规模扩大或者缩小时，Elasticsearch 会自动的在各个节点中迁移分片，使得数据能均匀地分配在集群里。

**分片又分为主分片和副本分片**，索引内任意一个文档都归属于一个主分片，所以**主分片的数目决定着索引能够保存的最大数据量**。技术上来说，一个主分片最大能够存储 128 个文档。实际的最大值还要看使用场景、硬件、文档的大小和复杂程度等。

**副本分片只是主分片的拷贝，作为硬件故障时保护数据不丢失的冗余备份，并为搜索和返回文档等读操作提供服务。**

**在索引建立的时候就已经确定了主分片数，但是副本分片数可以随时更改。**

*PUT* - **/blogs**

```json
{
   "settings" : {
      "number_of_shards" : 3,
      "number_of_replicas" : 1
   }
}
```

上述操作会在  *Figure1.包含空内容节点的集群* 中创建一个名为 blog 的索引，索引在默认情况下会被分配 5个 主分片，代码里时分配了 3个 主分片，以及每个主分片都会有一个副本分片。现在变为了 *Figure 2.拥有一个索引的单节点集群*。

```json
-- 集群健康如下
{
  "cluster_name": "elasticsearch",
  "status": "yellow", 
  "timed_out": false,
  "number_of_nodes": 1,
  "number_of_data_nodes": 1,
  "active_primary_shards": 3,
  "active_shards": 3,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 3,   # 没有被分配到任何节点的副本数，因为在同一个节点上同时保存主分片和副本分片时没有意义的
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 50
}
```

### 添加故障转移

当集群中只有一个节点在运行时，意味着会有一个单点故障的问题。只需要再加一个节点就可以防止数据丢失。

**在同一台机器上启动多个节点时**, 只需要将新节点的 cluster.name 配置为和第一个节点相同的，他就会发现集群并自动加入其中。

**在不同机器上启动多个节点时**, 为了加入到同一集群，你需要配置一个可连接到的[单播主机列表](https://www.elastic.co/guide/cn/elasticsearch/guide/current/important-configuration-changes.html#unicast).如果启动了第二个节点，就会从 *Figure 2.拥有一个索引的单节点集群* 变为 *Figure 3.拥有两个节点的集群——所有主分片和副本分片都已被分配*。副本分片都会放在第二个节点上。

所有新近被索引的文档都会保存在主分片上，然后被并行地复制到对应的副本分片上，这就保证我们既可以从主分片又可以从副本分分片上获取文档。

```json
{
  "cluster_name": "elasticsearch",
  "status": "green", 
  "timed_out": false,
  "number_of_nodes": 2,
  "number_of_data_nodes": 2,
  "active_primary_shards": 3,
  "active_shards": 6,
  "relocating_shards": 0,
  "initializing_shards": 0,
  "unassigned_shards": 0,
  "delayed_unassigned_shards": 0,
  "number_of_pending_tasks": 0,
  "number_of_in_flight_fetch": 0,
  "task_max_waiting_in_queue_millis": 0,
  "active_shards_percent_as_number": 100
}
```

## 水平扩容

当启动了第三个节点，就会从 *Figure 3.拥有两个节点的集群——所有主分片和副本分片都已被分配*  变为 *Figure 4.拥有三个节点的集群——为了分散负载而对分片进行重新分配*。

Node1 和 Node2 上各有一个分片被迁移到了新的 Node3 节点，现在每个节点都拥有两个分片，而不是之前的三个。这表示每个节点的硬件资源将被更少的分片所共享，每个分片的性能将会得到提升。

**分片是一个功能完整的搜索引擎，**它拥有使用一个节点上所有资源的能力。我们现在有6个分片，三主三副，可以最大扩容到六个节点。让每个分片都拥有所在节点的全部资源。

#### 更多的扩容

如果想要扩容超过6个节点。

主分片的数目其实在索引创建时就已经确定下来了，这个数目也决定了这个索引能够存储的最大数据量。但是，**读操作-搜索和返回数据-可以同时被主分片和副本分片所处理。所以当你拥有越多的副本分片时，意味着你可以有更大的吞吐量**。

在运行的集群上**可以动态调整副本分片的数目**。如

*PUT* - **/blogs/_settings**

```json
{
  "number_of_replicas": 2
}
```

*Figure 5.将参数 `number_of_replicas` 调大到 2*  一共有三个节点，有9个分片，3个主分片，6个副本分片，都会被均匀地分配在三个节点上。**当然如果在相同节点数目的集群上增加更多的副本分片并不能提升性能，**因为每个分片从节点上获得的资源会变上，因此你需要增加更多的硬件资源来提升吞吐量。在上面的配置下，我们即使失去两个节点也不会丢失任何数据。

## 应对故障

*Figure 6. 关闭了一个节点后的集群* 可以尝试一下关闭一个节点(Node1)，模仿某个节点出现故障的场景。

此时发生的第一件事情就是：重新选举一个新节点：Node2。

Node1 上有两个主分片1，2，并且在缺失主分片的时候索引是不能正常工作的。如果此时检查集群的状况，我们看到的状态是 red。还好在其它节点上存在着两个主分片的完整副本，所以新的节点会立即将这些分片在 Node2 和 Node3 上的副分片提升为主分片，此时集群的状态会变为 yellow。

这时虽然拥有了三个主分片，但是同时设置了每个主分片对应的是两个副本分片，此时却只有一个副本了。所以集群仍是 yellow 状态，如果重新启动 Node1, 则集群可以将缺失的副本分片再次进行分配。等...

## 数据的输入和输出

无论我们写什么样的程序，目的都是一样的：以某种方式组织数据已达到服务我们自己的目的。

一个 *对象* 是基于特定语言的内存的数据结构。为了通过网络发送或者存储它，我们需要将它表示成某种标准的格式。 [JSON](http://en.wikipedia.org/wiki/Json) 是一种以人可读的文本表示对象的方法。 它已经变成 NoSQL 世界交换数据的事实标准。当一个对象被序列化成为 JSON，它被称为一个 *JSON 文档* .

Elastcisearch 是分布式的 *文档* 存储。它能存储和检索复杂的数据结构—序列化成为JSON文档—以 *实时* 的方式。 换句话说，一旦一个文档被存储在 Elasticsearch 中，它就是可以被集群中的任意节点检索到。

在 Elasticsearch 中， *每个字段的所有数据* 都是 *默认被索引的* 。 即每个字段都有为了快速检索设置的专用倒排索引。而且，不像其他多数的数据库，它能在 *同一个查询中* 使用所有这些倒排索引，并以惊人的速度返回结果。

## 什么是文档？

通常情况下，我们使用的术语 **对象** 和 **文档** 是可以互相替换的。不过对象仅仅是类似于 hash、hashmap、字典、关联数组的 JSON 对象。对象可以嵌套对象。而在 Elasticsearch 中，**文档** 有额外的含义，是指最顶层或者根对象，这个根对象被序列化成 JSON 并存储到了 Elasticsearch 中，且给指定了唯一的 ID。

**字段的名字可以是任何合法的字符串，但是不可以包含 半角句号**

## 文档元数据

元数据 -- 有关文档的信息。三个必须的元数据元素如下：

**_index**: 文档在哪里存放。也就是索引名称

**_type**: 文档表示的对象类别

**_id**: 文档的唯一标识

### _index

数据被存储和索引在分片中，而一个索引仅仅是逻辑上的命名空间。这个命名空间是一个或者多个分片组成的。**索引名必须小写，并且不能以下划线开头，不能包含逗号。**指定索引名，Elasticsearch 会帮我们创建索引。

### _type

对索引中的数据进行逻辑分区，不同的 types 文档可能有不同的字段，但是最好能够非常相似。**一个 _type 的命名不限大小写，不能以下划线或者句号开头，不应该包含逗号，长度限制为 256 个字符。**

### _id

ID 是一个字符串，当它和 _index 以及 _type 组合，就可以唯一确定一个文档。当你创建文档时(创建一条数据)，要么你自己提供 _id, 要么 Elasticsearch 会帮你自动生成。

## 索引文档

### 使用自定义的ID

*PUT* - **/index/type/id** 

```json
{
  "field": "value",
  ....
}
```

可以往 ES 中插入一条文档。在 ES 中每一条文档都有一个版本号，当每次对文档进行修改时(包括删除)，_version 的值都会递增。这可以确保你的应用程序中的一部分修改不会覆盖另一部分所做的修改。

### Autogenerating IDs

如果你的数据没有自定义ID，ES 会这帮你自动生成，请求的时候则改 `PUT` 为`POST`

*POST* - **/index/type/**

```json
{
  "field": "value",
  ...
}
```

自动生成的 ID 是 URL-safe 的。基于 base64 编码，且长度为 20 个字符的 GUID 字符串。这些 GUID 字符串由可修改的 FakeID 模式生成，这种模式允许多个节点并行生成唯一 ID，且相互之间的冲突概率几乎为0。

## 取回一个文档

*GET* - **/index/type/id?pretty**

+ 在查询参数中加上 `pretty` 参数，是的 JSON 响应体更加可读。
+ `curl -i -XGET http://localhost:9200/website/blog/124?pretty` 可以显示响应头部, 就像下面这样

```json
HTTP/1.1 404 Not Found
Content-Type: application/json; charset=UTF-8
Content-Length: 83

{
  "_index" : "website",
  "_type" :  "blog",
  "_id" :    "124",
  "found" :  false
}
```

响应体中的 `_source` 字段包含我们索引数据时(分区)发送给 Elasticsearch 的原始 JSON 文档。

### 返回文档的部分

*GET* - **/index/type/id?_source=title,text**

+ 返回的 `_source` 字段中只包含 title 和 text 两个字段的内容， 如果不需要其它元数据，则只用 `...?_source` 即可。

```json
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 1,
  "found" :   true,
  "_source" : {
      "title": "My first blog entry" ,
      "text":  "Just trying this out..."
  }
}
```

## 检查文档是否存在

*HEAD* - **/index/type/id**

+ `curl -i -XHEAD http://localhost:9200/website/blog/123`

```json
# 如果文档存在，只会返回 200 的 http code， 否则返回 404
HTTP/1.1 200 OK
Content-Type: text/plain; charset=UTF-8
Content-Length: 0
```

当然一个文档仅仅在检查的时候不存在，并不意味着它在一毫秒之后也不存在。要注意多进程的考虑。

## 更新整个文档

在 Elasticsearch 中文档是 **不可被改变** 的。如果想要更新现有文档，需要*重建索引*，或者进行 *文档替换*。

*PUT* - **/index/type/id**

```json
{
  "title": "My first blog entry",
  "text":  "I am starting to get the hang of this...",
  "date":  "2014/01/02"
}
```

```json
{
  "_index" :   "website",
  "_type" :    "blog",
  "_id" :      "123",
  "_version" : 2,   # 注意此时的 _version 为 2
  "created":   false   # 为 false 是因为相同的索引、类型 和 ID 的文档都已经存在了
}
```

在内部，Elasticsearch 已将就文档标记为删除，并增加一个全新的文档。它不会立即消失，当继续索引更多的数据，Elasticsearch 会在**后台清理这些已经删除的文档**。

+ 从旧文档创建 json
+ 更改该 json
+ 删除旧文档
+ 索引一个新文档

## 创建新文档

创建新文档只需要确定 (_index, _type, _id) 是唯一的即可。否则覆盖现有文档。可以用 ES 自生成的 ID

+ *POST* - **/index/type/**

如果已经有了自己的 _id, 则必须告诉 Elasticsearch, 只有当 pk 不存在时，才接受我们的请求。

+ *PUT* - **/index/type/id?op_type=create**
+ *PUT* - **/index/type/id/_create**
+ 如果请求成功会返回 201 created 的 http code, 如果返回的是 409 conflict, 则代表该文档已存在

## 删除文档

*DELETE* - **/index/type/id**

+ 成功返回 200，且响应体中 _version=3
+ 失败返回 404，且响应体中 _version=4

不管文档是否存在，_version 值仍然会增加，这是 Elasticsearch 内部记录的一部分，用来确保 这些改变 在跨多节点时能够被以正确的顺序执行。还是和前文一样，删除请求之后数据并不会被马上删除，而是要不断进行索引数据之后，ES 才会在后台进行删除数据。

## 处理冲突

当我们使用 API 进行更新文档，可以一次性读取文档，做出修改，然后重新索引文档。最近的索引请求将获胜：无论哪一个文档被索引，都将被唯一存储在 Elasticsearch 中，如果其他人同时更改这个文档，他们的更改将会丢失。

 在数据库领域中，通常有两种方法被用来确保并发更新时的更新不丢失：

+ **悲观并发控制**

  这种方法被关系型数据库广泛使用，它假定有变更冲突可能发生，因此阻塞访问资源以防止冲突。一个典型的例子就是读取一行数据之前先将其锁住，确保只有放置锁的线程能够对这行数据进行修改。

+ **乐观并发控制**

  Elasticsearch 中假定冲突时不可能发生的，并且不会阻塞正在尝试的操作。然而，如果源数据在读写当中被修改，更新将会失败。应用程序接下来将决定该如何解决冲突。例如，可以重试更新、使用更新后的数据、将相关情况报告给客户等。

## 乐观并发控制

前文知道 es 是分布式的，当插入、更新或删除时，所有的操作都要被同步到集群中的其它节点中(其实是要复制到其它的副本分片中)。es 是 **异步** 和 **并发** 的。这意味着所有的复制请求都是并行发送的，并且到达目的地时也许 **顺序是乱的**。也就是说，可能就出现旧文档覆盖新文档的现象。

每个文档都是有 `_version` 号的，当文档被修改时，`_version` 号是递增的，所以如果旧文档在新文档之后到达分片，就可以被简单地忽略。也就是说，当 `_version=1` 的文档存在时，我们做了某个操作，这时该文档的版本号变为2， 假如我们再想操作 `_version=1` 的文档时，es 返回 409, 提示修改失败。

我们现在可以告诉用户，其他人已经修改了文档，并且在再次保存之前检查这些需要进行修改的内容，所有文档更新或删除文档的 API, 都可以接受 `version` 参数，这与许你在代码中使用乐观的并发控制，且这是一种明确的做法。

## 通过外部系统使用版本控制

场景：使用其它数据库作为主数据存储，使用 es 做数据检索，也就是说主数据所有的更改都需要向 es 进行同步，如果有多个进程在进行这一操作，也会出现之前提过的问题。如果你的主数据库已经有了 **唯一版本号** 或者 **一个能作为版本号的字段值，如 timestamp** 那么你就可以在 es 中通过增加 `version_type=external` 到查询字符串的方式来重用这些相同的版本号，版本号必须是大于0的整数，且小雨 9.2E+18。

创建一个新的具有外部本本好 5 的博客文章

*PUT* - **/website/blog/2?version=5&version_type=external**

```json
{
  "title": "just be confidence",
  "text": "just be confidence to acai"
}
```

现在更新这个文档，指定 `_version=10`

*PUT* - **/website/blog/2?version=10&version_type=external**

```json
{
  "title": "just be happy",
  "text": "just be happy acai"
}
```

## 文档的部分更新

update API 将 `检索-修改-重建` 的过程隐藏在了分片内部，这样可以减少多次网络请求产生的开销，通过减少检索和重建索引步骤之间的时间，我们也减少了其他进程的变更产生的冲突的可能性。

`update` 请求最简单的一种形式就是接收文档的一部分作为 doc 的参数，它只是与现有的文档进行合并。对象被合并到一起，覆盖现有的字段，增加新字段。

*POST* - **/wensite/blog/1/_update**

```json
{
  "doc": {
    "tags": ["testing"],
    "views": 0
  }
}
```

```json
{
   "_index":    "website",
   "_type":     "blog",
   "_id":       "1",
   "_version":  3,  // 我猜是新建，然后修改，所以这里才是 3
   "found":     true,
   "_source": {
      "title":  "My first blog entry",
      "text":   "Starting to get the hang of this...",
      "tags": [ "testing" ], 
      "views":  0 
   }
}
```

### 使用脚本进行文档的部分更新

*POST* - **/website/blog/1/_update**

```json
// _source 在更新脚本中成为 ctx._source
{
  "script": "ctx._source.views+=1"
}
```

**es 默认的脚本语言是 Groovy, es 1.3.0 中被首次引入并运行于沙盒中，然而 Groovy 脚本引擎中存在漏洞，允许攻击者通过构建 Groovy 脚本，在 es Java VM 运行时脱离沙盒并且执行 shell 命令，因为在更高版本中，它被默认为禁用**

指定新的标签作为参数，而不是硬编码到脚本内部，这使得每次我们想添加标签时都要对新脚本重新编译。

*POST* - **/website/blog/1/_update** 

```json
{
  "script": "ctx._source.tags+=new_tag",
  "params": {
    "new_tag": "search"
  }
}
```

我们甚至可以通过设置 `ctx.op` 来删除基于其内容的文档

*POST* - **/website/blog/1/_update**

```json
{
  "script": "ctx.op = ctx._source.views == count ? 'delete' : 'none'",
  "params": {
    "count": 1
  }
}
```

### 更新的文档可能尚不存在

*POST* - **/website/pageviews/1/_update**

```json
{
  "script": "ctx._source.views+=1",
  "params": {
    "views": 1
  }
}
```

我们第一次运行这个请求时，`upsert` 作为新文档被索引，初始化 `views=1`, 在后续运行中， 由于文档已存在，则 script 更新操作将替代 upsert 进行应用。

### 更新和冲突

对于部分更新的很多使用场景，文档已经被改变了也没有关系。如多个进程对页面访问计数器进行递增操作，他们发生的先后顺序其实不重要，如果冲突发生了，我们唯一需要做的就是尝试再更新。我们可以通过设置参数 `retry_on_conflic` 来规定失败之前 update 应该重试的次数，默认值为 0。

*POST* - **/website/pageviews/1/_update?retry_on_conflict=5**

```json
// 失败之前重试该更新 5 次
{
 	"script": "ctx._source.views+=1",
  "upsert": {
    "views": 0
  }
}
```

在增量操作无关顺序的场景，使用这个方法很有效。

## 取回多个文档

**es 可以将多个请求合并为一个，避免单独处理每个请求花费的网络延迟和开销。** 如果你需要从 es 检索很多文档，那么使用 `multi-get` 或者 `mget` API 来将这些检索请求放在一个请求中，将比朱哥文档请求更快地检索到全部文档。

`mget` API 要求有一个 `docs` 数组作为参数，每个元素包含需要检索文档的元数据，包括 `_index`、`_type`、`_id` 。如果你想检索一个或者多个特定的字段，你可以通过 `_source` 来指定这些参数的名字。

*GET* - **/_mget**

```json
// docs 数组里的顺序和请求的顺序是相同的，其中的每一个响应都和使用单个 get request 请求得到的相应体相同。
{
  "docs": [
    {
      "_index": "website",
      "_type": "blog",
      "_id": 2
    },
    {
      "_index": "website",
      "_type": "pageviews",
      "_id": 1,
      "_source": "views"
    }
  ]
}
```

```json
{
   "docs" : [
      {
         "_index" :   "website",
         "_id" :      "2",
         "_type" :    "blog",
         "found" :    true,
         "_source" : {
            "text" :  "This is a piece of cake...",
            "title" : "My first external blog entry"
         },
         "_version" : 10
      },
      {
         "_index" :   "website",
         "_id" :      "1",
         "_type" :    "pageviews",
         "found" :    true,
         "_version" : 2,
         "_source" : {
            "views" : 2
         }
      }
   ]
}
```

如果想检索的数据在相同的 `_index` 中，甚至在相同的 `_type` 中，则可以在 URL 中指定 `/_index` 或者 `/_index/_type`

*GET* - **/website/blog/_mget**

```json
{
  "docs": [
    {"_id": 2},
    {"_type": "pageviews", "_id": 1}
  ]
}
```

or

```json
{
  "ids": ["2", "1"]
}
```

## 代价较小的批量操作

`bulk` API 允许在单个步骤中进行多次 `create`、`index`、`update`、`delete` 请求。如果你需要索引一个数据流，比如日志时间，它可以排队和索引数百或者数千批次。

```json
{action: {metadata}} \n   // 指定 哪一个文档 做 什么操作
{request body} \n         
{action: {metadata}} \n
{request body} \n
```

这种格式类似一个有效的单行 JSON 文档流，可以通过换行符连接到一起。

+ 一定要以换行符结尾，包括最后一行
+ 不能包含未转义的换行符，他们会对解析造成干扰，也意味着这个 JSON 不能用 pretty 参数进行打印

`action` 必须是下列选项之一

+ `create` 如果文档不在就创建它
+ `index` 创建一个新文档或者替换一个现有的文档
+ `update` 部分更新一个文档
+ `delete` 删除一个文档

```json
{"create": {"_index": "website", "_type": "blog", "_id": "123"}} \n
{"title": "My first blog post"} \n
```

一个完整的 `bulk` 请求由如下形式：

*POST* - **/bulk**

```json
{"delete": {"_index": "website", "_type": "blog", "_id": "123"}} \n    // delete 后面不能有请求体 只能跟另一个动作
{"create": {"_index": "website", "_type": "blog", "_id": "123"}} \n
{"title": "My first blog post"} \n
{"index": {"_index": "website", "_type": "blog"}} \n
{"title": "My second blog post"} \n
{"update": {"_index": "website", "_type": "blog", "_id": "123", "_retry_on_conflict": 3}} \n
{"doc": {"title": "My updated blog post"}} \n
```

```json
{
   "took": 4,
   "errors": false, 
   "items": [
      {  "delete": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 2,
            "status":   200,
            "found":    true
      }},
      {  "create": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 3,
            "status":   201
      }},
      {  "create": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "EiwfApScQiiy7TIKFxRCTw",
            "_version": 1,
            "status":   201
      }},
      {  "update": {
            "_index":   "website",
            "_type":    "blog",
            "_id":      "123",
            "_version": 4,
            "status":   200
      }}
   ]
}
```

每个子请求都是独立执行，因此某个子请求的失败不会对其他子请求的成功与否造成影响。如果其中任何子请求失败，最顶层的 error 标志都会设置为 true, 并且在响应的请求报告中给出错误明细。但是这也意味着 `bulk` 请求不是原子的，不能用它来实现事务控制。

### 不要重复指定 index 和 type

为每一个文档指定相同的元数据是一种浪费，建议在 URL 中指定默认的 `_index` 和 `_type`。

*POST* - **/website/_bulk**

```json
{"index": {"_type": "blog"}} \n
{"event": "User logged in"} \n
```

*POST* - **/website/log/_bulk**

```json
{"index": {}} \n
{"event": "User logged in"} \n
{"index": {"_type": "blog"}} \n
{"title": "Overriding the default type"} \n
```

### 多大是太大了？

整个批量请求都需要由接收到请求的节点加载到内存中，因此该请求越大，其他请求所能获得的内存就越少。批量请求的大小有一个最佳值，大于这个值，性能就不再提升，甚至会下降。

找到这个点的最好方法就是，通过批量索引典型文档，不断增加批量大小进行测试，当性能开始下降即为0点。最好是 1000 到 5000 个文档作为一个单位进行批量尝试。一个好的批量大小在开始处理后所占用的无力大小约为 5-15 MB。



















































































