# 微软面试leetcode刷题

    王叔帮我找的内推 虽然对自己还是没什么信心，但是只有硬着头皮上了

---------------------------------------
### 1. 两数之和
    给定一个整数数组nums和一个目标值target，请在这个数组中找出和为target的那两个整数，并返回它们的数组下标

#### 示例
    nums = [2, 7, 11, 15], target = 9
    nums[0] + nums[1] = 2 + 7 = 9
    return [0, 1]

#### solution
#### 精髓就是：判断出rest在nums里面以后,怎么找到rest的index。需要同时能存(index, value)
```python
def twosum(nums, target):
    value = {}
    for index, num in enumerate(nums):
        rest = target - num
        if rest in value:
            return [nums[rest], index]
        nums[rest] = index
```

---------------------------------------
### 2. 整数反转
    给出一个 32 位的有符号整数，你需要将这个整数中每位上的数字进行反转。
    假设我们的环境只能存储得下 32 位的有符号整数，则其数值范围为 [−231,  231 − 1]。请根据这个假设，如果反转后整数溢出那么就返回 0。

#### 示例1
    输入: 123
    输出: 321
#### 示例2
    输入: -123
    输出: -321
#### 示例3
    输入: 120
    输出: 21

#### my_solution
```python
class Solution:
    def reverse(self, x: int) -> int:
        str_x = str(x)
        
        if x < 0:
            str_rst = str_x[0] + str_x[1:][::-1]
        else:
            str_rst = str_x[::-1]
        
        int_rst = int(str_rst)
        if int_rst < -2**31 or int_rst > 2**31-1:
            return 0
        return int_rst
```

#### 其实也可以用栈方法 还有queue的leftextend() 这些都是可以反转的方法

#### another solution(但是效率很低)
    不在string和int之间相互转换 使用数学方法 一边拿一边存一边转换一边判断

```python
class Solution:
    def reverse(self, x: int) -> int:
        flag = True if x > 0 else False
        x = abs(x)
        
        value = 0
        while x:
            value = value * 10 + x % 10
            x = x // 10
        
        value = value if flag else -value
        if value < -(2**31) or value > (2**31)-1:
            return 0
        return value
```

---------------------------------------
### 53. 最大子序和
    给定一个整数数组 nums ，找到一个具有最大和的连续子数组（子数组最少包含一个元素），返回其最大和。
#### 示例
    输入: [-2,1,-3,4,-1,2,1,-5,4],
    输出: 6
    解释: 连续子数组 [4,-1,2,1] 的和最大，为 6。

#### 动态规划解释
+ F(i)表示下标为i的时候，连续数组的最大和
+ 状态转移方程： max(F(i-1)+num[i], num[i])
+ 初始状态：F(0) = num[0]
+ 返回值： F(len(num)-1)
```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        for index in range(1, len(nums)):
            nums[index] = nums[index] + max(nums[index-1], 0)
        # 应该是慢在这里
        return max(nums)
```

#### 分冶法解释
+ 最大子序 要么在左边 要么在右边 要么穿过两边

---------------------------------------
### 21. 合并两个有序列表
    将两个有序链表合并为一个新的有序链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 
#### 示例
    输入：1->2->4, 1->3->4
    输出：1->1->2->3->4->4

#### solution
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        
        if not l1:
            return l2
        if not l2:
            return l1
        
        if l1.val <= l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        
        if l1.val > l2.val:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2
```

---------------------------------------
### 26. 删除排序数组中的重复项
    给定一个排序数组，你需要在原地删除重复出现的元素，使得每个元素只出现一次，返回移除后数组的新长度。
    不要使用额外的数组空间，你必须在原地修改输入数组并在使用 O(1) 额外空间的条件下完成。

#### 示例 1:
    给定数组 nums = [1,1,2], 
    函数应该返回新的长度 2, 并且原数组 nums 的前两个元素被修改为 1, 2。 
    你不需要考虑数组中超出新长度后面的元素。

#### 示例 2:
    给定 nums = [0,0,1,1,1,2,2,3,3,4],
    函数应该返回新的长度 5, 并且原数组 nums 的前五个元素被修改为 0, 1, 2, 3, 4。
    你不需要考虑数组中超出新长度后面的元素。

#### solution:
```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        slow = 0
        quick = 1
        length = len(nums)
        while(quick < length):
            if nums[quick] == nums[slow]:
                quick += 1
            else:
                slow += 1
                nums[slow] = nums[quick]
        return (slow + 1)
