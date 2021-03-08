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

+ *GET* - **/index/mapping/_search** -- 组合过滤查询

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

**在同一台机器上启动多个节点时**, 只需要将新节点的 **cluster.name** 配置为和第一个节点相同的，他就会发现集群并**自动加入其中**。

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

## 水平扩容（调整副本分片的数目）

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

## 分布式文档存储

### 路由一个文档到一个分片中

当索引一个文档时，文档会被存储到一个**主分片**中。es 通过以下公式决定文档被存储在分片1还是分片2中。

`shard = hash(routing) % number_of_primary_shards`

routing 是一个可变值，默认是文档 ID，也可以设置为一个自定义值。通过 hash() 生成一个数字，再将这个数字除以 number_of_pirmary_shards， 也就是主分片个数，去最后的余数。也就是说最后的值始终**在 0 到 主分片个数之间-1**。

**这也就解释了，为什么说主分片数量在创建索引的时候就要确定好，并且永远不会改变，如果改变了，之前路由好的值都会无效，文档也就找不到了。**

所有文档 API (get、index、delete、bulk、update、mget) 都接受一个叫做 routing 的路由参数，通过这个参数我们可以自定义文档到分片的映射。一个自定义的路由参数可以用来确保所有相关的文档都被存储到同一个分片当中。**(比如所有属于一个用户的文档存储在一个分片中)**。

### 主分片和副分片是如何交互的？

假设：一个集群有三个节点，包含一个叫做 blogs 的索引，有两个主分片，每个主分片有两个副本分片。相同分片的副本不会放在同一节点。

所以大概可以是这样的：

node1 = R0 + P1

node2 = R0 + R1

node3 = R1 + P0

我们可以把请求发送到集群中的任一节点上，每个节点都有能力处理任意的请求。因为每个节点都知道任意一个文档的位置，**为了扩展负载，更好的做法就是轮训集群中所有的节点**， 所以直接将请求转发到需要的节点上。如所有的请求发送到 node1, 我们将其称为 **协调节点(coordinating node)。**

### 新建、索引 和 删除 文档

前提：

+ Node1(master): R0、P1
+ Node2: R0、R1
+ Node3: P0、R1

上述三种都是 *写操作*， *写操作* 被要求**必须在主分片上面完成之后才能复制到相关的副本分片中**。需要经过以下**步骤**：

+ 客户端向 `Node1` 发送新建、索引或删除请求(这里并不是一定会向主节点发送请求的，任何一个节点都可以接收请求)。
+ 节点使用文档的 `_id` 确定文档属于分片 0，**请求会被转发到 `Node3`，因为分片 0 的主分片目前被分配在 `Node3` 上。**
+ `Node3` 在主分片上执行请求，如果成功了，它将请求并行转发到 `Node1` 和 `Node2` 的副本分片上，一旦所有的副本分片都报告成功，`Node3` 将向协调节点报告成功，协调节点会向客户端报告成功。(在本例中，`Node1` 就是协调节点)。

**客户端收到成功响应时，就代表文档变更已经在主分片和所有副本分片执行完成了，变更时安全的。**

*有一些可选的请求参数允许以牺牲数据安全为代价提升性能 :*

+ `consistency`

  默认设置 `True`, 即使仅仅是在试图执行一个 **写操作** 之前，主分片都会要求 **必须要有** 规定数量的分片副本(可以是主分片也可以是副本分片)处于活跃可用的状态，才会执行 **写操作**。这是为了避免在发生 网络分区故障(network partition) 的时候进行 **写操作** 将会导致 **数据不一致** 的现象。

  **规定数量计算公式：**

  `int(primary + number_of_replicas) / 2 + 1`

+ `timeout`

  如果**没有足够的副本分片**出现，es 会选择**等待**，希望更多的分片出现，最多等待 1min，可以用 `timeout` 让他更早终止。`100` (100 ms), `30s`（30s）

*新索引默认有一个 副本分片，意味着满足规定数量应该需要两个活动的分片副本，但是，这些默认的设置会阻止我们在单一节点上做任何事情。为了避免这个问题，要求只有当 number_of_replicas > 1 的时候，规定数量才会执行。*

### 取回一个文档

可以从主分片或者其它任意副本分片检索文档。

前提：

+ `Node1`(master): R0、P1
+ `Node2`: R0、R1
+ `Node3`: P0、R1

以下是从主分片或者副本分片检索文档的**步骤**：

+ 客户端向 `Node1` 发送获取请求
+ 节点使用文档的 `_id` 来确定文档属于分片 0, 分片0 的副本分片存在于所有的三个节点上。在这种情况下，它会将请求转发到 `Node2`。**转发方式是轮询转发。**
+ `Node2` 将文档返回给 `Node1`, 然后协调节点将文档返回给客户端

**在处理请求时，协调节点在每次请求的时候都会通过轮询所有的副本分片来达到负载均衡。**

在文档被检索时，已经被索引的文档可能已经存在于主分片上但是还没有复制到副本分片。在这种情况下，副本分片可能会报告文档不存在，但是主分片可能成功返回文档。**一旦索引请求成功然后返回给用户**，文档在主分片的副本分片上**都是可用的**。

### 局部更新文档

前提：

+ `Node1`(master): R0、P1
+ `Node2`: R0、R1
+ `Node3`: P0、R1

以下是部分更新一个文档的**步骤**：

+ 客户端向 `Node1` 发送更新的请求
+ 节点使用文档的 `_id` 来确定文档属于分片 0, 分片0 的副本分片存在于所有的三个节点上。在这种情况下，它会**将请求转发到主分片所在的 `Node3` 上**
+ `Node3` 从主分片检索文档，修改 `_source` 字段的 JSON，并且尝试重新索引主分片的文档。如果文档已经被另一个进程修改，它会重试步骤 3，超过 `retry_on_conflict` 次后放弃。
+ 如果 `Node3` 成功更新文档，它将新版本的文档并行转发到 `Node1` 和 `Node2` 上的副本分片，重新建立索引，一旦所有副本分片都返回成功，`Node3` 向协调节点也会返回成功，然后协调节点会向客户端返回成功。

```markdown
**基于文档的复制**：
当主分片把更改转发到副本分片上时，它不会转发更新请求。相反，它转发完整文档的新版本。这些更改将会异步转发到副本分片中，并且不能保证它们以发送它们相同的顺序到达。如果 es 仅转发更改请求，则可能以错误的顺序应用修改，导致得到损坏的文档。
```

### 多文档模式

`mget` 和 `bulk` API 模式类似于单文档模式。协调节点知道每个文档存在于哪个分片中。它将整个多文档请求分解为 `每个分片` 的多文档请求，并且将这些请求并行转发到每个参与节点。协调节点一旦收到来自每个节点的应答，会把所有节点的响应整理成一个大的响应，返回给客户端。

前提：

+ `Node1`(master): R0、P1
+ `Node2`: R0、R1
+ `Node3`: P0、R1

以下是使用单个 `mget` 请求取回多个文档所需要的步骤顺序：

+ 客户端向 `Node1` 发送 `mget` 请求
+ `Node1` 为每个分片构建多文档获取请求，然后并行转发这些请求到托管在每个所需的主分片或者副本分片的节点上。一旦收到所有的答复，`Node1` 构建响应并将其返回给客户端。

以下是使用 `bulk` 请求的步骤顺序：

+ 客户端向 `Node1` 发送 `bulk` 请求
+ `Node1` 为每个节点创建一个 `bulk` 请求，并将这些请求并行转发到每个包含主分片的节点主机
+ 主分片一个接一个按顺序执行每个操作，当每个操作成功时，主分片并行转发新的文档(或删除)到副本分片上，然后再执行下一个操作。一旦所有的副本分片报告操作成功，该节点将向协调节点报告成功，协调节点将响应整合兵返回给客户端。

**为什么 bulk API 在使用的时候要用换行符，而不是抱在 JSON 数组里？**

在批量请求中引用的每个文档可能属于**不同的主分片**。因此每个文档都有可能被分配给集群中的任何节点。这就意味着批量请求中的每个操作**都需要被转发到正确节点上的正确分片。** 如果用 JSON， 就需要先反序列化，然后查看请求以确定去哪个分片，再为每个分片都构造请求数组，再将这些数组都序列化为内部传输格式，将请求传输到每个分片。这样做是可行的，但是**需要大量的 RAM 来存储原本相同数据的副本，创建更多的数据结构，JVM 花更多的时间进行垃圾回收**。

## 搜索 -- 最基本的工具

ES 中的每个字段都被索引，且可以被查询。需要理解以下三个概念：

`mapping`: 描述数据在那个字段内如何存储

`analysis`: 全文是如何处理使之可以被搜索的

`query DSL`: es 中的查询语言

### 空搜索

`GET /_search`: 没有指定任何查询的空搜索，它简单地返回集群中所有索引下的所有文档。

```json
{
   "hits" : {
      "total" :       14,               // 匹配到的文档总数
      "hits" : [                        // 返回查询结果的前十个文档
        {
          "_index":   "us",
          "_type":    "tweet",
          "_id":      "7",
          "_score":   1,                // 衡量了文档和查询的匹配程度，默认情况下会返回最相关的文档结果，这个例子中没有指定任何查询，所有的 score = 1
          "_source": {
             "date":    "2014-09-17",
             "name":    "John Smith",
             "tweet":   "The Query DSL is really powerful and flexible",
             "user_id": 2
          }
       },
        ... 9 RESULTS REMOVED ...
      ],
      "max_score" :   1                 // 最大的 score 值
   },
   "took" :           4,                // 执行整个搜索请求耗费了多少秒
   "_shards" : {                        // 执行查询中参与分片的总数，以及这些分片成功了几个，失败了几个
      "failed" :      0,
      "successful" :  10,
      "total" :       10
   },
   "timed_out" :      false             // 告诉查询是否超时，可以在 query 参数里进行指定
   // timeout 并不是停止执行查询，它仅仅是告知正在协调的节点返回到目前为止收集到的结果，并且关闭连接。在后台，其它节点可能还在执行结果，只不过结果已经被发送了。
}
```

### 多索引、多类型

`/_search`

`/gb/_search`

`/gb,us/_search`

`/g*,u*/_search`

`/gb,us/user,tweet/_search`：在 gb, us 索引中搜索 user 和 tweet 类型

`/_all/user,tweet/_search`：在所有的索引中搜索 user 和 tweet 类型

索引一个索引有五个分片 和 搜索五个索引各有一个分片准确来说是等价的。

### 分页

`size`：显示应该返回的结果数量，默认是10

`from`：显示应该跳过的初始结果的数量，默认是0

```json
GET /_search?size=5          // 第一页
GET /_search?size=5&from=5   // 第二页
GET /_search?size=5&from=10  // 第三页
```

考虑到分页过深以及一次请求太多结果的情况，结果集在返回之前先进行排序，但是一个请求经常跨越多个分片，每个分片都产生自己的排序结果，这些结果需要进行集中排序以保证整体顺序是正确的。**在分布式系统中，对结果排序的成本随分页的深度呈指数上升，这就是 web 搜索引擎对任何查询都不要返回超过 1000 个结果的原因。**

### 轻量搜索

轻量搜索就是 *查询字符串版本*，要求在查询字符串中传递所有的参数。比如

`GET /_all/tweet/_search?q=tweet:elasticsearch ` 在所有索引的 tweet 类型中搜索 tweet 字段中包含 elasticsearch 的所有的文档。

`GET /_search?q=name:john+tweet:mary` 在所有索引的所有类型中搜索 name 字段包含 john **且** 在 tweet 字段中包含 mary 的所有的文档。

`+` 表示必须与查询条件匹配，`-` 表示一定不与查询条件相匹配。没有这俩就表示所有的条件都是 **可选** 的。匹配的越多，文档就越相关。

#### _all 字段

```json
GET /_search?q=mary
```

这个查询会在所有字段中查找含有 `mary` 这个文档数据。**当 es 取出所有的字段的值拼成一个大的字符串，作为 _all 字段进行索引**。当 `_all` 字段不再有用时，可以将它设置为失效。

#### 更复杂的查询

```json
+name:(mary john) + date:>2014-09-10 + (aggregations geo)
```

这个查询会查找 name 字段中包含 mary 或 john **且** date 值大于 2016-09-10 **且** _all 字段包含 aggregations 或者 geo。

**不推荐** 直接向用户暴露查询字符串搜索功能，除非对于集群和数据来说非常信任他们。

## 映射和分析

奇怪的现象：

```json
GET /_search?q=2014              # 12 results
GET /_search?q=2014-09-15        # 12 results !
GET /_search?q=date:2014-09-15   # 1  result
GET /_search?q=date:2014         # 0  results !
```

**可能是数据在 _all 字段 和 date 字段 的索引方式不同。**

```python
GET /gb/_mapping/tweet
{
   "gb": {
      "mappings": {
         "tweet": {
            "properties": {
               "date": {
                  "type": "date",
                  "format": "strict_date_optional_time||epoch_millis"
               },
               "name": {
                  "type": "string"
               },
               "tweet": {
                  "type": "string"
               },
               "user_id": {
                  "type": "long"
               }
            }
         }
      }
   }
}
```

**_all 字段是 string 类型的，date 字段是 date 类型的。因此两者搜索结果不一样是正常的。**因为 _all 是全文域，date 是精确值域。

### 精确值 & 全文

*es 中的数据可以概括分为两类：精确值 和 全文。*全文通常指非结构化的数据，自然语言是高度结构化的，规则是复杂的，所以计算机难以正确解析。精确值是很容易查询的，结果是二进制的，要么匹配查询，要么就不匹配。而全文查询通常问的是该文档和给定查询的相关性如何。

### 倒排索引

 es 中使用一种称为 **倒排索引** 的结构，它适用于快速的全文搜索。**一个倒排索引由文档中所有不重复词的列表构成**，对于其中每个词，有一个包含它的文档列表。

```markdown
假设有两个文档，每个文档的 content 域包含如下内容：

1. The quick brown fox jumped over the lazy dog
2. Quick brown foxes leap over lazy dogs in summer
```

+ 首先将每个 content 域 **拆分** 成单独的词

+ 创建一个包含了所有 **不重复** 词条的 **排序** 列表。列出每个词在哪个文档。
+ 如果将 **词条** 和 **用户搜索词条** 规范为标准模式，如都小写显示，就可以找到与用户搜索的词条**不完全一致**，但具有足够相关性的文档。

```
Term      Doc_1  Doc_2
-------------------------
Quick   |       |  X
The     |   X   |
brown   |   X   |  X
dog     |   X   |
dogs    |       |  X
fox     |   X   |
foxes   |       |  X
in      |       |  X
jumped  |   X   |
lazy    |   X   |  X
leap    |       |  X
over    |   X   |  X
quick   |   X   |
summer  |       |  X
the     |   X   |
------------------------
```

### 分析与分析器

分析则执行的是上节所述的过程。分析器实际上将三个功能封装到了一个包里：

**字符过滤器**：

在**分词前整理字符串**，一个字符过滤器可以用来去掉 `html`, 或者将 `&` 转换为 `and`。

**分词器**：

字符串被分词器**拆分**成多个词条，一个简单的分词器在遇到空格和标点时，可能会将文本拆分为词条。

**Token 过滤器：**

可能会**改变**词条(如大小写转换)，**删除**词条(如 a、and、the 等无用词)，**增加**词条(jump 和 leap 这种同义词)。

*es 提供了开箱即用的字符过滤器、分词器、Token 过滤器。这些组合起来形成自定义的分析器以用于不同的目的。这是可以自定义的。*

#### 内置分析器

`"Set the shape to semi-transparent by calling set_trans(5)"`

+ 标准分析器
  + es 默认使用的分析器。根据 Unicode 联盟定义的 单词边界 划分文本。删除绝大部份的标点。最后将词条小写转换。
  + `set, the, shape, to, semi, transparent, by, calling, set_trans, 5`
+ 简单分析器
  + 会在任何不是字母的地方分隔文本，然后将词条小写
  + `set, the, shape, to, semi, transparent, by, calling, set, trans`
+ 空格分析器
  + 在有空格的地方划分文本
  + `Set, the, shape, to, semi-transparent, by, calling, set_trans(5)`
+ 语言分析器
  + 应用于很多自然语言，比如 英语分析器 就把 `and`、`the` 这种无用的连接词给删除。
  + `set, shape, semi, transpar, call, set_tran, 5` call 为 calling 的词根形式，这些都会转换。

#### 什么时候使用分析器

+ 当你查询一个 **全文域**，需要对查询字符串应用相同的分析器，以产生正确的搜索词条列表。
+ 当你查询一个 **精确值域**，不会分析查询字符串，而是直接搜索你指定的精确值。

#### 测试分析器

```json
GET /analyze   // 用于查看文本是如何被分析的
{
  "analyzer": "standard",
  "text": "Text to analyze"
}
```

**如果不想用标准分析器，我们也可以自己指定分析器。**

### 映射

es 支持如下简单域类型:

+ 字符串：string
+ 整数：byte、short、integer、long
+ 浮点数：float、double
+ 布尔型：boolean
+ 日期：date

当你索引一个包含新域的文档，之前未曾出现，es 会使用*动态映射*。通过 JSON 中基本数据类型，尝试猜测域类型。

|   JSON TYPE   | 域 TYPE  |
| :-----------: | :------: |
| true or false | boolean  |
|      123      | long int |
|    123.45     |  double  |
|  2015-09-15   |   date   |
|    foo bar    |  string  |

#### 查看映射

`GET /gb/_mapping/tweet`

域**最重要的属性是** type，对于不是 string 的域，一般只要设置 type 就可以。**默认**，string 类型包含全文。就是说，他们的值在索引前会通过分析器，针对于这个域的查询在搜索前也会经过一个分析器。

+ string 域映射的两个最重要的属性是 index 和 analyzer

  ```json
  {
      "tag": {
          "type":     "string",
          "index":    "not_analyzed"
      }
  }
  ```

#### index

+ **analyzed（默认）**：首先分析字符串，然后索引它。以全文索引这个域。
+ **not_analyzed**：索引这个域，使之能够被搜索，但索引的是精确值，不会对它进行分析。
+ **no**：不索引这个域，这个域都不会被搜索到。

所以，如果想要一个 string 类型的域被精确搜索，只要将 index 设置为 not_analyzed, 其它类型也是有 index 属性的，比如 int、long、date，但是有意义的也只有 no 和 not_analyzed。

#### analyzer

```json
{
    "tweet": {
        "type":     "string",
        "analyzer": "english"
    }
}
```

+ 用于指定在搜索和索引时使用的分析器，默认用的是 `standard` 分析器。你也可以自己指定，比如 `whitespace`、`simple`、`english`。你也可以自定义一个分析器。

#### 更新映射

**不能修改** 已存在的域映射，如果一个域映射已经存在，该域的数据可能已经被索引，如果意图修改这个域的映射，索引的数据 **可能会出错**，不能被正常的索引。

```json
DELETE /gb
PUT /gb 
{
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "string",
          "analyzer": "english"
        },
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "string"
        },
        "user_id" : {
          "type" :   "long"
        }
      }
    }
  }
}
```

```json
// 新增某个域类型映射
PUT /gb/_mapping/tweet
{
  "properties" : {
    "tag" : {
      "type" :    "string",
      "index":    "not_analyzed"
    }
  }
}
```

#### 测试映射

```json
// analyze API 测试字符串域的映射，这个 API GET 请求是带请求体的
GET /gb/_analyze
{
  "field": "tweet",
  "text": "Black-cats" 
}

GET /gb/_analyze
{
  "field": "tag",
  "text": "Black-cats" 
}
```

### 复杂核心域类型

#### 多值域（数组）

`{"tag": ["search", "nosql"]}`  tag 域的值是一个数组。数组可以包含 任意多个值，包括 0 个值。

**数组中所有值都必须是相同数据类型的。** 你不能将 日期 和 字符串 混在一起。如果你通过索引数组来创建新的域，es 会用数组中的 **第一个值的数据类型作为这个域的类型。** 数组里的值是有序的，但是搜索的时候是无法指定搜索多值域里的第一个还是最后一个。

#### 空域

`null`、`[]`、`[null]` 被认为是空的，它们将不会被索引。

#### 多层级对象

```json
{
    "tweet":            "Elasticsearch is very flexible",
    "user": {
        "id":           "@johnsmith",
        "gender":       "male",
        "age":          26,
        "name": {
            "full":     "John Smith",
            "first":    "John",
            "last":     "Smith"
        }
    }
}
```

```json
{
  "gb": {
    "tweet": {                                          // 根对象
      "properties": {
        "tweet":            { "type": "string" },
        "user": {                                       // 内部对象
          "type":             "object",
          "properties": {
            "id":           { "type": "string" },
            "gender":       { "type": "string" },
            "age":          { "type": "long"   },
            "name":   {                                 // 内部对象
              "type":         "object",
              "properties": {
                "full":     { "type": "string" },
                "first":    { "type": "string" },
                "last":     { "type": "string" }
              }
            }
          }
        }
      }
    }
  }
}
```

