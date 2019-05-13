"""
Implements of Binary Search Tree
"""

class BST(object):
    
    def __init__(self, node):
        self.cur = node
        self.left_child = None
        self.right_child = None

    def insert(self, root, node):
        """
        if node greater than cur_node.cur, and insert into right node
        if node less than cur_node.cur and insert into left node
        """
        if not :
            self.cur = BST(node)
        
        if node <= self.left_child:
            self.left_child = self.insert(node)
        
        if node > self.right_child:
            self.right_child = self.insert(node)
        return node
        