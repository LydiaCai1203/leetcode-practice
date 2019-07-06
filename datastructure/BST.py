"""
Implements of Binary Search Tree
"""

class Node(object):
    self.data = data
    self.left = None
    self.right_child = Node


class Mytree(object):
    
    def __init__(self, node):
        # self.cur就是指的当前结点所在位置
        self.cur = node

    def insert_left(self, node):
        if not self.left:
            self.left = node
        else:
            cur_node = self.cur
            parent_node = None
            while(not cur_node):
                parent_node = cur_node
                cur_node = cur_node.left
            cur_node.left = node

    def insert_right(self, node):
        if not self.right:
            self.right = node
        else:
            cur_node = self.cur
            parent_node = None
            while(not cur_node):
                parent_node = cur_node
                cur_node = cur_node.right
            cur_node.right = node
    