#### 内部对象是如何索引的

内部对象会被扁平化处理，内部对象数组扁平化数据会 **丢失相关性，丢失有序性。**

```json
{
    "followers": [
        { "age": 35, "name": "Mary White"},
        { "age": 26, "name": "Alex Jones"},
        { "age": 19, "name": "Lisa Smith"}
    ]
}
```

```json
{
    "followers.age":    [19, 26, 35],
    "followers.name":   [alex, jones, lisa, smith, mary, white]
}
```

## 请求体查询

### 空查询

`{}` 空查询将返回索引库中的所有文档。

`GET /index_2014*/type1,type2/_search` 可以在 前缀是 index_2014 的索引中，在 type1 和 type2 中查询。如果想要在所有的索引中查询可以使用 `_all` 索引库。带上下列请求体，则可以对返回数据进行分页。*RFC 7231 文档中并没有规定一个带有请求体的 GET 请求应该如何处理，所以是某一些 HTTP 服务器允许这样使用，一些用于缓存和代理的服务器则不允许这样使用。*

```json
{
  "from": 30,
  "size": 10
}
```

### 查询表达式（query DSL）

要是用这种表达式先要把查询语句传递给 `query` 参数。

```json
// DSL 基本结构
{
  query_name: {
    field_name: {
      argument: value,
      argument: value
    }
  }
}
```

```json
// 查询所有
{                                               {}
  "query": {
    "match_all": {}              <==>            
  }
}
```

```json
// 查询某个具体字段的值
{
  "query": {
		"match": {"tweet": "elasticsearch"}    
  }
}
```

#### 合并查询语句

```json
// 这是一条复合语句，复合语句可以包含其它任何查询语句，包括复合语句
{
  "bool": {                                               // bool 允许在你需要的时候组合其它语句
    "must": {"match": {"tweet": "elasticsearch"}},        
    "must_not": {"match": {"name": "mary"}},
    "should": {"match": {"tweet": "full text"}},
    "filter": {"range": {"age": {"gt": 30}}}
  }
}
```

## 查询与过滤

**过滤查询**：

只是简单的检查包含或者不包含，计算很快。使用部评分查询，*结果会被缓存到内存中以便于快速读取*。

**评分查询**：

不仅仅要找出相关的文档，还要计算每个匹配文档的相关性，*且查询结果并不被缓存。*

*不过由于倒排索引的缘故，简单的评分查询在匹配少量的文档时的性能可能比一个涵盖百万文档的 filter 表现的一样好，升至更好*。

**不过，过滤的目标始终是减少那些需要通过评分查询进行检查的文档。**

## 最重要的查询

**match_all**

简单匹配所有的文档，没有指定查询方式时，它是默认的查询，经常与 filter 结合使用。

`{"match_all": {}}`

**match**

无论你在任何字段上进行全文搜索还是精确查询，match 是你可用的标准查询，取决你是在全文字段还是精确字段上使用。

`{"match": {"tweet": "about search"}}`

**multi_match**

可以在多个字段上执行相同的 match 查询

```json
{
  "multi_match": {
    "query": "full text search",
    "fields": ["title", "body"]
  }
}
```

**range**

range 查询找出那些落定在指定区间内的数字或时间

```json
{
  "range": {
    "age": {
      "gte": 20, 
      "lt": 30
    }
  }
}
```

**term**

被用于 *精确匹配*，`term` 查询对于输入的文本 *不分析*，所以它将给定的值用于精确查询。

```json
{"term": {"age": 26}}
{"term": {"tag": "full text"}}
```

**terms**

`terms` 查询和 `term` 查询一样，但是允许多值匹配，*如果这个字段包含了指定值中的任何一个值*，那么这个文档满足条件。

```json
{
  "terms": {
    "tag": ["search", "full_text", "nosql"]
  }
}
```

**exists 和 missing**

相当于 sql 中的 `IS NOT NULL` 和 `IS NULL`

`{"exists": {"field": "title"}}`

## 组合多查询

`bool` 查询可以将多种查询组合在一起，接受 `must`、`must_not`、`should`、`filter` 参数。

+ **must**
  + 文档 **必须包含** 这些条件才能被包含进来
+ **must_not**
  + 文档 **必须不包含** 这些条件才能被包含进来
+ **should**
  + 文档 **包含这些条件中的任意条件** 将增加 `_score`，否则无任何影响，主要用于修正文档的相关性得分。
  + **important:** 如果没有 `must` 语句，至少需要匹配一条 `should` 语句，如果存在至少一条 `must` 语句，则对 `should` 语句的匹配**无要求**。 <-------------
+ **filter**
  + **必须匹配**，但它以部评分、过滤模式来进行，对评分没有贡献，只是根据过滤标准来排除或包含文档。

每个字查询都独自地计算文档的相关性得分，一旦他们的得分被计算出来，bool 查询将这些得分进行合并并且返回一个代表整个布尔操作的得分。所有的查询都可以将 `查询放到 filter 中` 这样会自动转成一个不评分的。如果 `filter` 逻辑比较复杂的话，在 `filter` 内部构造 `bool` 查询即可。

```json
// 查找 title 包含 "how to make millions" 且 tag 不包含 "spam" 的
// 那些被标识为 starred 的 或 date 大于等于 2014-01-01 的文档评分会更高，两者都满足的话评分自然更更高
{
  "bool": {
    "must": {"match": {"title": "how to make millions"}},
    "must_not": {"match": {"tag": "spam"}},
    "should": [
      {"match": {"tag": "starred"}}
    ],
    "filter": {
      "range": {"date": {"gte": "2014-01-01"}}
    }
  }
}
```

```json
// 牛逼，奇技淫巧啊
{
    "bool": {
        "must":     { "match": { "title": "how to make millions" }},
        "must_not": { "match": { "tag":   "spam" }},
        "should": [
            { "match": { "tag": "starred" }}
        ],
        "filter": {
          "bool": { 
              "must": [
                  { "range": { "date": { "gte": "2014-01-01" }}},
                  { "range": { "price": { "lte": 29.99 }}}
              ],
              "must_not": [
                  { "term": { "category": "ebooks" }}
              ]
          }
        }
    }
}
```

### *constant_score

它将一个不变的常量评分应用于所有匹配的文档，它被经常用于，你只需要一个 `filter` 而没有其它查询的情况下，**用于取代只有 `filter` 语句的 `bool` 查询，在性能上是完全相同的**，但是对于提高简洁性和清晰度上有很大的帮助。

```json
{
    "query" : {
        "constant_score" : { 
            "filter" : {
                "term" : {"price" : 20}
            }
        }
    }
}
```

## 验证查询

`GET /gb/tweet/_validate/query`

```json
// 用于验证查询是否合法
{
  "query": {
    "tweet": {"match": "really powerful"}
  }
}
```

```json
{
  "valid" :         false,
  "_shards" : {
    "total" :       1,
    "successful" :  1,
    "failed" :      0
  }
}
```

### 理解错误信息

`GET /gb/tweet/_validate/query?explain` 请求体和上面一样，这样返回结果会带有 *查询不合法的原因*。

```json
{
  "valid" :     false,
  "_shards" :   { ... },
  "explanations" : [ {
    "index" :   "gb",
    "valid" :   false,
    "error" :   "org.elasticsearch.index.query.QueryParsingException:
                 [gb] No query registered for [tweet]"
  } ]
}
```

### 理解查询语句

`GET /_validate/query?explain`

```json
{
   "query": {
      "match" : {
         "tweet" : "really powerful"
      }
   }
}
```

```json
{
  "valid" :         true,
  "_shards" :       { ... },
  "explanations" : [ {
    "index" :       "us",
    "valid" :       true,
    "explanation" : "tweet:really tweet:powerful"
  }, {
    "index" :       "gb",
    "valid" :       true,
    "explanation" : "tweet:realli tweet:power"
  } ]
}
```

我们查询的每一个 index 都会返回对应的 explanation, 因为每一个 index 都有自己的映射和分析器。可以看出被重写成了两个 `term` 查询语句。对于索引 `us`，这两个 `term` 分别是 `really` 和 `powerful`。对于索引 `gb`，这两个 `term` 分别是 `realli` 和 `power`。很明显 `realli` 并不是 `really` 的原形，所以该用 `gb` 分析器为 `english` 分析器。

## 排序和相关性

### 排序

如果没有用 *评分查询语句*，只有 `filter` 语句 或者是前面的 `constant_score` 语句，则所有返回的文档评分为 0 分，且文档按照随机顺序返回。

### 按照字段字段的值排序

```json
{
  "query": {
    "bool": {"filter": {"term": {"user_id": 1}}}
  },
  "sort": {"date": {"order": "desc"}}      // "sort": "number_of_children" <==> "sort": {"number_of_children": {"order": "asc"}}
}
```

```json
"hits" : {
    "total" :           6,
    "max_score" :       null,     // _score 不被计算，因为它并没有用于排序, 如果一定要计算评分，使用 track_scores=true
    "hits" : [ {
        "_index" :      "us",
        "_type" :       "tweet",
        "_id" :         "14",
        "_score" :      null,     // 计算 _score 的值花销巨大，通常仅用于排序，我们并不按照 _score 排序则记录是没有意义的
        "_source" :     {
             "date":    "2014-09-24",
             ...
        },
        "sort" :        [ 1411516800000 ]     // 表示为 1970-01-01 00:00:00 以来到 当前文档的 date 的毫秒数，通过 sort 字段的值进行返回
    },                                    
    ...
}
```

### 多级排序

*请求体中排序*

```json
{
    "query" : {
        "bool" : {
            "must":   { "match": { "tweet": "manage text search" }},
            "filter" : { "term" : { "user_id" : 2 }}
        }
    },
    // 结果先按照第一个条件排序，仅当结果集的第一个 sort 值完全相同时才会按照第二个条件进行排序 
    "sort": [
        { "date":   { "order": "desc" }},
        { "_score": { "order": "desc" }}
    ]
}
```

*query-string 中排序*

`GET /_search?sort=date:desc&sort=_score&q=search`

### 多值字段的排序

对于数字或者日期，你可以 **通过 min,max,avg 将多值字段变为单值**。

```json
"sort": {
  "dates": {
    "order": "asc",
    "mode": "min"
  }
}
```

## 字符串排序与多字段

被解析的字符串字段也是多值字段，比如 `'fine old art'` ，我们很可能想要按照第一个单词的字母排序，然后再按照第二个单词的字母排序。

为了以字符串字段进行排序，这个字段应该仅包含一项 `not analyzed`，但是又想进行全文检索。**只要给该字段用上两个 index, analyzed 和 not analyzed**。前者用于排序，后者用于检索。

但是保存相同的字符串两次在 _source 字段是浪费空间的，我们想要做的是 **传递一个单类型字段但是却可以用两种方式索引**。所有的 _core_field 类型(strings, numbers, booleans,  dates) 接收一个 `fields` 参数。这个参数允许你转化一个简单的映射：

```  json
"tweet": {
    "type":     "string",
    "analyzer": "english"
}
```

上面的单类型映射会转换为下面的多类型映射

```json
"tweet": {           // tweet 主字段是一个 analyzed
    "type":     "string",
    "analyzer": "english",
    "fields": {
        "raw": {     // tweet.raw 是 not_analyzed
            "type":  "string",
            "index": "not_analyzed"
        }
    }
}
```

检索只要使用

```json
{
    "query": {
        "match": {
            "tweet": "elasticsearch"
        }
    },
    "sort": "tweet.raw"
}
```

**如果想要以全文 analyzed 字段排序会消耗大量的内存！！！！！！！！务必转换。**

## 什么是相关性

_score 是一个 **正浮点数**，评分越高，相关性越高，评分的 **计算方式** 取决于查询语句。不同的查询语句用于不同的目的。

1. `fuzzy` 查询计算与关键词的拼写的相似程度
2. `terms` 查询会计算找到的内容与关键词组成部分匹配的百分比

Elasticsearch 的相似度算法被定义为 **检索词频率/反向文档频率（TF/IDF）:**

+ 检索词频率

  检索词在**该文档**出现的频率越高，相关性越高。

+ 反向文档频率

  检索词在**该索引的所有文档中**出现的频率越高，相关性越低。

+ 字段长度准则

  字段的长度越长，相关性越低。

+ 相关性也适用于 yes|no 的子句，匹配的子句越多，相关性评分越高。

### 理解评分标准

词频率和文档频率是在每个分片中被计算出来的，而不是在每个索引中。

`GET /_search?explain `。explain 的代价十分昂贵，只能用作调试，不能用做生产。如果在参数中加上 `format=yaml` 返回体则为 yml 文档。

```json
{
   "query"   : { "match" : { "tweet" : "honeymoon" }}
}
```

```json
"_explanation": { 
   "description": "weight(tweet:honeymoon in 0)
                  [PerFieldSimilarity], result of:",
   "value":       0.076713204,
   "details": [
      {
         "description": "fieldWeight in 0, product of:",
         "value":       0.076713204,
         "details": [
            {  
               "description": "tf(freq=1.0), with freq of:",    // 检索词频率
               "value":       1,
               "details": [
                  {
                     "description": "termFreq=1.0",
                     "value":       1
                  }
               ]
            },
            { 
               "description": "idf(docFreq=1, maxDocs=1)",      // 反向文档频率
               "value":       0.30685282
            },
            { 
               "description": "fieldNorm(doc=0)",               // 字段长度准则
               "value":        0.25,
            }
         ]
      }
   ]
}
```

### 理解文档是如何被匹配到的

当 `explain` 被应用于某一文档上时，`/index/type/id/_explain` 会返回文档为何未被匹配的原因。

## Doc Values 介绍

在**搜索**的时候，我们能通过搜索关键词**快速**的到结果集。当**排序**的时候，需要倒排索引里面某个字段的集合。这就需要 **转置** 倒排索引。**转置结构** 在其它系统中经常被称为是 **列存储**。这使得对其进行排序操作是十分高效的。

`Doc Values` 是一种 *列式存储结构*，它在索引时创建，当字段索引时，es 为了能快速检索，会把字段的值加入到倒排索引中，同时也会存储该字段的 `Doc Values`。这种结构常被应用于 排序、聚合、地理位置过滤、某些与字段相关的脚本计算。

**也就是说，排序是发生在索引时建立的平行数据结构中的。**

## 执行分布式检索

一个搜索请求必须询问我们关注的索引的所有分片的所有副本来确定它们是否包含任何匹配的文档。

找到所有的匹配文档仅仅完成事情的一半，在 `search` 接口返回一个 `page` 结果之前，多分片中的结果必须组合成单个排序列表。

因此这个两阶段过程为：query_then_fetch

## 查询阶段

查询会广播到索引中的每一个分片拷贝(主分片或副本分片)。每个分片都在本地执行搜索并构建一个匹配文档的优先队列。优先队列是一个仅仅存有 *top-n* 匹配文档的有序列表，优先队列的大小取决于分页参数 `from` 和 `size`。

**查询过程分布式搜索：**

+ 客户端发送一个 `search` 请求到 `node3`, `node3` 会创建一个大小为 `from + size` 的空优先队列。
+ `node3` 将查询请求**转发**到索引的**每个**主分片和副本分片，然后在每个分片**本地**执行查询并添加结果到大小为 `from + size` 的本地优先队列中。(当然这个是谁有空谁会执行查询，因此才能增加吞吐率，且协调负载)
+ 每个分片返回各自优先队列中的所有文档 ID 和排序值给**协调节点(请求发给谁谁就是协调节点)**，即 `node3`, 它会合并这些值到自己的优先队列中来产生一个**全局排序**以后的结果列表。

一个索引可以由一个或者几个主分片组成，所以一个针对单个索引的搜索请求需要能够把来自多个分片的结果组合起来。

## 取回阶段

查询阶段只是 **标识** 哪些文档满足搜索请求，我们仍需 **取回** 文档。取回阶段由以下部分组成：