```

---------------------------------------
### 169. 求众数
    
    给定一个大小为 n 的数组，找到其中的众数。众数是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。
    你可以假设数组是非空的，并且给定的数组总是存在众数。

#### 示例 1：
    输入: [3,2,3]
    输出: 3

#### 示例 2:
    输入: [2,2,1,1,1,2,2]
    输出: 2

#### solution:
    先排序 再找中间的数 中间的数肯定就是众数
```python
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        nums = sorted(nums)
        return nums[len(nums)//2]
```

---------------------------------------
### 182. 查找重复的电子邮箱

    编写一个 SQL 查询，查找 Person 表中所有重复的电子邮箱。
#### 示例 1:
```mysql5
+----+---------+
| Id | Email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
```

#### 应当返回的结果为：
```mysql5
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```

#### solution
```python
select Email
from Person
group by Email
having count(id) > 1;
```

---------------------------------------
### 70. 爬楼梯
    假设你正在爬楼梯。需要 n 阶你才能到达楼顶。
    每次你可以爬 1 或 2 个台阶。你有多少种不同的方法可以爬到楼顶呢？
    注意：给定 n 是一个正整数

#### 示例 1：
    输入： 2
    输出： 2
    解释： 有两种方法可以爬到楼顶。
    1.  1 阶 + 1 阶
    2.  2 阶

#### solution(但是使用递归会超出时间限制):
+ F(i) 表示 需要走i步的时候 有几种走法
+ 状态转移方程： F(i) = F(i-1) + F(i-2)
+ 初始状态：F(1) = 1; F(2) = 2; F(3) = F(1) + F(2) = 3
+ 返回值： F(i)
    
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        steps = self.climbStairs(n-1) + self.climbStairs(n-2)
        return steps
```

#### solution(优化 执行之间还是太长了)：
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        nums = [None] * n
        for i in range(n):
            if i == 0:
                nums[i] = 1
                continue
            if i == 1:
                nums[i] = 2
                continue
            nums[i] = nums[i-1] + nums[i-2]
        return nums[-1]
```

#### solution(再优化！！！)
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        first = 1
        second = 2
        
        if n == 1:
            return 1
        if n == 2:
            return 2
        
        for i in range(n-2):
            first, second = second, first + second
            
        return second
```

---------------------------------------
### 13. 罗马数字转整数
```python
字符          数值
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
```
    例如， 罗马数字 2 写做 II ，即为两个并列的 1。12 写做 XII ，即为 X + II 。 27 写做  XXVII, 即为 XX + V + II 。
    通常情况下，罗马数字中小的数字在大的数字的右边。但也存在特例，例如 4 不写做 IIII，而是 IV。数字 1 在数字 5 的左边，所表示的数等于大数 5 减小数 1 得到的数值 4 。同样地，数字 9 表示为 IX。这个特殊的规则只适用于以下六种情况：
+ I 可以放在 V (5) 和 X (10) 的左边，来表示 4 和 9。
+ X 可以放在 L (50) 和 C (100) 的左边，来表示 40 和 90。
+ C 可以放在 D (500) 和 M (1000) 的左边，来表示 400 和 900。

#### 示例 1:    
    输入: "LVIII"
    输出: 58
    解释: L = 50, V= 5, III = 3.

#### 示例 2：
    输入: "MCMXCIV"
    输出: 1994
    解释: M = 1000, CM = 900, XC = 90, IV = 4.

#### solution:
    pass

--------------------------
### 28. 实现 strStr()
    给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。
    当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。
    对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。

#### 示例 1:
    输入: haystack = "hello", needle = "ll"
    输出: 2
#### 示例 2：
    输入: haystack = "aaaaa", needle = "bba"
    输出: -1

#### solution：
```python
    pass
```
