"""
    单链表反转：
    1. 输入空链表处理
    2. 三个指针实现(head, head_next, tmp)，tmp 始终等于 head_next.next
    3. 注意首轮循环，head 和 head_next 之间循环指向 1->2 && 2<-1
"""
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

def create_list_node(length=5):
    """创建单链表
    """
    node_list = [ListNode(i) for i in range(1, length+1)]
    for index, node in enumerate(node_list):
        cur = node
        if index == (length - 1):
            nxt = None
        else:
            nxt = node_list[index+1]
        cur.next = nxt
    return node_list[0] if node_list else None

def reverse(head: ListNode):
    """单链表反转 - 循环实现
    """
    if not head:
        return head

    head_next = head.next
    head.next = None
    while head_next:
        tmp = head_next.next
        head_next.next = head
        head = head_next
        head_next = tmp
    return head

def best_solution(head: ListNode):
    """最优解
    """
    pre, cur = None, head
    while cur:
        tmp = cur.next
        cur.next = pre
        pre = cur
        cur = tmp
    return pre


if __name__ == "__main__":
    head = create_list_node(4)
    head_next = reverse(head)

    node = head_next
    while node:
        print(node.val)
        node = node.next