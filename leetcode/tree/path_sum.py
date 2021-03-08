"""
输入一棵二叉树和一个整数，打印出二叉树中节点值的和为输入整数的所有路径。从树的根节点开始往下一直到叶节点所经过的节点形成一条路径。
"""
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution:

    def pathSum(self, root: TreeNode, path_sum: int) -> List[List[int]]:
        single_path: str = ''
        all_pathes = []
        self.pre_order(root, single_path, path_sum, all_pathes)
        return all_pathes
    
    def pre_order(self, node: TreeNode, single_path: str, path_sum: int, all_pathes: list):
        """先序遍历树
        """
        if not node:
            return 

        if not node.left and not node.right:
            single_path += str(node.val)
            single_path_list = list(map(lambda val: int(val), single_path.split('|'))) 
            if sum(single_path_list) == path_sum:
                all_pathes.append(single_path_list)
        else:
            single_path += f'{node.val}|'
            self.pre_order(node.left, single_path, path_sum, all_pathes)
            self.pre_order(node.right, single_path, path_sum, all_pathes)