## 第六章：内核数据结构

### 6.1 链表

```markdown
链表：
1. 所包含的元素都是动态创建并插入链表的，在编译时不必知道具体需要创建多少个元素。
2. 链表中的各个元素在内存中无须占用连续内存区。因此每个元素都包含一个指向下一个元素的指针。
```

#### 6.1.1 单向链表 和 双向链表

```c
// 单向链表
struct list_elemant {
  void *data;
  struct list_element *next;    
}
```

```c
// 单向链表
struct list_elemant {
  void *data;
  struct list_element *next;
  struct list_element *prev;
}
```

#### 6.1.2 环形链表

```markdown
通常情况下，链表的最后一个元素中的 `*next=NULL`, 环形链表中，链表首尾相连。当然环形链表也分 环形单向链表 和 环形双向链表。因为环形双向链表提供了最大的灵活性，所以 Linux 内核的标准链表采用的是环形双向链表。
```

#### 6.1.3 沿链表移动

```markdown
沿链表移动只能是线性移动，通过沿该元素的向后指针去访问下一个元素，不断重复。链表并不适合随机访问数据，适合需要遍历所有的原序或需要动态地增加和删除数据。
```

#### 6.1.4 Linux 内核中的实现

```c
struct fox {
  unsigned long tail_length;           // 尾巴长度8
  unsigned long weight;                // 重量
  bool is_fantastic;                   // 这只狐狸奇妙吗？
}
```

```c
/* Linux 内核不是将数据结构塞入链表，而是将链表节点塞入数据结构 */
struct fox {
  unsigned long tail_length; // 尾巴长度
  unsigned long weight; // 重量
  bool is_fantastic; // 这只狐狸奇妙吗？
  struct fox *next;
  struct fox *prev;
}
```

**1. 链表数据结构**

```markdown
在 Linux 2.1 内核开发系列中，首次引入了官方内核链表的实现。链表代码在头文件 `<linux/list.h>` 中声明。
```

```c
struct list_head {
  struct list_head *next;
  struct list_head *prev;
}

struct fox {
  unsigned long tail_length; // 尾巴长度
  unsigned long weight; // 重量
  bool is_fantastic; // 这只狐狸奇妙吗？
  struct list_head list; // fox.list.prev 指向前一个元素，fox.list.next 指向后一个元素
}
```

```markdown
内核又提供了一组链表操作例程，比如 `list_add()` 加入一个新节点到链表中。所有的链表操作例程都只接收 `list_head` 结构作为参数。不过使用 `container_of(ptr, type, member)` 可以让我们很方便地从链表指针找到父结构中包含的任何变量。因此依靠 `container_of` 就可以获得包含 `list_head` 的父类型结构体。这样我们使用 这些链表操作例程 也就不需要知道锁嵌入对象的数据结构是什么了。
```