+ 协调节点 **辨别** 出哪些文档需要被取回并向相关的分片提交 **多个 GET 请求**。(例如 `{"from": 90, "size": 1}` 则最初的 90 个结果会被丢弃，第 91 个结果需要被取回，这些文档可能来自一个或者多个分片。协调节点会给持有相关文档的每个分片创建一个 multi-get 请求，并发送请求给同样处于查询阶段的分片副本）
+ 每个分片加载并 **丰富** 文档，如果有需要的话，接着返回文档给协调节点。(根据需要加载 `_source` 字段，元数据、`search snippet highlighting` 来丰富文档)
+ 一旦所有的文档都被返回，协调节点包装成单个响应返回给客户端。

##### 深分页（Deep Pagination）

使用 `from` 和 `size` 的这个过程就是深分页，每个分片都需要创建 `from + size` 长度的队列，而协调节点需要根据 `number_of_shards * (from + size)` 排序文档，来找到包含在 `size` 里的文档。如果 `from` 太大，排序过程可能会变得非常沉重，使用大量的 CPU、内存、带宽。不过 1000 ～ 5000 页是完全可行的，再多的话不建议使用 深分页。

如果确实需要从集群中 **取回大量的文档**，可以使用 `scroll` 查询禁用排序，使得这个取回行为更加有效率。

## 搜索选项

### 偏好

**`perference` 参数控制由哪些分片或节点来处理搜索请求。**尤其可以避免 *Bouncing Results*。比如两个文档有同样的时间戳字段，搜索结果需要按照时间戳进行排序。用户每次刷新页面时，搜索结果表现文档为不同的顺序，所以这时候如果指定只使用一种分片，就可以避免这种问题。搜索请求在所有有效的分片副本间进行轮循，有可能发生主分片处理请求时，这俩文档是一种顺序，副本分片处理请求时又是另一种顺序。(这句话没理解呀，不都是返回主分片进行全局排序么？意思是全局排序时不稳定的排序？)

**只要让同一个用户始终使用同一个分片，就可以避免这种问题。设置 `perference` 参数为一个特定的任意值，比如用户会话 ID 来解决。**

### 超时问题

`timeout` 参数就是告诉 *分片允许处理数据的最大时间。* 如果没有足够的时间处理数据(最慢分片的处理时间 + 所有结果合并的时间)，这个分片的结果**可以是部分的，甚至是空数据。**

响应体里的 `{"time_out": true}` 标明了分片是否返回的是 **部分结果**。

*虽然设置了超时，但是很可能还会发生查询超过设定的超时时间，因为*

+ 超时检查是基于每个文档做的。但是某些查询类型有大量的工作在文档评估之前需要完成。
+ 一次长时间查询在单个文档上执行并且在下个文档被评估之前不会超时，这意味着差的脚本将会永远执行下去。

### 路由

在搜索的时候，不用搜索索引的所有分片，而是通过指定几个 `routing` 值来限定只搜索几个相关的分片即可。这种设计在大规模搜索系统时会派上用场。

`GET /_search?routing=user_1,user2`

### 搜索类型

缺省的搜索类型值为 `query_then_fetch`, 改善相关性精度也可以使用下列搜索类型。

`GET /_search?search_type=dfs_query_then_fetch`

`dfs_query_then_fetch` 有预查询的阶段，这个阶段可以从所有相关分片获取词频来计算全局词频。

## 游标查询 Scroll

`scroll` 可以用来对 es 执行大批量的文档查询，且不用付出深度分页的代价。**游标查询** 允许我们先做 **查询初始化**，然后再 **批量拉取结果**，有点像传统数据中的 **cursor**。

+ 查询初始化

  游标查询会取某个时间点的 **快照数据**，查询初始化之后索引上的任何变化都会被忽略，它通过 **保存旧的数据文件** 来实现这个特性，结果就像保留初始化时的索引 *视图* 一样。

+ 批量拉取结果

  深度分页的 **代价根源** 是结果集全局排序，如果去掉全局排序的特性的话，查询结果的成本就会很低。游标查询用字段 `_doc` 来排序。`scroll` 让 es 仅仅从还有结果的的分片返回下一批结果。(没明白)。

+ 使用

  ```json
                                      // 保持游标查询窗口需要小号资源，所以应该在稍有空闲的时候就释放掉
  GET /old_index/_search?scroll=1m    // 1m 为我们期望的游标查询的过期时间，过期时间会在每次做查询的时候刷新，这个时间只要足够处理当前批的结果就可以
  {
      "query": { "match_all": {}},
      "sort" : ["_doc"],              // 最有效的排序顺序 `_doc`
      "size":  1000                   // 也有可能取到超过 1000 个文档数量，size 作用于单个分片，所以每个批次返回的实际数量最大为 
                                      // size * number_of_primary_shards
  }
  ```

+ 返回

  ```json
  GET /_search/scroll
  {
      "scroll": "1m", 
      "scroll_id" : "cXVlcnlUaGVuRmV0Y2g7NTsxMDk5NDpkUmpiR2FjOFNhNnlCM1ZDMWpWYnRROzEwOTk1OmRSamJHYWM4U2E2eUIzVkMxalZidFE7MTA5OTM6ZFJqYkdhYzhTYTZ5QjNWQzFqVmJ0UTsxMTE5MDpBVUtwN2lxc1FLZV8yRGVjWlI2QUVBOzEwOTk2OmRSamJHYWM4U2E2eUIzVkMxalZidFE7MDs="
  }
  ```

  `scroll_id` 是一个 base64 编码的长字符串，现在我们能传递 `_scroll_id` 到 `_search/scroll` 查询接口获取下一批结果。

## 索引管理

## 创建一个索引

`PUT /my_index`

```json
{
    "settings": { ... any settings ... },
    "mappings": {
        "type_one": { ... any mappings ... },
        "type_two": { ... any mappings ... },
        ...
    }
}
```

**自动创建索引：**

用索引模版来预配置开启自动创建索引。这在索引日志数据的时候有用，将日志数据索引在一个以日期结尾命名的索引上，子夜时分，一个预配置的心索引将会自动创建。

**关闭自动创建索引：**

在 `config/elasticsearch.yml` 的每个节点下面添加 `action.auto_create_index: false`

## 删除一个索引

`DELETE /my_index`

`DELETE /index_one,index_two`

`DELETE /index_*`

`DELETE /_all`  `DELETE /*` 删除全部索引

**避免意外大量删除**

在 `elasticsearch.yml` 中修改 `action.destructive_requires_name: true`，设置了以后使删除只限定于特定名称指向的数据，不允许通过指定 `_all` 或 通配符来删除指定索引库。

## 索引设置

`PUT /my_temp_index`

```json
{
    "settings": {
        "number_of_shards" :   1,          // 主分片数，索引创建完以后不能更改
        "number_of_replicas" : 0           // 每个主分片的副本数，默认值1，可以随时修改
    }
}
```

`PUT /my_temp_index/_settings`  用于修改副本分片数

```json
{"number_of_replicas": 1}
```

## 配置分析器

`standard` 分析器 是用于全文字段的默认分析器，对于大部分西方语系来说是一个不错的选择。它包含了：

+ `standard` 分词器
  + 通过单词边界分割输入的文本
+ `standard` 语汇单元过滤器
  + 整理分词器出发的语汇单元
+ `lowercase` 语汇单元过滤器
  + 转换所有的语汇单元为小写
+ `stop` 语汇单元过滤器（默认情况下是禁用的，停用列表可以开启，也可以自定义配置停用词列表）
  + 删除停用词，如 `a`、`the`、`and`、`is`

`PUT /spanish_docs`

```json
{
    "settings": {
        "analysis": {
            "analyzer": {
                "es_std": {                    // 这个是新创建的分析器，叫做 es_std, 使用预定义的西班牙停用词列表；
                    "type":      "standard",   // es_std 并非全局，仅仅存在于 spanish_docs 索引中
                    "stopwords": "_spanish_"
                }
            }
        }
    }
}
```

```json
GET /spanish_docs/_analyze?analyzer=es_std
El veloz zorro marrón
```

```json
// 可以看到 El 已经被正确删除了
{
  "tokens" : [
    { "token" :    "veloz",   "position" : 2 },
    { "token" :    "zorro",   "position" : 3 },
    { "token" :    "marrón",  "position" : 4 }
  ]
}
```

## 自定义分析器

一个分析器就是 一个包里面组合了 **三种函数** 的一个包装器。三种函数按照顺序被执行：

+ **字符过滤器**

  用来整理一个尚未被分词的字符串。例如移除 html 标签，把 `&Aacute;` 转换为对应的 Unicode 字符 A。一个分析器可能有 *0 个* 或者 *多个* 字符过滤器。

+ **分词器**

  一个分析器中有且只有一个分词器。它将字符串分解为单个词条或者词汇单元。

  + **标准分词器** 将一个字符串根据单词边界分解为单个词条，并且移除掉大部分的标点符号。

  + **关键词分词器** 完整地输出接收到的同样的字符串，不做任何分词。

  + **空格分词器** 根据空格分割文本。

  + **正则分词器** 根据正则表达式分割文本。

+ **词单元过滤器**

  经过分词器的词单元流会按照指定的顺序通过指定的词单元过滤器。词单元过滤器用于修改、添加、删除词单元。

  + **词干过滤器** 将单词转换为词干
  + **ascii_folding 过滤器** 移除变音符(très 转换为 tres)
  + **ngram 和 edge_ngram 词单元过滤器** 可以产生适用于部分匹配或者自动补全的词单元

### 创建一个自定义分析器

`PUT /my_index`

```json
{
    "settings": {
        "analysis": {
            "char_filter": { ... custom character filters ... },       // 字符过滤器
            "tokenizer":   { ...    custom tokenizers     ... },       // 分词器
            "filter":      { ...   custom token filters   ... },       // 词单元过滤器
            "analyzer":    { ...    custom analyzers      ... }        // 分析器
        }
    }
}
```

示例，自定义分析器：

```json
PUT /my_index
{
    "settings": {
        "analysis": {
            "char_filter": {
                "&_to_and": {                        //  使用一个自定义 映射字符过滤器，把 & 替换为 and
                    "type":       "mapping",
                    "mappings": [ "&=> and "]
            }},
            "filter": {
                "my_stopwords": {                    //  自定义的停词过滤器移除自定义的停止词列表中包含的
                    "type":       "stop",
                    "stopwords": [ "the", "a" ]
            }},
            "analyzer": {
                "my_analyzer": {
                    "type":         "custom",
                    "char_filter":  [ "html_strip", "&_to_and" ],
                    "tokenizer":    "standard",
                    "filter":       [ "lowercase", "my_stopwords" ]
            }}
}}}
```

在某个字段上指定使用自定义分析器

```json
PUT /my_index/_mapping/my_type
{
    "properties": {
        "title": {
            "type":      "string",
            "analyzer":  "my_analyzer"
        }
    }
}
```

## 类型和映射

类型在 es 中表示一类相似的文档。类型由 *名称* 和 *映射* 组成。映射描述了文档可能具有的 *字段* 或 *属性*、*每个字段的数据类型*。

### Lucene 如何处理文档

在 Lucene 中，一个文档由一组简单的键值对组成，每个字段都可以有多个值，但至少要有一个值，因此一个字符串可以通过分析过程转化为多个值。当我们在 Lucene 中索引一个文档时，每个字段的值都被添加到相关字段的倒排索引中。你也可以将未处理的原始数据 *存储* 起来，以便这些原始数据在之后也可以被检索到。

### 类型是如何实现的

Lucene 没有文档类型的概念，每个文档的类型都被存储在一个叫 `_type` 的元数据字段上。当我们检索某个类型的文档时，es 通过在 `_type` 字段上使用过滤器限制，只返回这个类型的文档。Lucene 没有映射的概念，映射是 es 将复杂的 JSON 文档映射成 Lucene 需要的扁平化数据的方式。

例如，在 `user` 类型中，`name` 字段的映射可以声明这个字段是 `string` 类型，并且它的值被索引到名为 `name` 的倒排索引之前，需要通过 `whitespace` 分词器分析。

```json
"name": {
    "type":     "string",
    "analyzer": "whitespace"
}
```

### 避免类型陷阱

**如果有两个不同的类型，每个类型都有同名的字段，但是映射不同，比如一个是数字，一个是字符串，会出现什么情况？**

+ 简单的回答

  ES 不允许定义这样的映射，配置这样的映射时会出现异常。

+ 详细的回答

  每个 Lucene 索引中的所有字段都包含一个单一的、扁平的模式。一个特定的字段可以映射为 string 类型或 number 类型，但是不能两者兼具。在 ES 中所有类型最终都共享相同的映射。

```json
{
   "data": {
      "mappings": {
         "people": {
            "properties": {
               "name": {
                  "type": "string",
               },
               "address": {
                  "type": "string"
               }
            }
         },
         "transactions": {
            "properties": {
               "timestamp": {
                  "type": "date",
                  "format": "strict_date_optional_time"
               },
               "message": {
                  "type": "string"
               }
            }
         }
      }
   }
}
```

在 Lucene 内部转化为

```json
{
   "data": {
      "mappings": {
        "_type": {
          "type": "string",
          "index": "not_analyzed"
        },
        "name": {
          "type": "string"
        }
        "address": {
          "type": "string"
        }
        "timestamp": {
          "type": "long"
        }
        "message": {
          "type": "string"
        }
      }
   }
}
```

### 类型结论

多个类型可以在相同的索引中存在，只要它们的字段不冲突。

类型不适合 *完全不同类型* 的数据，如果两个类型的字段值不同，就以为着索引中将有一半的数据是空的，最终将导致性能问题。

## 根对象

映射的最高一层就是 **根对象**，它可能包含下面几项：

+ 一个 **properties 节点**，列出了文档中可能包含的每个字段的映射。
+ 各种 **元数据** 字段，以 `_` 打头，例如 `_type`、`_id` 、`_source`。
+ **设置项**，关于控制如何动态处理新的字段，例如 `analyzer`、`dynamic_date_formats`、`dynamic_templates`。
+ **其它设置**，可以同时应用在根对象和其它 `object` 类型的字段上，例如 `enabled`、`dynamic`、`include_in_all`。

### 属性

+ **type**
  + 字段的数据类型，string 或 date
+ **index**
  + **analyzed**：字段是否应当被当成全文来搜索
  + **not_analyzed**：被当成一个准确的值
  + **no**：完全不可搜索
+ **analyzer**
  + 确定在索引和搜索时，全文字段使用的 `analyzer` 是什么

### 元数据：_source 字段

**默认地**，es 在 `_source` 字段存储的是 **代表文档体的 JSON 字符串**。何所有被存储的字段一样，`_source` 字段在被写入磁盘之前会被 **压缩**。在下面这个搜索请求里，你可以通过在请求体中指定 `_source` 参数，来达到只获取特定的字段的效果：

```json
GET /_search
{
    "query": { "match_all": {}},
    "_source": ["title", "created"]
}
```

`_source` 就是一个被存储的字段，在 es 中对于文档的个别字段设置存储的方法通常不是最优的，整个文档都被存储为 `_source` 字段，使用 `_source` 参数提取你需要的字段总是好的。

### 元数据：_all 字段

`_all` 是一个把其它字段值当作一个大字符串来索引的特殊字段。

`GET /_search`

```json
{
    "match": {
        "_all": "john smith marketing"
    }
}
```

如果你不再需要 `_all` 字段，可以：

`PUT /my_index/_mapping/my_type`

```json
{
    "my_type": {
        "_all": { "enabled": false }
    }
}
```

通过 `include_in_all` 设置来逐个控制字段是否要包含在 `_all` 字段中，默认是 `true`。你可以为所有的字段默认禁用 `include_in_all`, 仅在你选择的字段上使用。

`PUT /my_index/my_type/_mapping`

```json
{
    "my_type": {
        "include_in_all": false,
        "properties": {
            "title": {
                "type": "string",
                "include_in_all": true
            },
            ...
        }
    }
}
```

`_all` 字段仅仅是一个经过分词的 `string` 字段，它使用默认分词器来分析它的值，不管这个值原本所在字段指定的分词器是什么。因此你也可以单独指定 `_all` 的分词器。

`PUT /my_index/my_type/_mapping`

```json
{
    "my_type": {
        "_all": { "analyzer": "whitespace" }
    }
}
```

### 元数据：文档标识

+ **_id**：文档的 ID 字符串（既没有被存储也没有被索引）
+ **_type**：文档的类型名（没有被存储但是被索引）
+ **_index**： 文档所在的索引（既没有被存储也没有被索引）
+ **_uid**：`type#id`（默认是被存储和索引的）

## 动态映射

当 es 遇到文档中以前 **未遇到过的字段**，它用 `dynamic mapping` 来 **确定字段的数据类型** 并且 **自动把新的字段添加到类型映射**。通常希望有新的字段被加入到文档可以 **自动被索引**，但是不希望有新的字段被加入到文档中却没人知道，因此如果 es 是作为重要的数据存储，可能就会期望 **遇到新字段就抛出异常**，这样可以及时发现问题。

**可以通过 dynamic 配置来控制这种行为：**

+ **true**：默认值，认为可以动态添加新的字段
+ **false**：忽略新的字段, 新的字段不会被加到映射中，也不可以被搜索。
+ **strict**：如果遇到新字段就抛出异常

这个字段可以配置在 根对象 或者 任何对象类型 的字段上。因此可以将 `dynamic=strict` 配置在根对象上，只在指定的内部对象中开启它。

`PUT /my_index`

```json
{
    "mappings": {
        "my_type": {
            "dynamic": "strict",                       // 遇到新字段，my_type 就会抛出异常
            "properties": {
                "title": {"type": "string"},
                "stash": {
                    "type": "object",
                    "dynamic": true                   // 内部对象 stash 遇到新字段就会动态创建新字段
                }
            }
        }
    }
}
```

比如下面的操作是可以正常添加新字段检索的：

`PUT /my_index/my_type/1`

```json
{
    "title": "This doc adds a new field",
    "stash": { "new_field": "Success!" }
}
```

但是对根节点对象 `my_type` 进行同样的操作就会失败：

`PUT /my_index/my_type/1`

```json
{
    "title": "This throws a StrictDynamicMappingException",
    "new_field": "Fail!"
}
```

## 自定义动态映射

### 日期检测

当 es 遇到一个新的字符串，它会检测这个字段是否包含一个可识别的日期，比如 `2014-01-01`。如果它像日期，这个字段就会被作为 `date` 类型添加。否则，会作为 `string` 类型添加。

`{"note": "2014-01-01"}` 会被识别为 `date` 类型，下一个存储进来的文档长这样 `{"note": "Logged out"}` ，这个不合法的日期就会造成一个异常。日期检测可以通过在根对象上设置 `date_detection=false` 来关闭。

`PUT /index`

```json
{
    "mappings": {
        "my_type": {
            "date_detection": false
        }
    }
}
```

那么这个映射就会被当成 `string` 类型，这样如果你始终需要一个 `date` 字段，必须手动添加。判断字符串为日期的规则通过设置 `dynamic_date_formates settings` 就可以。

### 动态模版

使用 `dynamic_templates`，控制新生成的字段的映射。每个模版都有一个 **名称**，可以用来描述这个模版的用途。一个 **mapping** 用来指定映射应该怎么使用。**至少一个参数** 来定义这个模版适用于哪个字段。模版会 **按照顺序** 进行检测，第一个匹配的模版会被启用。

**我们可以给 string 类型字段定义两个模版：**

+ `es`：以 `_es` 结尾的字段名需要使用 `spanish` 分词器。
+ `en`：所有其它字段使用 `english` 分词器。

`PUT /my_index`

```json
{
    "mappings": {
        "my_type": {
            "dynamic_templates": [
                { "es": {
                      "match":              "*_es",        // 匹配字段名以 _es 结尾的字段
                      "match_mapping_type": "string",      // 这个字段允许你应用模版到特定类型的字段上
                      "mapping": {
                          "type":           "string",
                          "analyzer":       "spanish"
                      }
                }},
                { "en": {
                      "match":              "*",           // 匹配其它所有拥有字符串类型的字段
                      "match_mapping_type": "string",
                      "mapping": {
                          "type":           "string",
                          "analyzer":       "english"
                      }
                }}
            ]
}}}
```

## 缺省映射

通常，一个索引中的所有类型共享相同的字段和设置。 `_default_` 映射更加方便地指定通用设置，而不用每次创建新类型时都要重复设置。`_default_` 映射是新类型的模版。也就是，设置了 `_default_` 映射之后创建的所有类型都会应用这些缺省的设置，除非类型在自己的映射中明确覆盖这些设置。

`PUT /my_index`

 ```json
{
    "mappings": {
        "_default_": {                     // 使用 _default_ 映射为所有的类型都禁用 _all 字段(这种用法没有太明白是什么意思)
            "_all": { "enabled":  false }
        },
        "blog": {                          // 只在 blog 字段中启用
            "_all": { "enabled":  true  }
        }
    }
}
 ```

## 重新索引你的数据

可以增加新的类型到索引中，也可以增加新的字段到类型中。但是 **不能** 添加新的分析器或者对现有的字段做改动。如果非要进行这些改动，就要 **重新索引**，用新的设置创建新的索引，并且把文档从旧的索引复制到新的索引。

**用 scroll 从旧的索引检索批量文档，然后用 bulk api 把文档推送到新的索引中去。** 从 v2.3.0 开始，**Reindex api 被引入**，它可以对文档重建索引，且不需要任何插件或者外部工具。

`GET /old_index/_search?scroll=1m`

```json
{
    "query": {
        "range": {
            "date": {
                "gte":  "2014-01-01",          // 按时间过滤可以把大的重建索引分成小的任务
                "lt":   "2014-02-01"
            }
        }
    },
    "sort": ["_doc"],
    "size":  1000
}
```

## 索引别名和零停机

**索引别名** 就像一个快捷方式 或 软连接，可以指向一个或多个索引，也可以给任何一个需要索引名的 API 来使用。**别名** 允许我们：

+ 在运行的集群中可以无缝地从一个索引切换到另一个索引。
+ 给多个索引分组。
+ 给索引的一个子集创建视图。

**别名 可以在 零停机下 从旧索引切换到新索引。**

假设现在有一个 `my_index` 索引，事实上，`my_index` 是一个指向真实索引 `my_index_v1`。

```json
PUT /my_index_v1 
PUT /my_index_v1/_alias/my_index 
```

可以检测这个别名具体指向的是哪一个索引。

`GET /*/_alias/my_index`

或者哪些别名指向这个索引

`GET /my_index_v1/_alias/*`

两者都会返回下面的结果

```json
{
    "my_index_v1" : {
        "aliases" : {
            "my_index" : { }
        }
    }
}
```

这时我们想修改 `my_index_v1` 的映射，但又不能修改现有字段的的映射，因此只好重新索引数据。首先用新映射创建 `my_index_v2`。

`PUT /my_index_v2`

```json
{
    "mappings": {
        "my_type": {
            "properties": {
                "tags": {
                    "type":   "string",
                    "index":  "not_analyzed"
                }
            }
        }
    }
}
```

然后我们将数据从 `my_index_v1` 索引到 `my_index_v2`。

```json
PUT /my_index_v2/_alias/my_index 
```

但是上面的操作，是将 `my_index` 同时指向 `my_index_v1` 和 `my_index_v2`，因此 **添加** 新的索引到别名的 **同时** 需要将就的索引从别名中 **删除**。

`POST /_aliases`

```json
{
    "actions": [
        { "remove": { "index": "my_index_v1", "alias": "my_index" }},
        { "add":    { "index": "my_index_v2", "alias": "my_index" }}
    ]
}
```

**在你的应用中使用别名而不是索引名，然后你就可以在任何时候重建索引，别名的开销很小，应该广泛使用。**

## 分片内部原理

分片，最小的工作单元。

## 使文本可被搜索

es 需要文本字段中的每个单词都可以被搜索，最好的数据结构就是 **倒排索引**，倒排索引包含一个 **有序列表**，列表包含所有文档出现过的 **不重复个体(词项)**，对于每一个词项，包含了所有曾出现过文档的列表。

```
Term  | Doc 1 | Doc 2 | Doc 3 | ...
------------------------------------
brown |   X   |       |  X    | ...
fox   |   X   |   X   |  X    | ...
quick |   X   |   X   |       | ...
the   |   X   |       |  X    | ...
```

倒排索引还会包含 **每一个词项出现过的文档总数**、**在对应的文档中一个具体词项出现的总次数**、**词项在文档中的顺序**、**每个文档的长度**、**所有文档的平均长度**。这些统计信息允许 es 决定哪些词比其它词更加重要，哪些文档比其它文档更加重要。

因此倒排索引需要知道集合中的所有文档，这是需要认识到的关键问题。

早起的全文检索会为整个文档集合建立一个很大的倒排索引并将其写入到磁盘，一旦新的索引就绪，旧的就会被其替换，这样最近的变化便可以被检索到。这里我理解的是，早期的 es 搜索，新建文档要先写入到磁盘中，然后再从磁盘中读出来，或者从缓存中读取。

### 不变性

倒排索引被写入到磁盘后，是永远不可以被改变的。不可变就意味着：

+ 不需要锁。不更新索引就不需要担心多进程修改数据的问题。
+ 一旦索引被读入内核的文件系统缓存，便会留在那里，由于其不变性，只要文件系统缓存中还有足够的空间，大部分的读请求会直接请求内存，对性能有很大的提升。
+ 其它缓存(像 filter 缓存)，在索引的生命周期内始终有效。它们不需要在每次数据改变时被重建，因为数据不会变化。
+ 写入单个大的倒排索引允许数据被压缩，减少磁盘 I/O 和 需要被缓存到内存的索引的使用量。

不过这也对一个索引所能包含的数据量造成了很大的限制，或者对索引可呗更新的频率造成了很大的限制。

## 动态更新索引

**通过增加新的补充索引反应新近的修改，而不是直接重写整个倒排索引。每一个倒排索引都会被轮流查询到，这样将从最早的开始到查询完后再对结果进行合并，就可以解决在不变性的前提下，实现对倒排索引的更新问题了。**

es 的 Java 库引入了按段搜索的概念，**每一个段** 就是一个倒排索引，**提交点** 就是一个列出了所有已知段的文件。新的文档首先被添加到内存索引缓存中，然后写入到一个 **基于磁盘的段**。**一个 Lucene 索引就是 es 中的分片，一个 es 的索引是多个分片的集合。**

逐段搜索会以如下流程进行工作：

+ **新文档**被收集到 **内存索引缓存**
+ 不时地, 缓存被 *提交* 
  + 一个新的段（一个追加的倒排索引）被写入磁盘。
  + 一个新的包含新段名字的 *提交点* 被写入磁盘。
  + 将所有在文件系统缓存中 **等待的写入** 都刷新到 磁盘
+ **内存缓存** 被清空，等待接收新的文档。
+ 这里也没有说清楚是不是每一次新建文档就会被刷新到磁盘，也没有说清楚 缓存被写入到段中是否就可以进行搜索。还是要被 `fsync` 写入到磁盘以后才能被搜索，无语 - -。也不知道是翻译还是什么原因，难道是前面漏看了？

当一个查询被触发，所有已知段 **按顺序被查询**。词项统计会对所有段的结果进行聚合，以保证每个词和每个文档的关联都被准确计算。这种方式可以用相对较低的成本 **将新的文档添加到索引**。

### 删除和更新

段是 **不可改变的**，既不能将文档从旧段中删除，也不能修改旧段来反映文档的更新。取而代之的是，每个提交点会包含一个 **`.del`** 文件，文件中会列出这些被删除文档的段信息。

当一个文档被 “删除” 时，实际上只是在 **`.del`** 文件中 **被标记删除**。一个被标记删除的文档 **仍然可以被查询匹配到**，但它会在最终 **结果被返回前** 从结果集中 **删除**。

文档更新也是类似操作，当一个文档被更新时，旧版本的文档会被标记删除，文档的新版本被索引到一个新段中。两个版本的文档都会被一个查询匹配到，但被删除的那个旧文档在结果集返回的时候就已经被删除了。

## 近实时搜索

按段搜索 的速度 比 使用新索引替换旧索引 的速度要快(这里的速度是指发生变更以后，再到被搜索到的这个时间)，但还是不够快的。从缓存刷新到磁盘成为了瓶颈。**提交一个新段到磁盘需要一个 `fsync` 来确保段被物理性地写入磁盘**，这样断电时才不会发生数据丢失。但是 `fsync` 代价很大，如果每次索引 (新建) 一个文档都去调用一次 `fsync` 的话，就会造成较大的性能问题。

因此，如何才能不要每次新建文档就进行一次 `fsync`, 如下：

+ **新文档** 会被写入到 文件系统缓存中
+ 内存索引缓冲区中的文档会被写入到一个 **可被搜索的** 且在 **文件系统缓存中的** 新段中，但 **不会被提交**。稍后才会被提交。

这种方法比一次提交要好，允许新段被写入和打开，其包含的文档在未进行一次完整提交时便对搜索可见，在不影响性能的前提下可以频繁地执行，

### refresh API

在 es 中，写入和打开一个新段轻量过程叫做 `refresh`。默认情况下，每个分片会每秒自动刷新一次，这就是为什么说 es 是近实时搜索的原因，文档的变化并不是立即对搜索可见，但是 1s 内变为可见。

```json
POST /_refresh 
POST /blogs/_refresh
```

`refresh` 是比 `fsync` 更加轻量的动作，但还是会有性能开销，避免在生产环境中进行使用。可以通过设置 `refresh_interval` 降低索引的刷新频率。

```json
PUT /my_logs
{
  "settings": {
    "refresh_interval": "30s"              // 关闭索引刷新只需要设置值为 -1, 比如上生产之前要创建一个很大的索引，就可以先关掉
  }
}
```

如果写的不是 '30s' 而是 '30'，则含义为 30ms, 这样会造成你系统的崩溃。

## 持久化变更

`fsync` 的操作依旧不能省略，我们需要确保文件被写入到磁盘中。es 在启动或重新打开一个索引的过程中，使用提交点来判断哪些段隶属于当前分片。即使通过 `refresh` 实现了近实时的搜索，我们仍需要经常进行完整提交确保能从失败中恢复数据。

那么在上一次完整提交之后，这一次完整提交之前，发生了故障怎么办呢？

es 增加了一个 `translog`，也就是 事务日志，它会对每一次 es 操作进行记录，流程如下。

+  一个文档被索引之后，就会被添加到内存缓冲区，然后追加到 `translog` 上。
+ `refresh` 使缓冲区的文档写入到新段中，注意这里并没有进行 `fsync` 的动作。写入到新段以后的文档就可以被索引了，内存缓冲区会被清空，`translog` 不会被清空的。
+ 事务日志不断积累文档，循环步骤2
+ 每隔一段时间，段会被全量提交，一个新的 `translog` 会被创建。
  + 所有内存缓冲区的文档都会被写入一个新的段
  + 缓冲区被清空
  + 一个提交点被写入硬盘
  + 文件系统缓存通过 `fsync` 被 `flush`
  + 老的 `translog` 会被删除

`translog` 实际上提供所有 **还没有** 被刷到磁盘上的操作的一个 **持久化** 记录。当 es 启动时，它会从 disk 中使用最后一个提交点去恢复已知的段，并且会 **重放** `translog` 中所有在最后一次提交之后发生的变更操作。

当你试着通过 ID 查询、更新、删除一个文档，它会尝试从相应的段中检索任何最近的变更，这就意味着它总是能实时地获取到文档的最新版本。

### flush API

执行一个提交并截断 `translog` 的行为在 es 称为一次 `flush`。分片每 30min 被自动 `flush`，或者 `translog` 过大的时候也会刷新。这些阈值可以自行配置。

```json
POST /blogs/_flush 

POST /_flush?wait_for_ongoing 
```

在重启节点或关闭索引之前执行 `flush` 有益于你的索引，当 es 尝试恢复或重新打开一个索引，需要重放 `translog` 中的所有操作，因此，日志越短，恢复越快。

### translog 有多安全？

在文件被 `fsync` 到磁盘前，被写入的文件在重启之后就会丢失。默认 `translog` 每 5s 就会被 `fsync` 刷新到 disk， 或者在每次写请求完成以后执行。这个过程在主分片和副本分片上都会发生。也就是说，整个请求被 `fsync` 到主分片和副本分片的 `translog` 之前，客户端都不会得到 200 的响应。

后面还有一个功能没看懂，暂时不介绍了。

## 段合并

由于自动刷新流程每秒会创建一个新的段，这样会导致短时间内段的数量暴增。每一个段都会消耗文件句柄、内存、CPU 运行周期。更重要的是每个搜索请求都必须轮流检查每个段，所以段越多，搜索也会越慢。

es 会在 **后台** 进行 **段合并** 来解决这个问题。小的段被合并到大的段，然后大的段再被合并到更大的段。这个过程发生在 进行索引 和 搜索 时。

段合并的时候会将哪些旧的 **已经删除文档** 从文件系统中 **清除**。不会被拷贝到新的大段中。

具体流程如下：

+ 当索引的时候，`refresh` 操作会创建新的段并将段打开以供搜索使用
+ 合并进程选择一小部分大小相似的段，并且在后台将它们合并到更大的段中，这并不会中断索引和搜索。
+ 一旦合并结束，老的段会被删除。新的段会被 `flush` 到磁盘，然后被打开，用于搜索，老的段会被删除。

**合并段需要消耗大量的 I/O 和 CPU 资源。任其发展会影响搜索性能，因此 es 在默认情况会对合并流程进行资源限制。**

### optimize API

这个 API 用于强制合并，会将一个分片强制合并到 `max_num_segments` 大小的段数目。

`POST /logstash-2014-10/_optimize?max_num_segments=1` 意为将每一个分片合并为一个单独的段，节省资源，且使搜索更加快速。

**但是**，这个 API 触发段合并的时候不会受到任何资源上的限制，可能会消耗掉你节点上全部的 I/O 资源，使没有多余的资源处理 搜索请求。集群可能会失去响应。使用的时候应该先把索引挪到 **安全的节点**，再执行。

## 结构化搜索

**结构化搜索** 是指有关探询那些具有 **内在数据结构** 的过程。结构化查询中，得到的结果 **非是即否**，要么存在于集合之中，要么存在于集合之外，不关心文件或相关度或评分，简单的对文档 **包括** 或者 **排除** 处理。结构化文本来说，一个值要么相等，要么不等，不存在 **更似** 这种概念。

## 精确值查找

使用精确值查找时，我们会使用过滤器（filters）,过滤器的执行速度 **非常快**，**不会计算相关度**，**很容易被缓存**。请尽可能多的，使用过滤式查询。

### term 查询数字

`term` 查询可以处理 numbers、booleans、dates 以及 text。

在对 numbers、booleans、dates 查找时可以直接使用下列用法。

```json
{"term": {"price": 20}}
```

在对 text 使用 `term` 查询时，先修改该字段的 index 为 not_analyzed, 否则可能导致被分词器分词导致查询不到指定的文档。如果有问题的话我们也可以使用 `analyzed` API 查看分析器将字段分析成了什么样。

```json
GET /my_store/_analyze
{
  "field": "productID",
  "text": "XHDK-A-1293-#fJ3"
}
```

更改映射需要先删除再重建

```json
DELETE /my_store 

PUT /my_store 
{
    "mappings" : {
        "products" : {
            "properties" : {
                "productID" : {
                    "type" : "string",
                    "index" : "not_analyzed" 
                }
            }
        }
    }

}
```

### 内部过滤器的操作

es 会在运行非评分查询的时候执行多个操作：

+ **查找匹配文档**

+ **创建 bitset**

  过滤器会创建一个 bitset(包含 0 和 1 的数组)，它描述了哪个文档会包含该 term。匹配的文档则该标识位为 1。

+ **迭代 bitsets**

  一旦为每个查询生成了 bitsets, es 会循环迭代 bitsets 从而找到满足过滤条件的所有匹配文档的几个。执行顺序是启发式的，一般会先迭代 稀疏的 bitsets。因为这样可以过滤掉大量的文档。

+ **增量使用计数**

  主要目的是只缓存将来会使用到的，减少浪费内存资源。

  es 会为每个索引跟踪保留查询使用的历史状态，如果查询在最近的 256 次中会被用到，才会被缓存到内存中。当 bitset 被缓存后，那些低于 10000 个文档的段 不会放入缓存，因为有段合并，它们即将会消失。

## 组合过滤器

当需要过滤多个值或者字段，需要使用 bool 过滤器，这是个 **复合过滤器(compound filter)**。他可以接受其它过滤器作为参数，并将这些过滤器结合成个 布尔组合。

### 布尔过滤器

组合多查询那一章已经讲过，不过多赘述了。

```json
GET /my_store/products/_search
{
   "query" : {
      "filtered" : {           // 貌似这个可以代替掉 bool-filter, 可以少写两层
         "filter" : {
            "bool" : {
              "should" : [
                 { "term" : {"price" : 20}}, 
                 { "term" : {"productID" : "XHDK-A-1293-#fJ3"}} 
              ],
              "must_not" : {
                 "term" : {"price" : 30} 
              }
           }
         }
      }
   }
}
```

### 嵌套布尔过滤器

我们还可以将 bool 过滤器 放在其它的 bool 过滤器内部。

```sql
SELECT document
FROM   products
WHERE  productID      = "KDKE-B-9947-#kL5"
  OR (     productID = "JODL-X-1937-#pV7"
       AND price     = 30 )
```

转换一下就是

```json
GET /my_store/products/_search
{
   "query" : {
      "filtered" : {
         "filter" : {
            "bool" : {
              "should" : [
                { "term" : {"productID" : "KDKE-B-9947-#kL5"}}, 
                { "bool" : { 
                  "must" : [
                    { "term" : {"productID" : "JODL-X-1937-#pV7"}}, 
                    { "term" : {"price" : 30}} 
                  ]
                }}
              ]
           }
         }
      }
   }
}
```

## 查找多个精确值

`terms` 的用法之前也介绍过，不再赘述。

```json
{ "tags" : ["search"] }
{ "tags" : ["search", "open_source"] }
```

假如有两条文档，es 会在倒排索引中查找 `{ "term" : { "tags" : "search" } }` 包含 `search` 的所有文档。然后构造一个 bitsets, 这两个文档均会被标记为 1，最后作为结果进行返回。

**因此 terms 和 term 都是必须包含操作，而不是必须精确相等操作。**

### 精确相等

如果一定期望得到整个字段完全相等的行为，**最好的方式** 是增加并索引另一个字段，这个字段用以存储该字段包含词项的数量。如：

```json
{ "tags" : ["search"], "tag_count" : 1 }
{ "tags" : ["search", "open_source"], "tag_count" : 2 }
```

进行如下查询即可：

```json
GET /my_index/my_type/_search
{
    "query": {
        "constant_score" : {
            "filter" : {
                 "bool" : {
                    "must" : [
                        { "term" : { "tags" : "search" } }, 
                        { "term" : { "tag_count" : 1 } } 
                    ]
                }
            }
        }
    }
}
```

## 范围

基础用法搜索 `range` 即可，不再赘述。

### 日期范围

日期计算只要在某个日期后面加上一个 双管符号(||) 紧跟一个数学表达式即可。

```json
"range" : {
    "timestamp" : {
        "gt" : "2014-01-01 00:00:00",
        "lt" : "2014-01-01 00:00:00||+1M"     // 小于 2014-02-01 00:00:00
    }
}
```

### 字符串范围

字符串范围采用 **字典顺序(5,50,6,a,ab,abb,abc,b)** 或 **字母顺序**。倒排索引中的词项采取的就是字典顺序排列。这也是字符串范围可以使用这个顺序来确定的原因。

```json
"range" : {
    "title" : {
        "gte" : "a",
        "lt" :  "b"
    }
}
```

es 内部实际为范围查询内的 **每一个词项** 都执行了 `term` 过滤器，这会比日期或数字的范围过滤都 **慢很多**。唯一词项越多，字符串范围计算会越慢。

## 处理 Null 值

如果某个字段没有值，它将 **不会被存入** 倒排索引中，它不会拥有任何 `token`，无法在倒排索引中表现。

也就是说，不论是 **`null`** 还是 **`[]`**  还是 **`[null]`** 这些都是等价的，都无法被存入 倒排索引。

如果某些文档甚至都 **没有** 我们 **指定的字段**，也是不会存在于 **某个字段** 的 **倒排索引中**的。

### 存在查询

`exists` 查询会返回那些在指定字段有任何值的文档。

```json
GET /my_index/posts/_search
{
    "query" : {
        "constant_score" : {
            "filter" : {
                "exists" : { "field" : "tags" }
            }
        }
    }
}
```

### 缺失查询

`missing` 查询会返回某个 **无值字段** 的文档。

```json
GET /my_index/posts/_search
{
    "query" : {
        "constant_score" : {
            "filter": {
                "missing" : { "field" : "tags" }      // 会返回没有 tags 字段的文档 和 tags 字段没有值的文档
            }
        }
    }
}
```

### 当 null 的意思是 null

有时候我们需要区分一个字段 是没有值，还是被显示设置成了 null。可以将显示的 null **替换**为指定的 占位符。在为 `string`、`numeric`、`boolean`、`date` 字段指定映射时，可以为之设置 `null_value`，用以处理显示 `null` 值的情况。不过即使如此还是会将一个没有值的字段从倒排索引中排除。

当选择合适的 `null_value` 空值的时候，**需要保证以下几点**：

- 它会匹配字段的类型，我们不能为一个 `date` 日期字段设置字符串类型的 `null_value` 。
- 它必须与普通值不一样，这可以避免把实际值当成 `null` 空的情况。

### 对象上的存在和缺失

`exists` 和 `missing` 都可以进行嵌套结构的对象查询。

```json
{
   "name" : {
      "first" : "John",
      "last" :  "Smith"
   }
}
```

和

```json
{
   "name.first" : "John",
   "name.last"  : "Smith"
}
```

如果

```json
{
    "exists" : { "field" : "name" }
}
```

实际上执行的是

```json
{
    "bool": {
        "must": [
            { "exists": { "field": "name.first" }},
            { "exists": { "field": "name.last" }}
        ]
    }
}
```

也就是说，只有 first 和 last 两个字段都为空，才会认为不存在。文档上写的是 `should` 似乎不对吧。

## 关于缓存

过滤器的核心是采用 bitset 记录与过滤器匹配的文档，es 会积极地将这些 bitset 缓存起来，bitset 可以复用任何已使用过的相同过滤器，无需再次计算。这些缓存是智能的，以增量方式更新，只将新文档加入已有的 bitset，过滤器是实时的，无需担心缓存过期的问题。

### 独立的过滤器缓存

独立于它所属搜索请求其它部分的，意味着一旦被缓存，一个查询可以被用作多个搜索请求。

```json
// 过滤器1 和 过滤器2 会使用同一个 bitset
GET /inbox/emails/_search
{
  "query": {
      "constant_score": {
          "filter": {
              "bool": {
                 "should": [
                    { "bool": {                   
                          "must": [
                             { "term": { "folder": "inbox" }},   // 过滤器1
                             { "term": { "read": false }}
                          ]
                    }},
                    { "bool": {                   
                          "must_not": {
                             "term": { "folder": "inbox" }       // 过滤器2，会使用 过滤器1 的 bitset 
                          },
                          "must": {
                             "term": { "important": true }
                          }
                    }}
                 ]
              }
            }
        }
    }
}
```

### 自动缓存行为

**现象：**

如果 `term` 过滤的字段 `user_id` 有上百万用户，每个具体 `user_id` 出现的概率很小，为了这样的过滤器缓存 bitset 旧不是很好的选择。

**解决方法：**

es 会使用 **基于使用频次自动缓存查询**。如果一个非评分查询在最近的 256 次查询中被使用过，那么这个查询就会被作为缓存的 **候选**。并不是所有的片段都能保证缓存 `bitset`。只有 **文档数量超过 10000**，或 **超过总文档数量的 3%** 才会被缓存。因为小段很快会被合并，缓存意义不大。

**bitset 剔除**：

一旦缓存满了，最近最少使用的过滤器就会被剔除。

## 基于词项与基于全文

**基于词项的查询**

`term` 和 `fuzzy` 这样的底层查询 **不需要** 分析阶段，**只对单个词项** 进行操作。`term` 查询只对倒排索引的词项精确匹配，不会对词的多样性进行处理，如 foo 和 Foo 的区别。

**基于全文的查询**

`match` 或 `query_string` 这样的查询是高层查询。

+ 如果查询的是 `date`、`integer`，它们会将查询字符串作为 `date` 和 `integer` 进行判断。
+ 如果查询一个 `not_analyzed` 字符串字段，则会将整个查询字符串作为单个词项对待。
+ 如果查询一个 `analyzed` 全文字段，则会将查询字符串传递到一个合适的分析器，然后生成一个供查询的词项列表。

## 匹配查询

`match` 是一个 **高级** 的 **全文查询**，意味着既可以处理全文字段，又可以处理精确字段。**主要应用场景** 是全文搜索。

### 索引一些数据

```json
DELETE /my_index 

PUT /my_index
{ "settings": { "number_of_shards": 1 }} 

POST /my_index/my_type/_bulk
{ "index": { "_id": 1 }}
{ "title": "The quick brown fox" }
{ "index": { "_id": 2 }}
{ "title": "The quick brown fox jumps over the lazy dog" }
{ "index": { "_id": 3 }}
{ "title": "The quick brown fox jumps over the quick dog" }
{ "index": { "_id": 4 }}
{ "title": "Brown fox brown dog" }
```

### 单个词查询

```json
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "title": "QUICK!"
        }
    }
}
```

es 内部 `match` 查询步骤为：

+ **检查字段类型**

  `title` 字段是 `analyzed` 类型的，因此查询字符串也需要被分析器分析。

+ **分析查询字符串**

  `QUICK!` 经过标准分析器出来的结果是 `quick`，因为只有一个单词项，所以底层执行的是单个 `term` 查询。

+ **查找匹配文档**

  `term` 查询在倒排索引中查找 `quick` 然后获取符合数据的文档，结果是 文档1，2，3

+ **为每个文档评分**

  用 `term` 查询计算每个文档相关度评分 `_score`。采用的是 TF/IDF 相似性算法，前文有简单的介绍了。

## 多词查询

```json
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "title": "BROWN DOG!"
        }
    }
}
```

因为 `match` 底层会构造成

```json
{
    "query": {
        "bool": {
          	"should": [
              {"term": {"title": "BROWN"}},
              {"term": {"title": "DOG"}}
            ]
        }
    }
}
```

也就是说只要 任何一个文档里面包含任何一个 `match` 里面任何一个词项，就能被匹配到，匹配到的词项越多，文档就越相关。

### 提高精度

如果想要搜索的是 `BROWN AND DOG`，而不是 `BROWN OR DOG`。只需要使用下面：

```json
GET /my_index/my_type/_search
{
    "query": {
        "match": {
            "title": {      
                "query":    "BROWN DOG!",
                "operator": "and"                // es 可以接受 operator 作为输入参数，默认情况下是 or
            }
        }
    }
}
```

### 控制精度

如果我们既想包含那些可能相关的文档，同时排除那些不太相关的，`match` 支持 `minimum_should_match` 最小匹配参数，可以指定必须匹配的词项数用来表示一个文档是否相关。可以设置为某个具体数字，更常用的做法是将其设置为一个百分数，因为我们无法控制用户搜索时输入的单词数量。

```json
GET /my_index/my_type/_search
{
  "query": {
    "match": {
      "title": {
        "query": "quick brown dog",
        "minimum_should_match": "75%"
      }
    }
  }
}
```

## 组合查询

bool 查询除了决定一个文档是否应该被包括在结果中，还会计算文档的相关程度。

```json
GET /my_index/my_type/_search
{
  "query": {
    "bool": {
      "must":     { "match": { "title": "quick" }},
      "must_not": { "match": { "title": "lazy"  }},
      "should": [
                  { "match": { "title": "brown" }},
                  { "match": { "title": "dog"   }}
      ]
    }
  }
}
```

### 评分计算

`bool` 查询会为每个文档计算相关度评分 `_score`，再将所有匹配的 `must` 和 `should` 语句的 `_score` 求和，最后除以 `must` 和 `should` 语句的总数。`must_not` 不会影响评分，作用只是将不相关的文档排除。

### 控制精度

所有 `must` 语句必须匹配，所有 `must_not` 语句都必须不匹配，但有多少 `should` 语句应该匹配呢？默认情况下，没有 `should` 语句是必须匹配的，只有一个例外：那就是当没有 `must` 语句的时候，至少有一个 `should` 语句必须匹配。

可以通过 `minimum_should_match` 控制需要匹配的 `should` 语句的数量，既可以是一个数字，也可以是一个百分比。

```json
GET /my_index/my_type/_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title": "brown" }},
        { "match": { "title": "fox"   }},
        { "match": { "title": "dog"   }}
      ],
      "minimum_should_match": 2 
    }
  }
}
```

这个查询结果会将所有满足以下条件的文档返回： `title` 字段包含 `"brown" AND "fox"` 、 `"brown" AND "dog"` 或 `"fox" AND "dog"` 。如果有文档包含所有三个条件，它会比只包含两个的文档更相关。

## 查询语句提升权重

如何让匹配某些查询语句的文档获得更高的权重呢？可以通过指定 `boost` 来控制任何查询语句的相对的权重。

```json
GET /_search
{
    "query": {
        "bool": {
            "must": {                // 默认 boost 值为, boost 值更高的更为重要，匹配的文档会拥有更高的评分
                "match": {  
                    "content": {
                        "query":    "full text search",
                        "operator": "and"
                    }
                }
            },
            "should": [
                { "match": {
                    "content": {
                        "query": "Elasticsearch",
                        "boost": 3 
                    }
                }},
                { "match": {
                    "content": {
                        "query": "Lucene",
                        "boost": 2 
                    }
                }}
            ]
        }
    }
}
```

boost 参数被用来提升一个语句的相对权重(>1)，也可以降低相对权重([0, 1))，这种提升或降低都不是线性的。更高的 `boost` 值为我们带来更高的评分 `_score`。

## 控制分析

查询只能查找倒排索引表中真实存在的项，保证 **文档再索引时与查询字符串在搜索时应用相同的分析过程** 非常重要，这样查询的项才能够匹配倒排索引中的项。

为 `my_index` 新增一个字段：

```json
PUT /my_index/_mapping/my_type
{
    "my_type": {
        "properties": {
            "english_title": {
                "type": "string",
                "analyzer": "english"
            }
        }
    }
}
```

也就是说，使用 `term` 查询 `fox` 时，`english_title` 字段会被匹配，但是 `title` 字段不会。

```json
GET /my_index/_analyze
{
  "field": "my_type.title",   
  "text": "Foxes"                         // 默认使用 standard 标准分析器，返回 `foxes`
}

GET /my_index/_analyze
{
  "field": "my_type.english_title",       // 英语分析器 返回的词项是 `fox`
  "text": "Foxes"
}
```

`match` 查询这样的高层查询知道字段映射的关系，能为每个被查询的字段应用正确的分析器，可以使用 `validate-query API` 查看这个行为。

```json
GET /my_index/my_type/_validate/query?explain
{
    "query": {
        "bool": {
            "should": [
                { "match": { "title":         "Foxes"}},
                { "match": { "english_title": "Foxes"}}
            ]
        }
    }
}
```

返回结果为：`(title:foxes english_title:fox)`

### 默认分析器

分析器可以从三个层面进行定义：

+ 按字段
+ 按索引
+ 全局缺省

es 会按照以下顺序依次处理，直到它找到能够使用的分析器。

**索引时的顺序如下：**

+ 字段映射里定义的 `analyzer`
+ 索引设置中名为 `default` 的分析器，缺省配置
+ `standard` 标准分析器，缺省配置

**搜索时的顺序如下：**

+ 查询自己定义的 `analyzer`

+ 字段映射里定义的 `analyzer`
+ 索引设置中名为 `default` 的分析器，默认为
+ `standard` 标准分析器

有时，在索引时和搜索时使用不同的分析器是合理的，因为我们可能想为同义词建索引(例如，quick 出现的地方，同时也为 fast、rapid、speedy 创建)，但是在搜索的时候不需要搜索所有的同义词，只需要搜索单个词即可。

为此，es 支持一个可选的 **`search_analyzer`** 映射，**仅会应用**于搜索时。还有一个等价的 **`default_search`** 映射，用以指定索引层的默认配置。

**所以搜索时完整的顺序会是：**

1. 查询自己定义的 `analyzer`，否则
2. 字段映射里定义的 `search_analyzer`，否则
3. 字段映射里定义的 `analyzer`，否则
4. 索引设置中名为 `default_analyzer` 的分析器，默认为
5. 索引设置中名为 `default` 的分析器，默认为
6. `standard` 标准分析器

### 分析器配置实践

最简单的途径就是在创建索引或增加类型映射的时候，为每个全文字段设置分析器。保持尽量简单的原则。为绝大部分的字段设置你想指定的 default 默认分析器，然后在字段级别设置中，为某一两个字段配置需要指定的分析器。

**对于和时间相关的日志数据，通常做法是每天自行创建索引，由于这种方式不是从头创建的索引，仍可以用索引模版为新建的索引指定配置和映射。**

## 被破坏的相关度

+ 问题：

用户索引了一些文档，运行了一个简单的查询，然后发现明显低的相关度的结果出现在了高相关度的结果之上。

+ 原因：

设想，我们在两个主分片上创建了索引和总共 10 个文档，其中 6 个文档有单词 `foo` 。可能是分片 1 有其中 3 个 `foo` 文档，而分片 2 有其中另外 3 个文档，换句话说，所有文档是均匀分布存储的。

在 [什么是相关度？](https://www.elastic.co/guide/cn/elasticsearch/guide/current/relevance-intro.html)中，我们描述了 Elasticsearch 默认使用的相似度算法，这个算法叫做 *词频/逆向文档频率* 或 TF/IDF 。词频是计算某个词在当前被查询文档里某个字段中出现的频率，出现的频率越高，文档越相关。 *逆向文档频率* 将 *某个词在索引内所有文档出现的百分数* 考虑在内，出现的频率越高，它的权重就越低。

但是由于性能原因， Elasticsearch 不会计算索引内所有文档的 IDF 。相反，每个分片会根据 *该分片* 内的所有文档计算一个本地 IDF 。

因为文档是均匀分布存储的，两个分片的 IDF 是相同的。相反，设想如果有 5 个 `foo` 文档存于分片 1 ，而第 6 个文档存于分片 2 ，在这种场景下， `foo` 在一个分片里非常普通（所以不那么重要），但是在另一个分片里非常出现很少（所以会显得更重要）。这些 IDF 之间的差异会导致不正确的结果。

在实际应用中，这并不是一个问题，本地和全局的 IDF 的差异会随着索引里文档数的增多渐渐消失，在真实世界的数据量下，局部的 IDF 会被迅速均化，所以上述问题并不是相关度被破坏所导致的，而是**由于数据太少。**

+ 解决方法：

**因此为了避免这种情况，我们可以只在主分片上创建索引，如果只有一个分片，那么本地的 IDF 就是 全局的 IDF**。

**在搜索请求后加上 `?search_type=dfs_query_then_fetch` dfs 是指分布式频率搜索，让 es 先分别获得每个分片本地的 IDF，然后根据结果再计算整个索引的全局 IDF。**

不要在生产环境使用，因为只要有足够的数据保证词频是均匀分布的，就没有理由给每个查询额外加上 DFS 这步。

## 多字符串查询

**`bool`** 查询采取的是 `more matches is better` 匹配的 **越多越好** 的方式。`bool` 查询运行每个 `match` 查询，再把评分加在一起，将结果与所有匹配的语句数量相乘，最后除以所有语句的数量。**处于同一层的语句具有相同的权重。**

```json
GET /_search
{
  "query": {
    "bool": {
      "should": [
        { "match": { "title":  "War and Peace" }},           // 1
        { "match": { "author": "Leo Tolstoy"   }},           // 2
        { "bool":  {                                         // 假如子句 match 在外层查询中，则 1，2 比重就会变成 1/4, 而现在是 1/3
          "should": [
            { "match": { "translator": "Constance Garnett" }},
            { "match": { "translator": "Louise Maude"      }}
          ]
        }}
      ]
    }
  }
}
```

### 语句的优先级

使用 `boost` 参数，要获取最佳值最简单的方式就是不断试错。比较合理的值是在 1~10 之间，也可能是 15。如果要指定更高的值，将不会对最终的评分结果产生更大的影响，因为评分是被归一化的。使用方式前文有，不赘述了。

## 单字符串查询

有些用户期望将所有的搜索项堆积到单个字段中，并期望应用程序能为他们提供正确的结果。多字段搜索的表单通常被称为 高级查询。

## 最佳字段

假设有个网站允许用户搜索博客内容，现在有两篇文章是这样的：

```json
PUT /my_index/my_type/1
{
    "title": "Quick brown rabbits",
    "body":  "Brown rabbits are commonly seen."
}

PUT /my_index/my_type/2
{
    "title": "Keeping pets healthy",
    "body":  "My quick brown fox eats rabbits on a regular basis."
}
```

内部实现肯定是：

```json
{
    "query": {
        "bool": {
            "should": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}
```

但是最后会发现 文档1的评分会比文档2更加高，可是文档2包含了两个词，文档1只包含了一个词。

**`bool` 查询评分逻辑：**

1. 它会执行 `should` 语句中的两个查询。
2. 加和两个查询的评分。
3. 乘以匹配语句的总数。
4. 除以所有语句总数（这里为：2）。

可以看出本例中，title 和 body 字段是 **互相竞争** 的关系，需要找到单个 **最佳匹配** 的字段。即，将 **最佳匹配** 字段的评分作为查询的整体评分，这样文档1的相关度就会高一些。也就是同时包含 `brown` 和 `fox` 的单个字段的相关度会更加高。

### dis_max 查询

最大化查询（*Disjunction Max Query*）会想任何与任一查询匹配的文档作为结果返回，但是只将 **最佳匹配** 的评分作为查询的评分结果分会。

```json
{
    "query": {
        "dis_max": {                                   // disjunction == or
            "queries": [
                { "match": { "title": "Brown fox" }},
                { "match": { "body":  "Brown fox" }}
            ]
        }
    }
}
```

## 最佳字段查询调优

```json
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ]
        }
    }
}
```

```json
{
  "hits": [
     {
        "_id": "1",
        "_score": 0.12713557, 
        "_source": {
           "title": "Quick brown rabbits",
           "body": "Brown rabbits are commonly seen."
        }
     },
     {
        "_id": "2",
        "_score": 0.12713557, 
        "_source": {
           "title": "Keeping pets healthy",
           "body": "My quick brown fox eats rabbits on a regular basis."
        }
     }
   ]
}
```

`dis_max` 会让这俩文档评分一致，单个字段都只匹配了一个词项，但是显然文档2的评分应该更高。

### tie_broker 参数

```json
{
    "query": {
        "dis_max": {
            "queries": [
                { "match": { "title": "Quick pets" }},
                { "match": { "body":  "Quick pets" }}
            ],
            "tie_breaker": 0.3     // 0 表示使用 dis_max 最佳匹配语句的普通逻辑，1表示所有匹配到的语句同等重要，最合理的值应该与0接近 [0.1, 0.4]
        }
    }
}
```

`tie_broker` 参数提供了一种 `dis_max` 和 `bool` 之间的这种选择，它的 **评分方式** 如下：

1. 获得最佳匹配语句的评分 `_score` 。
2. 将其他匹配语句的评分结果与 `tie_breaker` 相乘。
3. 对以上评分求和并规范化。

**它会考虑所有匹配的语句，但是最佳匹配语句依旧占最终结果的很大一部分。**

## multi_match 查询

```json
{
  "dis_max": {
    "queries":  [
      {
        "match": {
          "title": {
            "query": "Quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
      {
        "match": {
          "body": {
            "query": "Quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
    ],
    "tie_breaker": 0.3
  }
}
```

```json
{
    "multi_match": {
        "query":                "Quick brown fox",
        "type":                 "best_fields",       // 默认值，best_fields 、most_fields 和 cross_fields
        "fields":               [ "title", "body" ],
        "tie_breaker":          0.3,
        "minimum_should_match": "30%" 
    }
}
```

### 查询字段名称的模糊匹配

```json
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": "*_title"
    }
}
```

### 提升单个字段的权重

可以使用 `^` 字符语法为单个字段提升权重，在字段名称的末尾添加 `^boost` ，其中 `boost` 是一个浮点数：

```json
{
    "multi_match": {
        "query":  "Quick brown fox",
        "fields": [ "*_title", "chapter_title^2" ] 
    }
}
```

## 后面还有几章，但是内容和相关度有关，目前还用不到评分特性，暂时不记录了

## 短语匹配

`match_phrase` 查询首先将查询字符串解析成一个词项列表，然后对这些词项进行搜索，只保留那些包含 **全部搜索** 的词项，以及 **位置与搜索词项相同** 的文档。

```json
GET /my_index/my_type/_search
{
    "query": {
        "match_phrase": {
            "title": "quick brown fox"
        }
    }
}
```

等价于另一种写法

```json
"match": {
    "title": {
        "query": "quick brown fox",
        "type":  "phrase"
    }
}
```

### 词项的位置

当一个字符串被分词后，这个分析器不但会返回一个词项列表，而且还会返回各词项在原始字符串中的 **位置关系**。

位置信息可以被存储在倒排索引中，因此 `match_phrase` 查询这类对词语位置敏感的查询，可以利用位置信息去匹配包含所有查询词项，且各词项的顺序与搜索指定一致的文档，且 **中间不夹杂其它词项**。

### 什么是短语

一个被认定为和短语 `quick brown fox` 匹配的文档，必须满足以下这些要求：

- `quick` 、 `brown` 和 `fox` 需要全部出现在域中。
- `brown` 的位置应该比 `quick` 的位置大 `1` 。
- `fox` 的位置应该比 `quick` 的位置大 `2` 。

本质上来讲，`match_phrase` 查询是利用一种低级别的 `span` 查询族（query family）去做词语位置敏感的匹配。 Span 查询是一种词项级别的查询，所以它们没有分词阶段；它们只对指定的词项进行精确搜索。

## 混合起来

获取我们想要的是包含 "quick brown fox" 的文档也能匹配 "quick fox"。如下所述我们有这样一个文档。

```
            Pos 1         Pos 2         Pos 3
-----------------------------------------------
Doc:        quick         brown         fox
-----------------------------------------------
Query:      quick         fox
Slop 1:     quick                 ↳     fox
```

```json
GET /my_index/my_type/_search
{
    "query": {
        "match_phrase": {
            "title": {
            	"query": "quick fox",
            	"slop":  1              // 告诉 match_phrase 查询此条相隔多远时仍然能将文档视为匹配
            }                         
        }
    }
}
```

使用了 `slop` 短语匹配中的所有单词 **必须出现**，但是这些单词不必为了匹配而按 **相同的序列排列**。有了足够大的 `slop` 值，单词可以按照任意顺序排列。

"quick fox" 和 "fox quick" 相差的 slop 就是 2。quick 必须至少挪 2 个位置，才能挪到 fox 的左边。因此如果 slop = 2, 词项的匹配也就可以不按顺序了。

## 多值字段

多值字段使用短语匹配时会发生奇怪的事情。

对以下这个文档进行查询

```json
PUT /my_index/groups/1
{
    "names": [ "John Abraham", "Lincoln Smith"]
}
```

```json
GET /my_index/groups/_search          // 文档依旧会被匹配到，即使是属于两个不同的人名
{
    "query": {
        "match_phrase": {
            "names": "Abraham Lincoln"
        }
    }
}
```

因为在分析 `John Abraham` 的时候，产生如下信息：

- Position 1: `john`
- Position 2: `abraham`

在分析 `Lincoln Smith` 的时候，产生如下信息：

- Position 3: `lincoln`
- Position 4: `smith`

搜索的时候 `abraham` 和 `lincoln` 正好相邻，因此就匹配到了。这种情况可以使用 **`position_increment_gap`** 进行解决。

```json
DELETE /my_index/groups/ 

PUT /my_index/_mapping/groups                      // 创建一个有正确值的新的映射 groups
{
    "properties": {
        "names": {
            "type":                "string",
            "position_increment_gap": 100
        }
    }
}
```

`position_increment_gap` 告诉 es 应该为数组中每个新元素增加当前词条 `position` 的指定值。所以现在索引 `names` 数组时，得到的映射是：

- Position 1: `john`
- Position 2: `abraham`
- Position 103: `lincoln`
- Position 104: `smith`

## 越近越好

```json
POST /my_index/my_type/_search
{
   "query": {
      "match_phrase": {
         "title": {
            "query": "quick dog",
            "slop":  50 
         }
      }
   }
}
```

`match_phrase` 仅仅排除了不包含确切短语的文档，邻近查询(slop > 0) 的查询，会将查询词条的邻近度考虑到最终相关度 `_score` 中。通过设置一个像 50 或 100 的高 slop 值，能给予那些单词临近的文档更高的分数。

```json
POST /my_index/my_type/_search
{
   "query": {
      "match_phrase": {
         "title": {
            "query": "quick dog",
            "slop":  50                  // 注意这个值，非常高
         }
      }
   }
}
```

## 使用邻近度提高相关度

事实上，如果 7 个词条中有 6 个匹配，那么这个文档对于用户而言就已经足够相关，但是 `match_phrase` 会将其排除在外。前文介绍的 `minimum_should_match` 的确可以解决这个问题。如果想将多个查询的 **分数累计** 起来，意味着我们应该用 `bool` 查询将它们进行合并。

```json
GET /my_index/my_type/_search
{
  "query": {
    "bool": {
      "must": {                     // 从结果集中包含或者排除文档
        "match": { 
          "title": {
            "query":                "quick brown fox",
            "minimum_should_match": "30%"
          }
        }
      },
      "should": {                   // 增加了匹配到文档的相关度评分
        "match_phrase": { 
          "title": {
            "query": "quick brown fox",
            "slop":  50
          }
        }
      }
    }
  }
}
```

## 性能优化

短语查询 和 邻近查询 都比 简单的 query 查询 **代价更高**。一个 `match` 查询仅仅是看词条是否存在于 倒排索引 中，而一个 **`match_phrase`** 查询是 **必须计算并比较多个可能重复词项的位置。**一个简单的 `term` 查询 比 一个短语查询大约快 10 倍，比邻近查询(有 slop) 大约快 20 倍。比如在 DNA 序列中，**有很多词项是在很多位置是反复出现的**，这时候使用高 slop 值会导致位置计算量大大增加，查询成本过高。

### 结果集重新评分

一个查询可能会匹配成千上万条结果，但是用户可能只对结果的前几页感兴趣。我们可以对 **顶部文档** 重新排序，来给 **同时匹配** 了短语查询的文档一个额外的相关度升级。`search` API 通过 **重新评分** 明确支持该功能。重新评分阶段支持一个 **代价更高** 的评分算法 -- `phrase` 查询。只是为了从 **每个分片** 中获取 **前 k 个** 结果，根据它们的 **最新评分重新排序**。

```json
GET /my_index/my_type/_search
{
    "query": {
        "match": {                                    // 决定最终哪些文档会被包含在最终结果集中，通过 TF/IDF 排序
            "title": {
                "query": "quick brown fox",
                "minimum_should_match": "30%"
            }
        }
    },
    "rescore": {                                     // 重新评分
        "window_size": 50,                           // 是每一分片进行重新评分的顶部文档数量
        "query": {         
            "rescore_query": {
                "match_phrase": {
                    "title": {
                        "query": "quick brown fox",
                        "slop": 50
                    }
                }
            }
        }
    }
}
```

## 寻找相关词

会出现这样一种情况， *I’m not happy I’m working* 和 *I’m happy I’m not working* 拥有相同的邻近度，但是含义截然不同。有时候想要搜索的是语义相同的文档。

这种时候要对单词的上下文尽可能多地进行保留。**将每个单词以及它的邻近词作为单个词项索引。**

` ["I m", "m not", "not happy", "happy I", "I m", "m working"]`

这些单词对被称为是 `shingles`。当然也可以索引三个单词。

(后面还有一些和相关度查询的就不做摘抄了)。

## 部分匹配

但如果想匹配部分而不是全部的词该怎么办？ *部分匹配* 允许用户指定查找 **词的一部分** 并找出所有包含这部分片段的词。

es 只是简单地将它们的词干作为索引形式，没有必要像 MySQL 一样做部分匹配。部分匹配较为常见的应用在：

+ **匹配邮编、产品序列号、其它 `not_analyzed` 类型的字段**，这些值可以以某个特定前缀开始，也可以是与某种模式匹配的。
+ **输入即搜索(search-as-u-type)** 在用户键入搜索词过程的同时，呈现最可能的结果。
+ 匹配 德语、荷兰语 这样有长组合词的语言。(*Weltgesundheitsorganisation*)

## 邮编与结构化数据

```json
PUT /my_index
{
    "mappings": {
        "address": {
            "properties": {
                "postcode": {
                    "type":  "string",
                    "index": "not_analyzed"
                }
            }
        }
    }
}

PUT /my_index/address/1
{ "postcode": "W1V 3DG" }    // W 代表区域（1或2个字母）1V 代表行政区(1或2个数字，可能跟着一个字母) 3代表街区区块 DG 代表单元

PUT /my_index/address/2
{ "postcode": "W2F 8HW" }

PUT /my_index/address/3
{ "postcode": "W1F 7HW" }

PUT /my_index/address/4
{ "postcode": "WC1N 1LZ" }

PUT /my_index/address/5
{ "postcode": "SW5 0BE" }
```

## prefix 前缀查询

为了找到所有以 W1 开始的右边，使用简单的 **`prefix` 查询**。

**`prefix` 查询** 是一个词级别的底层的查询，**不会**在搜索之前分析查询字符串，它假定传入前缀就正式要查找的前缀。`prefix` **不会** 做相关度评分计算，只是将所有匹配的文档返回，并为每条结果赋值评分为1。

**`prefix` 查询** 和 **`prefix` 过滤器** 两者区别只在于过滤器可以被缓存，查询不行。

```json
GET /my_index/address/_search
{
    "query": {
        "prefix": {
            "postcode": "W1"
        }
    }
}
```

**`prefix` 查询的工作原理：**

倒排索引包含了一个有序的 唯一词 列表，对于每个词，倒排索引都会将包含的文档 ID 列入 倒排表。查询则会：

+ 扫描词列表并查找到第一个以 W1 开始的词
+ 搜集关联的文档 ID
+ 移动到下一个词
+ 如果这个词以 W1 开头，重复执行步骤2，否则执行步骤3

前缀索引越短，所需要访问的词就会越多，如果以 W 作为前缀，则可能就需要数千万次的匹配。它的伸缩性并不是很好，**会给集群带来很多压力**。可以使用较长的前缀进行限制，减少要访问的量。

## 通配符和正则表达式查询

**`wildcard` 通配符查询** 也是一种底层基于词的查询。与前缀查询不同的是它允许指定匹配的正则式，使用标准的 shell 通配符：`?` 匹配任意字符，`*` 匹配 0 或者 多个字符。

```json
GET /my_index/address/_search
{
    "query": {
        "wildcard": {
            "postcode": "W?F*HW"        // 会匹配包含 W1F 7HW 和 W2F 8HW 的文档 
        }
    }
}
```

如果现在只想匹配 W 区域的所有邮编，前缀匹配也会包括以 `WC` 开头的所有邮编。`regexp` 查询允许写出更复杂的模式：

```json
GET /my_index/address/_search
{
    "query": {
        "regexp": {
            "postcode": "W[0-9].+" 
        }
    }
}
```

`wildcard` 和 `regexp` 查询的工作方式与 `prefix` 查询完全一样，它们也需要扫描倒排索引中的词列表才能找到所有匹配的词，然后依次获取每个词相关的文档 ID ，与 `prefix` 查询的 **唯一不同** 是：它们能支持更为复杂的匹配模式。

**避免使用左通配模匹配，如 `*foo`** 这样会消耗非常多的资源。

`prefix`、`wildcard`、`regexp` 三种查询都是针对 `not_analyzed` 字段进行查询，如果是对 `analyzed` 字段进行查询，则会对分词后的每一个词都做检查匹配，效率会更低..查找到的数据也不是正确的。

## 输入即搜索

就是所谓的 即时都锁，让用户能在更短的时间内得到搜索结果，引导用户搜索索引中真实存在的结果。(这个功能可以在很多搜索引擎中看到。

在短语匹配中，还有 `match_phrase_prefix`  短语匹配查询，匹配相对顺序一致的所有指定词语。

```json
{
    "match_phrase_prefix" : {
        "brand" : "johnnie walker bl"
    }
}
```

它与 `match_phrase` 唯一的区别就是把 查询字符串 的 最后一个词 作为前缀使用。实际上搜索的是 `johnnie walker bl*`。

```json
{
    "match_phrase_prefix" : {
        "brand" : {
            "query": "walker johnnie bl", 
            "slop":  10
        }
    }
}
```

前缀查询会有严重的资源消耗的问题，短语查询也是如此，可以通过设置 `max_expansions` 限制前缀扩展的影响：

```json
{
    "match_phrase_prefix" : {
        "brand" : {
            "query": "johnnie walker bl",
            "max_expansions": 50             // 控制可以与前缀匹配的词的数量，也就是说最多匹配出 50 条结果
        }
    }
}
```

## 索引时优化

查询时的灵活性通常以牺牲搜索性能为代价，有时候将这些消耗从查询过程转移到别的地方是有意义的。可以通过在索引时处理数据的灵活性以提升系统性能。虽然增加索引空间与变慢的索引能力，但是索引时的代价只需要付出一次，或许比查询时的代价更小。

## Ngrams 在部分匹配的应用

单个词的查找会比在词列表中盲目挨个查找的效率要高，因此在 **搜索之前** 准备好供部分匹配的数据 可以提高搜索的性能。

在索引时准备数据意味着要选择合适的分析链，这里部分匹配使用的工具是 *n-gram* 。可以将 *n-gram* 看成一个在词语上 *滑动窗口* ， *n* 代表这个 “窗口” 的长度。如果我们要 n-gram `quick` 这个词 —— 它的结果取决于 *n* 的选择长度：

- 长度 1（unigram）： [ `q`, `u`, `i`, `c`, `k` ]
- 长度 2（bigram）： [ `qu`, `ui`, `ic`, `ck` ]
- 长度 3（trigram）： [ `qui`, `uic`, `ick` ]
- 长度 4（four-gram）： [ `quic`, `uick` ]
- 长度 5（five-gram）： [ `quick` ]

但对于输入即搜索（search-as-you-type）这种应用场景，我们会使用一种特殊的 n-gram 称为 *边界 n-grams* （edge n-grams）。所谓的边界 n-gram 是说它会固定词语开始的一边，以单词 `quick` 为例，它的边界 n-gram 的结果为：

- `q`
- `qu`
- `qui`
- `quic`
- `quick`

可能会注意到这与用户在搜索时输入 “quick” 的字母次序是一致的，换句话说，这种方式正好满足即时搜索（instant search）！

## 索引时输入即搜索

[不摘抄了](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_index_time_search_as_you_type.html)

## Ngrams 在复合词的应用

[不摘抄了](https://www.elastic.co/guide/cn/elasticsearch/guide/current/ngrams-compound-words.html)

## 控制相关度

评分机制暂时不看了。这个等到以后应用的时候再仔细看吧。

## 聚合

## 高阶概念

+ 桶（Buckets）
  + 满足特定条件的文档集合
+ 指标（Metrics）
  + 对桶内的文档进行统计计算

## 桶

当聚合开始被执行，每个文档里的值通过计算来决定符合哪个桶的条件。如果匹配到，文档将放入相应的桶并接着进行聚合操作。

桶也可以嵌套早其它桶里，比如，辛辛那提会被放入俄亥俄州这个桶，而 *整个* 俄亥俄州桶会被放入美国这个桶。

## 指标

桶能让我们按照条件划分文档，但是最终我们需要对桶内的文档进行一些指标的计算。

指标指的是简单的数学运算，比如 最小值、平均值、最大值、汇总。

## 尝试聚合

```json
POST /cars/transactions/_bulk
{ "price" : 10000, "color" : "red", "make" : "honda", "sold" : "2014-10-28" }
{ "price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05" }
{ "price" : 30000, "color" : "green", "make" : "ford", "sold" : "2014-05-18" }
{ "price" : 15000, "color" : "blue", "make" : "toyota", "sold" : "2014-07-02" }
{ "price" : 12000, "color" : "green", "make" : "toyota", "sold" : "2014-08-19" }
{ "price" : 20000, "color" : "red", "make" : "honda", "sold" : "2014-11-05" }
{ "price" : 80000, "color" : "red", "make" : "bmw", "sold" : "2014-01-01" }
{ "price" : 25000, "color" : "blue", "make" : "ford", "sold" : "2014-02-12" }
```

汽车经销商可能会想知道哪个颜色的汽车销量最好。 

```json
GET /cars/transactions/_search
{
  "size": 0,
  "aggs": {
    "popular_colors": {
      "terms": {
        "field": "color"
      }
    }
  }
}
```

```json
{
...
   "hits": {                       // 因为设置了 size=0 所以不会有结果返回
      "hits": [] 
   },
   "aggregations": {
      "popular_colors": { 
         "buckets": [
            {
               "key": "red", 
               "doc_count": 4 
            },
            {
               "key": "blue",
               "doc_count": 2
            },
            {
               "key": "green",
               "doc_count": 2
            }
         ]
      }
   }
}
```

**一旦** 文档可以被搜索到，**就** 能被聚合。也就意味我们可以直接将聚合的结果源源不断传入图形库，生成实时的仪表盘。

## 添加度量指标

假如我们想要求每种颜色汽车的平均价格是多少？

```json
GET /cars/transactions/_search
{
  "size": 0,
  "aggs": {
    "colors": {
      "terms": {
        "field": "color"
      }
    },
    "avg_price": {
      "avg": {
        "field": "price"
      }
    }
  }
}
```



```json
{
...
   "aggregations": {
      "colors": {
         "buckets": [
            {
               "key": "red",
               "doc_count": 4,
               "avg_price": { 
                  "value": 32500
               }
            },
            {
               "key": "blue",
               "doc_count": 2,
               "avg_price": {
                  "value": 20000
               }
            },
            {
               "key": "green",
               "doc_count": 2,
               "avg_price": {
                  "value": 21000
               }
            }
         ]
      }
   }
...
}
```

## 嵌套桶

每种颜色的汽车平均价格是多少？各自的汽车制造商是谁？

```json
{
  "size": 0,
  "aggs": {
    "colors": {
      "terms": {"field": "color"}
    },
    "aggs": {
      "avg_price": {
        "avg": {"field": "price"}
      },
      "make": {
        "terms": {"field": "make"}
      }
    }
  }
}
```

```json
{
...
   "aggregations": {
      "colors": {
         "buckets": [
            {
               "key": "red",
               "doc_count": 4,
               "make": { 
                  "buckets": [
                     {
                        "key": "honda", 
                        "doc_count": 3
                     },
                     {
                        "key": "bmw",
                        "doc_count": 1
                     }
                  ]
               },
               "avg_price": {
                  "value": 32500 
               }
            },

...
}
```

## 最后的修改

假如我们想要知道每种颜色的汽车的平均价格，且其中每种汽车制造商的最高价格和最低价格是多少？

```json
{
  "size": 0,
  "aggs": {
    "colors": {
      "terms": {"field": "color"},
      "aggs": {
        "avg_price": {"avg": {"field": "price"}},
        "aggs": {
          "make": {
            "terms": {"field": "make"},
            "aggs": {
              "min_price": {"min": {"field": "price"}},
              "max_price": {"max": {"field": "price"}}
          	}
          }
        }
      }
    }
  }
}
```

```json
{
...
   "aggregations": {
      "colors": {
         "buckets": [
            {
               "key": "red",
               "doc_count": 4,
               "make": {
                  "buckets": [
                     {
                        "key": "honda",
                        "doc_count": 3,
                        "min_price": {
                           "value": 10000 
                        },
                        "max_price": {
                           "value": 20000 
                        }
                     },
                     {
                        "key": "bmw",
                        "doc_count": 1,
                        "min_price": {
                           "value": 80000
                        },
                        "max_price": {
                           "value": 80000
                        }
                     }
                  ]
               },
               "avg_price": {
                  "value": 32500
               }
            },
...
```

## 条形图

聚合还有一个令人激动的特性就是十分容易地将它们转换成图表和图形。

我们希望知道每个售价区间内汽车的销量，还会想知道每个售价区间内汽车带来的收入，可以通过对每个区间内已售汽车的售价求和得到。

[具体使用看这里吧 不记录了](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_building_bar_charts.html)

## 按时间统计

构建按时间统计的 date_histogram 使用频率仅次于使用 es 进行搜索。**默认** 只返回文档数目非 0 的 buckets。

Date_histogram 倾向于转换成线状图以展示时间序列。假如想知道每月销售多少台汽车？

```json
GET /cars/transactions/_search
{
  "size": 0,
  "aggs": {
    "sales": {
      "data_histogram": {
        "field": "sold",
        "interval": "month",
        "format": "yyyy-MM-dd"
      }
    }
  }
}
```

```json
{
   ...
   "aggregations": {
      "sales": {
         "buckets": [
            {
               "key_as_string": "2014-01-01",
               "key": 1388534400000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-02-01",
               "key": 1391212800000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-05-01",
               "key": 1398902400000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-07-01",
               "key": 1404172800000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-08-01",
               "key": 1406851200000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-10-01",
               "key": 1412121600000,
               "doc_count": 1
            },
            {
               "key_as_string": "2014-11-01",
               "key": 1414800000000,
               "doc_count": 2
            }
         ]
...
}
```

## 返回空的 buckets

```json
GET /cars/transactions/_search
{
  "size": 0,
  "aggs": {
    "sales": {
      "data_histogram": {
        "field": "sold",
        "interval": "month",
        "format": "yyyy-MM-dd",
        "min_doc_count": 0,           // 这个参数会返回空的 buckets
        "extended_bounds": {          // es 只会默认返回最大值和最小值之间的 buckets, 加上这个参数就可以返回边界值了
          "min": "2014-01-01",
          "max": "2014-12-31"
        }
      }
    }
  }
}
```

## 扩展例子

[暂时不写了](https://www.elastic.co/guide/cn/elasticsearch/guide/current/_extended_example.html)

## 潜力无穷

kibana

## 范围限定的聚合

福特在售车有多少种颜色？

```json
GET /cars/transactions/_search
{
  "query": {
    "match": {"make": "ford"}
  },
  "aggs": {
    "colors": {
      "terms": {"field": "color"}
    }
  }
}
```

```json
{
...
   "hits": {
      "total": 2,
      "max_score": 1.6931472,
      "hits": [
         {
            "_source": {
               "price": 25000,
               "color": "blue",
               "make": "ford",
               "sold": "2014-02-12"
            }
         },
         {
            "_source": {
               "price": 30000,
               "color": "green",
               "make": "ford",
               "sold": "2014-05-18"
            }
         }
      ]
   },
   "aggregations": {
      "colors": {
         "buckets": [
            {
               "key": "blue",
               "doc_count": 1
            },
            {
               "key": "green",
               "doc_count": 1
            }
         ]
      }
   }
}
```

### 全局桶

福特汽车与所有汽车平均售价的比较。

```json
GET /cars/transactions/_search
{
  "size": 0,
  "query": {"match": {"make": "ford"}},
  "aggs": {
    "single_avg_price": {
      "avg": {"field": "price"}
    },
    "all": {
      "global": {},                       // 全局桶没有参数
      "aggs": {
        "avg_price": {
          "avg": {"field": "price"}       // 聚合操作针对所有文档，忽略汽车品牌，有点牛逼的样子，es 的功能也太丰富了吧
        }
      }
    }
  }
}
```

`single_avg_price` 度量计算是基于查询范围内所有文档，即所有的福特汽车。

`avg_price` 嵌套在全局桶下，意味着它完全忽略了范围，并对所有文档进行计算，聚合返回的平均值是所有汽车的平均售价。

## 过滤和聚合

如果想找到售价在 $10000 美元之上的所有汽车的同时，为这些车计算平均售价。聚合结果收到筛选条件的影响。

```json
GET /cars/transactions/_search
{
  "size": 0,
  "query": {
    "constant_score": {
      "filter": {"range": {"price": {"gte": 10000}}}
    }
  },
  "aggs": {
    "single_avg_price": {"avg": {"field": "price"}}
  }
}
```

## 过滤桶

假设现在有一个用户搜索框，用户搜索福特汽车的同时，我们也在页面上显示出上个月福特汽车出售的数量，同时显示所有福特汽车的平均售价。

```json
GET /cars/transactions/_search
{
  "size": 0,
  "query": {"match": {"make": "ford"}},
  "aggs": {
    "recent_sales": {
      "filter": {"range": {"sold": {"from": "now-1M"}}}
    },
    "aggs": {
      "average_price": {"avg": {"field": "price"}}
    }
  }
}
```

```json
{
  "took": 36,
  "timed_out": false,
  "_shards": {
    "total": 4,
    "successful": 4,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": 103675,
    "max_score": 1,
    "hits": [
      {....}                 // 这个结果显示的是所有的 福特 汽车信息
    ]
  },
  "aggregations": {
    "skl_trade": {
      "doc_count": 6880     // 这个结果显示的是 filter 桶里的信息
    },
    "avg_price": {
      "value": 3.2459393124612808      // 聚合结果不受到 filter 桶的影响，计算的是 福特 汽车的平均价格，不管是不是近一个月内的
    }
  }
}
```

## 后过滤器

假如我们想要在页面上显示 绿色的福特汽车的信息，还想显示统计 每种颜色的福特车的数量。就可以使用下列的语句。反正就是一个语句，干了 sql 语句的两个事情。

```json
GET /cars/transactions/_search
{
    "size" : 0,
    "query": {
        "match": {
            "make": "ford"
        }
    },
    "post_filter": {                              // resp['hits']['hits'] 里面的内容是绿色福特车的信息
        "term" : {
            "color" : "green"
        }
    },
    "aggs" : {
        "all_colors": {
            "terms" : { "field" : "color" }      // aggregations 里面的信息是 每种颜色的福特车的数量信息
        }
    }
}
```

### 性能考虑：

当你需要对搜索结果和聚合结果做不同的过滤时，才应该用 `post_filter`, 它的特性是在查询之后执行，任何过滤对性能带来的好处都会完全丢失(比如缓存)。所以**不要把它当作普通的过滤条件使用**，`post_filter` 只与聚合一起使用。

## 小结

query 中的 `filter` 过滤 会影响搜索结果和聚合结果

`filter` 桶不会影响 query 的结果，也不会影响聚合的结果，但会增加一个字段显示 `filter` 桶 的查询结果

`post_filter` 会影响 query 结果，但是不会影响聚合结果

## 多桶排序

多值桶(`terms`、`histogram`、`data_histogram`) 会动态生成很多桶，那么 es 是如何决定这些桶展示给用户的顺序呢？

**默认** 会根据 `doc_count` 降序排列。

## 内置排序

现在想要按照 `terms` 聚合，按照 `doc_count` 值升序排序

```json
GET /cars/transactions/_search
{
  "size": 0,
  "aggs": {
    "colors": {
      "terms": {
        "field": "color",
        "order": {"_count": "asc"}
      }
    }
  }
}
```

`order` 中可以写：

+ `_count` 按文档数排序，对 `terms`、`histogram`、`date_histogram` 有效
+ `_term` 按词项的字符串值的字母顺序排序，只在 `terms` 内使用
+ `_key` 按每个桶的键值数值排序，理论上与 `_term` 类似，只在 `histogram` 和 `date_histogram` 内使用

## 按度量排序

如果想按照汽车颜色创建一个销售条状图表，但按照汽车平均售价的升序进行排序。增加一个度量，再指定 `order` 参数引用这个度量即可：

```json
GET /cars/transactions/_search
{
    "size" : 0,
    "aggs" : {
        "colors" : {
            "terms" : {
              "field" : "color",
              "order": {
                "avg_price" : "asc"                // 按照平均价格进行排序
              }
            },
            "aggs": {
                "avg_price": {
                    "avg": {"field": "price"}      // 计算每个桶的平均价格
                }
            }
        }
    }
}
```

如果想使用 **多值度量** 进行排序呢？只需以 **关心的度量** 为 **关键词** 使用 **点式** 路径。

```json
GET /cars/transactions/_search
{
    "size" : 0,
    "aggs" : {
        "colors" : {
            "terms" : {
              "field" : "color",
              "order": {
                "stats.variance" : "asc" 
              }
            },
            "aggs": {
                "stats": {                                     
                    "extended_stats": {"field": "price"}
                }
            }
 9       }
    }
}
```

## 基于 "深度" 度量排序

当想要对更深的度量进行排序，比如 孙子桶 或者 从孙同。可以定义更深的路径，使用 (>) 括起来即可。

但是这样的前提是 **嵌套路径上的每个桶必须是 单值的**

目前有三个单值桶：`filter`、`global`、`reverse_nested`。创建一个汽车售价的直方图，按照红色和绿色车各自的方差进行排序。

```json
GET /cars/transactions/_search
{
    "size" : 0,
    "aggs" : {
        "colors" : {
            "histogram" : {
              "field" : "price",
              "interval": 20000,
              "order": {
                "red_green_cars>stats.variance" : "asc"
              }
            },
            "aggs": {
                "red_green_cars": {
                    "filter": { "terms": {"color": ["red", "green"]}},
                    "aggs": {
                        "stats": {"extended_stats": {"field" : "price"}}   
                    }
                }
            }
        }
    }
}

```

## 近似聚合

单词请求获得精确结果的，这类型的算法通常被认为是 "高度并行" 的，无需任何额外的代价，可以在多台机器上并行执行。

### max 度量

1. 把请求广播到所有的分片上
2. 查看每个文档的 `price` 字段，如果 `price > current_max`，将 `current_max` 替换成 `price`
3. 返回所有分片最大的 `price` 并传回给协调节点
4. 找到从所有分片返回的最大 `price`, 这就是最终的最大值

这个算法可以随着机器数的线性增长而横向扩展，机器之间不需要讨论中间结果，内存消耗很小。

**那么更加复杂的操作则需要在算法的性能和内存使用上做出权衡，对于这个问题，有一个三角因子模型：大数据、精确性、实时性。** 选择的时候满足其中两项。

Elasticsearch 目前支持 **两种近似算法**（ `cardinality` 和 `percentiles` ）。 它们会提供准确但不是 100% 精确的结果。 以牺牲一点小小的估算错误为代价，这些算法可以为我们换来高速的执行效率和极小的内存消耗。

## 统计去重后的数量

[优化指标计算的速度](https://www.elastic.co/guide/cn/elasticsearch/guide/current/cardinality.html)

## 百分位的计算

[另一种优化指标计算的速度](https://www.elastic.co/guide/cn/elasticsearch/guide/current/percentiles.html)

## 通过聚合发现异常指标

[暂时不想记录了](https://www.elastic.co/guide/cn/elasticsearch/guide/current/significant-terms.html)

## Doc Values and Fielddata

 聚合使用一个叫做 **doc values** 的数据结构。doc values 的存在是因为倒排索引只对某些操作是高效的。

倒排索引的 **优势** 在于查找包含某个项的文档，对于另外一个方向的相反操作并 **不高效**。

```
Term      Doc_1   Doc_2   Doc_3
------------------------------------
brown   |   X   |   X   |
dog     |   X   |       |   X
dogs    |       |   X   |   X
fox     |   X   |       |   X
foxes   |       |   X   |
in      |       |   X   |
jumped  |   X   |       |   X
lazy    |   X   |   X   |
leap    |       |   X   |
over    |   X   |   X   |   X
quick   |   X   |   X   |   X
summer  |       |   X   |
the     |   X   |       |   X
------------------------------------
```

如果我们想要获得所有包含 `brown` 的文档的词的完整列表。

```json
GET /my_index/_search
{
  "query" : {              // 查询部分简单又高效
    "match" : {            // 首先在词项列表中找到 brown, 然后扫描所有列，找到包含 brown 的所有文档
      "body" : "brown"     // 可以找到 doc_1 和 doc_2 这两个满足条件
    }
  },
  "aggs" : {               // 聚合部分要找到 doc_1 和 doc_2 里所有唯一的项
    "popular_terms": {     // 迭代索引力的每个 词项，收集 doc_1 和 doc_2 列中的 token
      "terms" : {          // 这很慢，且很难扩展，随着词项和文档的数量增加，执行时间也会增加
        "field" : "body"
      }
    }
  }
}
```

Doc values 通过转置两者间的关系来解决这个问题。

```
Doc      Terms
-----------------------------------------------------------------
Doc_1 | brown, dog, fox, jumped, lazy, over, quick, the
Doc_2 | brown, dogs, foxes, in, lazy, leap, over, quick, summer
Doc_3 | dog, dogs, fox, jumped, over, quick, the
-----------------------------------------------------------------
```

数据转置以后, 收集 doc_1 和 doc_2 的 唯一 token 就会很容易，获得每个文档行，获取所有的词项，求两个集合的 **并集** 即可。(话说为什么不是求的交集呢？？？？？？)

**搜索 和 聚合 是相互紧密缠绕的，搜索使用倒排索引查找文档，聚合操作收集和聚合 doc values 里的数据。**

**另外 排序、访问字段值的脚本、父子关系处理 都用到了 doc values。**

## 深入理解 Doc Value

`doc values` 是 **在索引时** 与 倒排索引 **同时** 生成。也就是说 `doc values` 和 倒排索引 一样，基于 `segment` 生成，并且是 **不可变的**。`doc values` 和 倒排索引 一样 **序列化** 到磁盘，这样对性能和扩展性有很大帮助。

+ 当 `working set` **远小于** 系统的 **可用内存**

  系统会自动将 `doc values` 驻留在内存中，使得读写十分 **快速**。

+ 当 `working set` **远大于** 系统的 **可用内存**
  
  系统会根据需要从磁盘读取 `doc values`, 然后 **选择性** 地放到分页缓存中。很显然，这样 **性能** 会比在内存中 **差很多**，但是它的大小就不再局限于服务器的内存了。如果是使用的 `JVM` 的 `Heap` 来实现，那么只能是因为 `OutOfMemory` 导致程序崩溃了。

### 列式存储的压缩

`doc values` 本质上是一个序列化的 **列式存储**。列式存储 **适用于** 聚合、排序、脚本 等操作。

这种存储方式 **便于压缩（减少磁盘空间、提高访问速度）**，所以减少直接存磁盘读取数据的大小可以提高性能，尽管需要额外消耗 CPU 运算进行解压。

### 如何压缩数据

```
Doc      Terms
-----------------------------------------------------------------
Doc_1 | 100
Doc_2 | 1000
Doc_3 | 1500
Doc_4 | 1200
Doc_5 | 300
Doc_6 | 1900
Doc_7 | 4200
-----------------------------------------------------------------
```

按列布局，意味着我们有一个 **连续的数据块**：`[100,1000,1500,1200,300,1900,4200]`。因为我们已经知道他们 **都是数字**，所以可以使用 **统一的偏移** 来将他们紧密排列。

**针对数字压缩有很多压缩技巧**，会注意到这里的数字都是 100 的倍数，`doc values` 会检测一个段里面的所有数值，并使用一个最大公约数，方便做进一步的数据压缩。如果我们保存 100 作为此段的除数，我们可以对每个数字都除以 100，这样数字都会变少，就可以用更少的位存储，也减少了磁盘存放的大小。

**doc value** 在 **压缩**过程中会使用如下技巧（针对 **数值类型**）：

1. 如果所有的数值各不相同，或有缺失，设置一个标记并记录这些值
2. 如果这些值 **小于** 256，将使用一个简单的 **编码表**
3. 如果这些值 **大于** 256，检测是否存在一个 **最大公约数**
4. 如果 **不存在** 最大公约数，从最小的数值开始，统一计算 **偏移量** 进行编码

那么针对 **string 类型**呢？

​	es 会借助 **顺序表**，会讲字段值进行 **去重** 之后存放如顺序表，通过分配一个 ID，然后通过 ID 来构建 Doc values。这样可以和数值类型达到同样的的压缩效果。当然还有其它的方法：**固定长度**、**变长**、**前缀字符编码** 等等。

### 禁用 Doc Values

`Doc Values` **默认** 会对 所有的数字、地理坐标、日期、IP、`not_analyzed` 字符类型 会 **开启**。

`analyzed` 字符类型 暂时还不能使用 `Doc Values`。因为文本经过分析流程会生成很多的 Token，使得 `Doc Values` 无法高效进行。因此如果你确定某些字段永远都不会进行聚合的话，可以 **禁用** 该字段的 `Doc Values`。这样不仅 **节省磁盘空间**，也许会 **提升索引的速度**。

禁用方式为：

```json
PUT my_index
{
  "mappings": {
    "my_type": {
      "properties": {
        "session_id": {
          "type":       "string",
          "index":      "not_analyzed",
          "doc_values": false      // 禁用该字段的 Doc Values, 这样它就不能被正常聚合、排序
        }                          // 以及脚本操作了
      }
    }
  }
}
```

也可以禁用特定字段的倒排索引，方式如下：

```json
PUT my_index
{
  "mappings": {
    "my_type": {
      "properties": {
        "customer_token": {
          "type":       "string",
          "index":      "not_analyzed",
          "doc_values": true,            // 被启用来允许聚合
          "index": "no"                  // 索引被禁用，该字段无法被搜索了
        }
      }
    }
  }
}
```

## 聚合与分析

`analyzed` 是如何影响聚合呢？

+ 分析会影响聚合中使用的 tokens
+ Doc values 不能适用于 `analyzed` 字符串

初始数据如下：

```json
POST /agg_analysis/data/_bulk
{ "state" : "New York" }
{ "state" : "New Jersey" }
{ "state" : "New Mexico" }
{ "state" : "New York" }
{ "state" : "New York" }
```

现在我们聚合：

```json
GET /agg_analysis/data/_search
{
    "size" : 0,
    "aggs" : {
        "states" : {
            "terms" : {
                "field" : "state"
            }
        }
    }
}
```

得到结果：

```json
{
...
   "aggregations": {
      "states": {
         "buckets": [
            {
               "key": "new",
               "doc_count": 5
            },
            {
               "key": "york",
               "doc_count": 3
            },
            {
               "key": "jersey",
               "doc_count": 1
            },
            {
               "key": "mexico",
               "doc_count": 1
            }
         ]
      }
   }
}
```

显然这不是我们想要的结果，只需要把 字段类型 设置为 `not_analyzed`。这样可以防止 `New York` 被分析。

```json
DELETE /agg_analysis/
PUT /agg_analysis
{
  "mappings": {
    "data": {
      "properties": {
        "state" : {
          "type": "string",
          "fields": {           // raw multified
            "raw" : {
              "type": "string",
              "index": "not_analyzed"
            }
          }
        }
      }
    }
  }
}

GET /agg_analysis/data/_search
{
  "size" : 0,
  "aggs" : {
    "states" : {
        "terms" : {
            "field" : "state.raw"         // 这样聚合出的结果才是正确的
        }
    }
  }
}
```

### 分析字符串 和 Fielddata

为什么 Doc Values 不支持 分析字符串，但是为什么仍然可以对这些字段使用聚合呢？

答案：

因为 `fielddata`，它的构建和管理 100% 在内存中，常驻于 JVM 内存对，这意味着它的 **本质** 是 **不可扩展** 的。从历史上看，`fielddata` 是所有字段的默认值，但是 es 已迁移到 doc values 以减少 OOM 的机率。分析的字符串是仍然使用 `fielddata` 的最后一块阵地。最终目的是建立一个序列化的数据结构，可以高维度的分析字符串，逐步淘汰 fielddata。

虽然没有看懂 fielddata 到底是干啥的... 假装看懂了吧。也许 7.x 这里会完全不一样。

### 高基数内存的影响

**避免分析字段的另一个原因就是：**

高基数字段在加载到 `fielddata` 时会消耗大量内存，分析过程会生成大量的 `token`，这些 `token` 大多数是唯一的，这会增加字段的整体技术并且带来更大的内存压力。

`n-gram` 的分析过程（New York）：

`ne`、`ew`、`w`、`y`、`yo`、`or`、`rk`

由此可见会生成 **大量的唯一 token**，这些数据加载到内存中，会轻而易举地将我们 **堆空间消耗殆尽**。

最后，在聚合字符串之前，务必确认该字符串类型是 `not_analyzed` 还是 `analyzed`，如果是 `not_analyzed` 则会通过 `doc values` 来节省内存。如果是 `analyzed`，则它将使用 `fielddata` 并加载到内存中。它会否因为 `ngrams` 拥有一个非常大的基数？如果是，这对于内存来说是极度不友好的。

## 限制内存使用

`fielddata` 是 **延迟加载** 的。如果从来 **没有聚合** 一个 `analyzed` 字符串，就 **不会加载**  `fielddata` 到内存中。另外 `fielddata` 是 **基于字段加载** 的，所以只有 **很活跃** 地使用字段才会增加 `fielddata` 的负担。一旦，`analyzed` 字符串被加载到 `fielddata`，它们就一直会在那里，直到节点崩溃。所以，要留意 **内存的使用情况**。

**！！！** 

但是，假如你的查询是 高度选择性 和 只返回命中的 100 个结果，需要注意：

1. `fielddata` 会加载索引中（针对该特定字段的）**所有的** 文档。
2. `fielddata` 不是在索引创建时构建的，而是在查询运行时 **动态填充** 的。因此将所有的信息一次加载，再将其维持在内存中的方式，比反复只加载一个 `fielddata` 的部分代价要低。
3. 堆栈乱用会导致节点不稳定，感谢缓慢的垃圾回收机制，甚至会导致节点宕机。JVM 堆是有限资源，应该被合理利用。**限制 fielddata 对堆使用的影响有多套机制，而这些机制非常重要。**

#### 选择堆大小

在设置 es 堆大小时需要通过设置 `$ES_HEAP_SIZE` 环境变量。遵循以下两个规则：

**不要超过可用 RAM 的 50%**

因为 Lucene 能很好利用文件系统的缓存，它是通过系统内核管理的，如果没有足够的文件系统缓存空间，性能会受到影响。此外，专用于堆的内存越多意味着其他所有使用 doc values 的字段内存越少。

**不要超过 32GB**

如果堆大小小于 32 GB，JVM 可以利用指针压缩，这可以大大降低内存的使用：每个指针 4 字节而不是 8 字节。

### Fielddata 的大小

`indices.fielddata.cache.size` 控制为 fielddata 分配的堆空间大小。 当你发起一个查询，分析字符串的聚合将会被加载到 fielddata，如果这些字符串之前没有被加载过。如果结果中 fielddata 大小超过了指定 `大小` ，其他的值将会被回收从而获得空间。

### 监控 fielddata

无论是仔细监控 fielddata 的内存使用情况， 还是看有无数据被回收都十分重要。高的回收数可以预示严重的资源问题以及性能不佳的原因。

Fielddata 的使用可以被监控：

- 按索引使用 [`indices-stats` API](http://www.elastic.co/guide/en/elasticsearch/reference/current/indices-stats.html) ：

  ```json
  GET /_stats/fielddata?fields=*
  ```

- 按节点使用 [`nodes-stats` API](https://www.elastic.co/guide/en/elasticsearch/reference/5.6/cluster-nodes-stats.html) ：

  ```json
  GET /_nodes/stats/indices/fielddata?fields=*
  ```

- 按索引节点：

```json
GET /_nodes/stats/indices/fielddata?level=indices&fields=*
```

使用设置 `?fields=*` ，可以将内存使用分配到每个字段。

### 断路器

Elasticsearch 包括一个 *fielddata 断熔器* ，这个设计就是为了处理上述情况。 断熔器通过内部检查（字段的类型、基数、大小等等）来估算一个查询需要的内存。它然后检查要求加载的 fielddata 是否会导致 fielddata 的总量超过堆的配置比例。

如果估算查询的大小超出限制，就会 *触发* 断路器，查询会被中止并返回异常。这都发生在数据加载 *之前* ，也就意味着不会引起 OutOfMemoryException 。

## Fielddata 的过滤

背景：

用户可以为歌曲设置任何他们喜欢的标签，比如 rock、hiphop、electronica，但是有的歌曲也会附上 my_16th_birthday_favourite_anthem 这样的标签，假如我们想为用户展示每首歌曲最受欢迎的三个标签，怎么实现呢？

```json
PUT /music/_mapping/song
// 有了这个映射，只有那些至少在 本段 文档中出现超过 1% 的项才会被加载到内存中
// 这样可以把 my_16th_birthday_favourite_anthem 这种标签过滤掉
{
  "properties": {
    "tag": {
      "type": "string",
      "fielddata": {                    // 在这里面配置 fielddata 处理该字段的方式
        "filter": {
          "frequency": {                // 允许我们基于项频率过滤加载 fielddata
            "min":              0.01,   // 只加载那些至少在本段文档中出现 1% 的项
            "min_segment_size": 500     // 忽略任何文档个数小于 100 的段，如果段内只有少量文档
          }                             // 它的词频会非常粗略切没有任何意义，且小的分段会很快被
        }                               // 合并到大的分段中
      }
    }
  }
}
```

**fielddata 是按段来加载** 的，所以可见的词频只是该段内的频率。但是这个限制也有 **好处**，可以让受欢迎的新项迅速提升到顶部。

为什么这么说呢？

试想，有一个新风格的歌曲在一夜间收到大众欢迎，如果想要将这种新风格的歌曲标签包括在最受欢迎列表中呢？依赖对索引做完整的词频计算，就必须等到新标签变得像 rock 和 electronica 一样流行。但是基于段来加载的 fielddata，新加的标签会很快作为高频标签出现在新段内，当然也会迅速上升到顶部。

**缺点**，Fielddata 过滤对内存使用有 **巨大的** 影响，因为有些数据根本就没有被使用到，舍弃掉也没问题，**内存的节省** 通常要比包括一个大量而无用的长尾项更为重要。

## 预加载 fielddata

[预加载原理、全局序号、索引预热器](https://www.elastic.co/guide/cn/elasticsearch/guide/2.x/preload-fielddata.html)

## 优化聚合查询

`terms` 桶基于我们的数据动态构建桶，大多数时候，对于单个字段的聚合查询还是非常快的，但是 **同时聚合多个字段时**，就可能产生大量的分组，最终结果就是占用大量 es 内存，导致 OOM 的情况发生。

假设我们现在有一些关于电影的数据集，每条数据里面会有一个数组类型的字段，存储该电影的所有演员的名字。

文档数据长这样：

```json
{
  "actors" : ["Fred Jones", "Mary Jane", "Elizabeth Worthing"]
}
```

这时我们想查询出演影片最多的十个演员以及与他们合作最多的演员

```json
{
  "aggs": {
    "actors": {
      "terms": {
        "field": "actors",       // 返回出演最多的十分演员
        "size": 10
      },
      "aggs": {
        "costars": {
          "terms": {
            "field": "actors",   // 返回与这十位演员合作最多的五位演员（？？？？）
            "size": 5
          }
        }
      }
    }
  }
}
```

这条语句，第一层 actors，构建树的第一层，每个演员都会有一个桶。第二层 costars，构建第二层，每个联合出演都会有一个桶。意味着每部影片会生成 n^2 个桶。因此，即使最后返回数据只有 50 条，但是会创建一个有 2，000，000 桶的树，还要排序，取前10。随着文档数目的增加，内存压力也会越来越大。

### 深度优先 和 广度优先

es 允许我们**改变**聚合的 **集合模式**。之前展示的策略就是 **深度优先**，先构建完整的树，修建无用的节点，这对于大多数的聚合都能正常工作，但对于上面举的例子则不再使用。

**广度优先** 会先执行第一层聚合，再继续下一层聚合之前先做修建。结合之前的例子，就是说构建第一层树的时候，已经知道我们只需要前十位演员。因此也就没必要保留其它的演员信息。然后根据前十个桶，再构建第二层树。广度优先可以 **大幅度节省内存**。

只需要使用：

```json
{
  "aggs" : {
    "actors" : {
      "terms" : {
         "field" :        "actors",
         "size" :         10,
         "collect_mode" : "breadth_first" 
      },
      "aggs" : {
        "costars" : {
          "terms" : {
            "field" : "actors",
            "size" :  5
          }
        }
      }
    }
  }
}
```

广度优先 **仅仅适用于** 每个组聚合数量远远小于当前总组数的情况。

广度优先的 **内存使用情况** 与 **裁剪后的缓存分组数据量** 是呈线性的。对于很多聚合来说，每个桶内的文档数量是相当大的，假如有一个 按月分组 的直方图，**总组数是固定的**，每个月下的数据量相当大的话，广度优先并不是一个好的选择。这时候在第一层进行修剪没有什么意义，且数据量大内存使用也大，因此才选择用 深度优先 作为 **默认策略**。

## 总结

内存的管理形式可以有多种形式，取决于我们特定的应用场景：

- 在规划时，组织好数据，使聚合运行在 `not_analyzed` 字符串而不是 `analyzed` 字符串，这样可以有效的利用 doc values 。
- 在测试时，验证分析链不会在之后的聚合计算中创建高基数字段。
- 在搜索时，合理利用近似聚合和数据过滤。
- 在节点层，设置硬内存大小以及动态的断熔限制。
- 在应用层，通过监控集群内存的使用情况和 Full GC 的发生频率，来调整是否需要给集群资源添加更多的机器节点

## 数据建模（关联关系处理）

关系型数据库中，实体关联查询时间消费是很昂贵的，关联的越多，消费就越昂贵，特别是跨服务器，关联成本极其昂贵，基本不可用。单个服务器上又存在数据量的限制。

es 与大多数的 NoSQL 数据库类似，是扁平化的，索引是独立文档的集合体。单个文档中的 **数据变更** 是 **ACIDic** 的，但是涉及到多个文档的事务则不是。当一个事务部分失败时，无法回滚索引数据到前一个状态的。

**扁平化有以下优势：**

+ 索引过程是快速和无锁的
+ 搜索过程是快速和无锁的
+ 每个文档都是相互独立的，因此大规模的数据可以在多个节点上分布

## 应用层联接

意思就是我们无法通过语法对不同的索引进行 join， 但是可以在应用程序中实现联接，来模拟关系型数据库中的 join。

找到用户名字为 John 的用户 ID

```json
GET /my_index/user/_search
{
  "query": {
    "match": {
      "name": "John"
    }
  }
}
```

比如通过用户的 ID = 1 可以很容易找到博客帖子。

```json
GET /my_index/blogpost/_search
{
  "query": {
    "filtered": {
      "filter": {
        "term": { "user": 1 }
      }
    }
  }
}
```

应用层联接的 **主要优点**：可以对数据进行标准化的处理；**缺点** 是：为了在搜索时联接文档，必须运行额外的查询。但是这种方式只适用于第一次查询只有少量的文档匹配的情况，并且最好它们 **很少改变**。这样会允许应用程序对它们进行缓存，避免经常运行第一次查询。

## 非规范的你的数据

如果希望能够通过某个用户姓名找到它的博客文章，可以在博客文档中包含着歌用户的姓名。比如：

```json
PUT /my_index/blogpost/2
{
  "title":    "Relationships",
  "body":     "It's complicated...",
  "user":     {
    "id":       1,
    "name":     "John Smith" 
  }
}
```

这样就能减少在应用层的关联，**数据非规范化** 的 **优点** 就是速度快。因为每个文档都包含了所需的信息，这样并不需要花费昂贵的代价在联接操作上了。

## 字段折叠

如果需要通过特定字段进行 **分组** 的话，例如，我们需要按照 用户名称 分组，然后返回最相关的博客文章。

```json
PUT /my_index/_mapping/blogpost
{
  "properties": {
    "user": {
      "properties": {
        "name": {                // 用 user.name 字段进行全文检索
          "type": "string",
          "fields": {
            "raw": {             // user.name.raw 字段可以通过 terms 聚合进行分组
              "type":  "string",
              "index": "not_analyzed"
            }
          }
        }
      }
    }
  }
}
```

有如下这样的数据

```json
PUT /my_index/user/1
{
  "name": "John Smith",
  "email": "john@smith.com",
  "dob": "1970/10/24"
}

PUT /my_index/blogpost/2
{
  "title": "Relationships",
  "body": "It's complicated...",
  "user": {
    "id": 1,
    "name": "John Smith"
  }
}

PUT /my_index/user/3
{
  "name": "Alice John",
  "email": "alice@john.com",
  "dob": "1979/01/04"
}

PUT /my_index/blogpost/4
{
  "title": "Relationships are cool",
  "body": "It's not complicated at all...",
  "user": {
    "id": 3,
    "name": "Alice John"
  }
}
```

现在查询标题包含了 relationships 并且作者名称包含了 John 的博客，查询结果再按照作者名进行分组。

```json
GET /my_index/blogpost/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        {"match": {"title": "relationships"}},
        {"match": {"user.name": "John"}}
      ]
    }
  },
  "aggs": {
    "users": {
      "terms": {
        "field": "user.name.raw",
        "order": {"top_score": "desc"}
      },
      "aggs": {
        "top_score": {"max": {"script": "_score"}},
        "blogposts": {"top_hits": {"_score": "title", "size": 5}}  // top_hits 是一个关键词
      }
    }
  }
}
```

**top_score**: 通过 users 聚合得到的每一个桶按照文档评分对词项进行排序

**top_hits**: 仅仅为每个用户返回评分最高最相关的 5 个博客文档的 title 字段。

```json
...
"hits": {
  "total":     2,
  "max_score": 0,
  "hits":      []     // 因为 size=0 所以这里是空的
},
"aggregations": {
  "users": {
     "buckets": [
        {
           "key":       "John Smith",        // 每个用户都会有一个桶
           "doc_count": 1,
           "blogposts": {
              "hits": {                      // 在 blogposts.hits 数组包含针对着歌用户的顶层查询
                 "total":     1,             // 结果
                 "max_score": 0.35258877,
                 "hits": [
                    {
                       "_index": "my_index",
                       "_type":  "blogpost",
                       "_id":    "2",
                       "_score": 0.35258877,
                       "_source": {
                          "title": "Relationships"
                       }
                    }
                 ]
              }
           },
           "top_score": {                         // 用户桶按照每个用户最相关的博客文章进行排序
              "value": 0.3525887727737427
           }
        },
...
```

使用 **top_hits** 聚合 **等效** 执行一个查询，返回这些用户的名字，和他们最相关的文档，然后为每一个用户执行相同的查询，以获得最好的博客。不过使用 **top_hits** 的效率会好很多。

## 非规范化和并发

非规范化数据的 **缺点**：

1. 索引会 **更大**，因为每个博客文档的 `_source` 也会 **更大**，并且这里有很多的索引字段。不过数据被存入磁盘会被高度压缩，且磁盘已经很廉价了，es 可以很愉快地应付这些额外的数据。

2. 如果用户改变了名字，那么所有博客文档里面的用户名也都要修改了。

如果我们希望能够搜索到一个特定目录下的文件，等效于：

`grep "some text" /clinton/projects/elasticsearch/*`

文档结构长这样：

```json
PUT /fs/file/1
{
  "name":     "README.txt", 
  "path":     "/clinton/projects/elasticsearch", 
  "contents": "Starting a new Elasticsearch project is easy..."
}
```

当然我们也希望能够搜索到一个特定目录下的目录树包含的任何文件，相当于：

`grep -r "some text" /clinton`

因此，需要对路径层次结构进行索引：

```json
/clinton
/clinton/projects
/clinton/projects/elasticsearch
```

这种层次结构能够通过 `path` 字段使用 `path_hierarchy tokenizer` 自动生成

```json
PUT /fs
{
  "settings": {
    "analysis": {
      "analyzer": {
        "paths": { 
          "tokenizer": "path_hierarchy"
        }
      }
    }
  }
}
```

file 类型的映射看上去如下所示

```json
PUT /fs/_mapping/file
{
  "properties": {
    "name": { 
      "type":  "string",
      "index": "not_analyzed"
    },
    "path": { 
      "type":  "string",
      "index": "not_analyzed",
      "fields": {
        "tree": { 
          "type":     "string",
          "analyzer": "paths"
        }
      }
    }
  }
}
```

一旦索引建立并且文件已被编入索引，就可以在 `/clinton/projects/elasticsearch` 目录中包含 `elasticsearch` 的文件。

```json
GET /fs/file/_search
{
  "query": {
    "filtered": {
      "query": {
        "match": {
          "contents": "elasticsearch"
        }
      },
      "filter": {
        "term": { 
          "path": "/clinton/projects/elasticsearch"
        }
      }
    }
  }
}
```

或者

```json
GET /fs/file/_search
{
  "query": {
    "filtered": {
      "query": {
        "match": {
          "contents": "elasticsearch"
        }
      },
      "filter": {
        "term": { 
          "path.tree": "/clinton"
        }
      }
    }
  }
}
```

### 重命名文件和目录

```json
PUT /fs/file/1?version=2    // 确保该更改仅应用于索引中具有此相同版本号的文档
{
  "name":     "README.asciidoc",
  "path":     "/clinton/projects/elasticsearch",
  "contents": "Starting a new Elasticsearch project is easy..."
}
```

## 解决并发问题

如果多个人同时进行 重命名文件 或 目录 时，可能出现以下两种情况。

+ 当你使用 version 时，若与重命名的版本号产生冲突时，你的重命名操作将会失败。
+ 如果没有使用版本控制，你的变更将会覆盖其它用户的变更。

**解决方式:**

+ 如果你的主要数据存储是关系数据库，es 仅仅是作为一个 搜索引擎 或 一种提升性能 的方式。可以首先在数据库中执行变更动作，在完成后将变更录入 es，这种方式你将受益于 ACID 数据库事务的支持。并在 es 中以正确的顺序产生变更。

+ 如果不是在 关系型数据库 中，就得使用 es 的 全局锁、文档锁、树锁

### 全局锁

在 **任何时间** 只允许一个进程进行变更动作。另外由于大部分的变更都只涉及到少量的文件，因此会很快完成，不会造成较长时间的堵塞。这个方法 **锁定** 的是 **整个文件系统**。

es 支持文档级别的 ACID, 我们可以使用 **一个文档是否存在的状态** 来作为全局锁。

```json
// 为了请求得到锁，尝试 create 全局锁
// 如果这个请求因冲突异常而失败，说明另一个进程已被授予全局锁，稍后再进行尝试
PUT /fs/lock/global/_create
{}
```

完成变更以后，务必要释放全局锁

```json
DELETE /fs/lock/global
```

全局锁对系统造成的性能限制 和 变更的频繁程度以及单个变更的时间消耗有关。如果性能限制过大，可以通过 **细化锁粒度** 来增加并行度。

### 文档锁

文档锁顾名思义锁的是单个文档，也就任何时间只有一个进程可以修改某个文档。

```json
POST /fs/lock/1/_update
{
  "upsert": { "process_id": 123 },
  "script": "if ( ctx._source.process_id != process_id )
  { assert false }; ctx.op = 'noop';"
  "params": {
    "process_id": 123
  }
}
```

如果文档并不存在， `upsert` 文档将会被插入—和前面 `create` 请求相同。 但是，如果该文件 *确实* 存在，该脚本会查看存储在文档上的 `process_id` 。 如果 `process_id` 匹配，更新不会执行（ `noop` ）但脚本会返回成功。 如果两者并不匹配， `assert false` 抛出一个异常，你也知道了获取锁的尝试已经失败。

变更执行完以后务必释放掉所有的锁，检索所有的锁的文档，并进行批量删除。

```json
POST /fs/_refresh 

GET /fs/lock/_search?scroll=1m 
{
    "sort" : ["_doc"],
    "query": {
        "match" : {
            "process_id" : 123
        }
    }
}

PUT /fs/lock/_bulk
{ "delete": { "_id": 1}}
{ "delete": { "_id": 2}}
```

 ### 树锁

我们还可以锁定目录树的一部分，而不是锁定涉及到的每一个文档。我们将需要独占访问我们要重命名的文件或目录，它可以通过 **独占锁** 来实现。树锁用最小的代价提供了细粒度的并发控制，它也有不适应的场景，如：数据模型必须有类似目录树的顺序访问路径，才可以使用。

具体使用暂时不摘录了，没看懂。

### 总结

**如果持有锁的进程死了怎么办？** 我们需要考虑以下两个问题：

+ 我们如何知道我们可以释放的死亡进程中原本持有的锁？
+ 如何清理死去进程还未完成的变更？

**采用锁**，会带来 **复杂** 的实现逻辑，作为 **替代方案** ，es 提供两个模型帮助我们处理相关联的实体，嵌套的对象 和 父子关系。

## 嵌套对象

将相关的实体数据都存储在同一文档中，就可以利用文档的 ACIDic 来解决了。

比如：

```json
PUT /my_index/blogpost/1
{
  "title": "Nest eggs",
  "body":  "Making your money work...",
  "tags":  [ "cash", "shares" ],
  "comments": [ 
    {
      "name":    "John Smith",
      "comment": "Great article",
      "age":     28,
      "stars":   4,
      "date":    "2014-09-01"
    },
    {
      "name":    "Alice White",
      "comment": "More like this please",
      "age":     31,
      "stars":   5,
      "date":    "2014-10-22"
    }
  ]
}
```

但是如上的结构会导致下列查询也能返回数据：

```json
GET /_search
{
  "query": {
    "bool": {
      "must": [                             // 实际上 Alice 是 13 岁 而不是 28 岁
        { "match": { "name": "Alice" }},
        { "match": { "age":  28      }} 
      ]
    }
  }
}
```

这种 **问题** 出现是因为 es 存储的时候 **将 JSON 对象扁平化** 存储了，失去了姓名和年龄的对应关系了。

```json
{
  "title":            [ eggs, nest ],
  "body":             [ making, money, work, your ],
  "tags":             [ cash, shares ],
  "comments.name":    [ alice, john, smith, white ],
  "comments.comment": [ article, great, like, more, please, this ],
  "comments.age":     [ 28, 31 ],
  "comments.stars":   [ 4, 5 ],
  "comments.date":    [ 2014-09-01, 2014-10-22 ]
}
```

**嵌套对象** 可以解决这个问题。只需要将 `comments` 的字段类型设置为 `nested`。而不是 `object`。每一个嵌套对象都会被索引为一个 **隐藏的独立文档**。由于是隐藏的，如果要 **增删改** 一个嵌套对象，必须把整个文档都重新索引才可以。并且查询的时候，返回的是全部文档，而不仅是嵌套对象本身。

```json
{       // 嵌套文档
  "comments.name":    [ john, smith ],
  "comments.comment": [ article, great ],
  "comments.age":     [ 28 ],
  "comments.stars":   [ 4 ],
  "comments.date":    [ 2014-09-01 ]
}
{       // 嵌套文档
  "comments.name":    [ alice, white ],
  "comments.comment": [ like, more, please, this ],
  "comments.age":     [ 31 ],
  "comments.stars":   [ 5 ],
  "comments.date":    [ 2014-10-22 ]
}
{       // 根文档（或称父文档）
  "title":            [ eggs, nest ],
  "body":             [ making, money, work, your ],
  "tags":             [ cash, shares ]
}
```

嵌套文档 **优点**：

1. 嵌套文档 **直接存储** 在 文档内部，查询时，嵌套文档和根文档的 **联合成本低**，速度和单独存储的一样。
2. 嵌套文档中的每一个 嵌套对象 都是独立索引的，因此对象中的每一个 **相关性都会得以保留**，查询不会出错。

## 嵌套对象映射

设置一个对象为嵌套对象很简单，只需要将字段类型 object 替换为 nested 即可。

```json
PUT /my_index
{
  "mappings": {
    "blogpost": {
      "properties": {
        "comments": {
          "type": "nested", 
          "properties": {
            "name":    { "type": "string"  },
            "comment": { "type": "string"  },
            "age":     { "type": "short"   },
            "stars":   { "type": "short"   },
            "date":    { "type": "date"    }
          }
        }
      }
    }
  }
}
```

## 嵌套对象查询

需要使用 nested 查询去获取它们。

```json
GET /my_index/blogpost/_search
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "title": "eggs"              // 查询根文档
          }
        },
        {
          "nested": {                    // nested 子句作用于 comments 字段
            "path": "comments",          // 查询中，既不能查询文档字段，也不能查询其它的嵌套文档
            "query": {
              "bool": {
                "must": [ 
                  {
                    "match": {
                      "comments.name": "john"   // 具体这样点操作符操作
                    }
                  },
                  {
                    "match": {
                      "comments.age": 28
                    }
                  }
                ]
              }
            }
          }
        }
      ]
}}}
```

nested 字段 **可以包含** 其它的 nested 字段，同样地，nested 查询也 **可以包含** 其它的 nested 查询。

**nested 查询** 肯定可以匹配到多个嵌套的文档，每一个匹配的 **嵌套文档** 都有自己的相关度的分，但是众多分数最终需要汇聚为可供根文档使用的一个分数。默认情况，**根文档** 的分数是这些嵌套文档分数的 **平均值**。可以通过设置 score_mode 来控制这个得分策略（avg、max、sum、none-返回1.0 常数值分数）

## 使用嵌套字段排序

```json
PUT /my_index/blogpost/2
{
  "title": "Investment secrets",
  "body":  "What they don't tell you ...",
  "tags":  [ "shares", "equities" ],
  "comments": [
    {
      "name":    "Mary Brown",
      "comment": "Lies, lies, lies",
      "age":     42,
      "stars":   1,
      "date":    "2014-10-18"
    },
    {
      "name":    "John Smith",
      "comment": "You're making it up!",
      "age":     28,
      "stars":   2,
      "date":    "2014-10-16"
    }
  ]
}
```

假如我们想要查询 10月份收到评论的博客文档，按照 stars 数的最小值 升序排序，查询语句如下：

```json
GET /_search
{
  "query": {
    "nested": {                        // 筛选出了 10月份 收到评论的文章
      "path": "comments",
      "filter": {
        "range": {
          "comments.date": {
            "gte": "2014-10-01",
            "lt":  "2014-11-01"
          }
        }
      }
    }
  },
  "sort": {                                
    "comments.stars": {            // 按照匹配的评论中 comment.starts 字段的最小值 升序排序
      "order": "asc",   
      "mode":  "min",   
      "nested_path": "comments",   // 为什么在这里重复了一遍 nested_filter 呢?
      "nested_filter": {           // 排序发生在查询执行之后，查询条件限定了 10 月份收到评论的博客文档，但返回的是博客文档。
        "range": {                 // 如果我们不在排序子句中加入 nested_filter, 那博客文档的排序就是基于博客文档的所有评论，而不仅仅是 10 月份了
          "comments.date": {
            "gte": "2014-10-01",
            "lt":  "2014-11-01"
          }
        }
      }
    }
  }
}
```

## 嵌套聚合

nested 聚合允许我们对嵌套对象里的字段进行聚合操作

```json
GET /my_index/blogpost/_search
{
  "size" : 0,
  "aggs": {
    "comments": { 
      "nested": {
        "path": "comments"
      },
      "aggs": {
        "by_month": {
          "date_histogram": {                // comment 对象根据 comments.date 字段的月份值被分到不同的桶
            "field":    "comments.date",
            "interval": "month",
            "format":   "yyyy-MM"
          },
          "aggs": {
            "avg_stars": {
              "avg": {                       // 计算每个桶内 star 的平均数量
                "field": "comments.stars"
              }
            }
          }
        }
      }
    }
  }
}
```

嵌套结果：

```json
...
"aggregations": {
  "comments": {
     "doc_count": 4, 
     "by_month": {
        "buckets": [
           {
              "key_as_string": "2014-09",
              "key": 1409529600000,
              "doc_count": 1, 
              "avg_stars": {
                 "value": 4
              }
           },
           {
              "key_as_string": "2014-10",
              "key": 1412121600000,
              "doc_count": 3, 
              "avg_stars": {
                 "value": 2.6666666666666665
              }
           }
        ]
     }
  }
}
...
```

### 嵌套对象的使用时机

嵌套模型的 **缺点**：

+ 当对嵌套文档做 增加、修改、删除时，整个文档都要 **重新被索引**，嵌套文档越多，成本越大
+ 查询 **结果返回** 的不仅仅是匹配的嵌套文档，而是整个文档
+ 又是你需要在主文档和其关联实体之间做一个完整的隔离设计，这个隔离是由 **父子关联** 提供的。

## 父-子 关系文档

暂时不做记录了，再看也记不住，[链接](https://www.elastic.co/guide/cn/elasticsearch/guide/current/parent-child.html)

## 扩容设计

暂时不做记录了，再看也记不住，[链接](https://www.elastic.co/guide/cn/elasticsearch/guide/current/scale.html)



































































































































































































