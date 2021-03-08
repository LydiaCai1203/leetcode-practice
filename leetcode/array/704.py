"""
    二分查找：给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。
"""
from typing import List


class Solution:

    def search(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1
        
        begin, end = 0, len(nums) - 1

        while begin <= end:
            mid = int((end - begin) / 2)
            if nums[mid] == target:
                return mid
            elif nums[mid] > target:
                end = mid - 1
            else:
                begin = mid + 1
        
        return -1