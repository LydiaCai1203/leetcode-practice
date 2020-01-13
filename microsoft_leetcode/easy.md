# 微软面试leetcode刷题

    王叔帮我找的内推 虽然对自己还是没什么信心，但是只有硬着头皮上了

[TOC]
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
**就是边界情况一定要考虑完全了 不然很容易就会出问题**
+ 只输入一个字符的时候
+ 最后还剩下两个字符
    + 两个字符一次就能匹配到
    + 两个字符要两次才能匹配到
+ 最后还剩下一个字符
    + 倒数第二个和第三个字符是一个key，offset=2
    + 倒数第二个字符是一个key
```python
class Solution:
    def romanToInt(self, s: str) -> int:
        # 大的数字+小的数字=加法
        # 小的数字+大的数字=减法(但并不是全部,只存在某些特殊情况)
        roman_number = {
            'I': 1, 'V': 5, 'IV': 4,
            'X': 10, 'L':50, 'IX': 9, 'XL': 40,
            'C': 100, 'XC': 90,
            'D': 500, 'M': 1000, 'CD': 400, 'CM': 900,
        }
        
        rst, first, second = 0, 0, 1
        
        if s in roman_number:
            return roman_number[s]
        
        while first <= len(s) - 2:
            key = s[first] + s[second]
            if key in roman_number:
                rst += roman_number[key]
                if second == len(s) - 2:
                    rst += roman_number[s[second+1]]
                first += 2
                second += 2
            else:
                # 没有的话就只能加上first对应的值，second还要和下一个字符匹配一下
                rst += roman_number[s[first]]
                if second == len(s) - 1:
                    rst += roman_number[s[second]]
                first += 1
                second += 1
        return rst
```

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
    class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        
        first, second = 0, 0
        
        if len(haystack) < len(needle):
            return -1
        
        while first < len(haystack):
            second = 0
            if haystack[first] != needle[second]:
                # 如果匹配不上就向后移一个位置
                first += 1
            else:
                # 如果第一个字符能匹配上的话
                pre = first
                flag = True
                for i in needle:
                    if haystack[pre] != needle[second]:
                        flag = False
                        break
                    pre += 1
                    second += 1
                if flag:
                    return first
        return -1
```

#### best solution:
```python
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if not needle or haystack == needle:
            return 0
        
        if len(haystack) < len(needle):
            return -1
        
        # 没必要遍历一边haystack 当haystack剩下的字符长度<needle的字符总长度 也就没有必要比了
        for i in range(len(haystack)-len(needle)+1):
            if haystack[i:i+len(needle)] == needle:
                return i
        return -1
```

--------------------------
### 101. 对称二叉树
    给定一个二叉树，检查它是否是镜像对称的。例如，二叉树 [1,2,2,3,4,4,3] 是对称的。
    如果你可以运用递归和迭代两种方法解决这个问题，会很加分。
#### 示例 1:
    镜像对称
```python
    1
   / \
  2   2
 / \ / \
3  4 4  3
```
#### 示例 2：
    镜像不对称
```python
    1
   / \
  2   2
   \   \
   3    3
```

#### solution
+ 1. 两棵树的根结点相同
+ 2. 两棵树，一棵树的左孩子等于另一棵树的右孩子
+ 3. 还要注意判断当结点为空的时候的情况
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        if not root:
            return True
        
        return self.check(root.left, root.right)
        
    
    def check(self, node1, node2):
        if not node1 and not node2:
            return True
        if not node1 or not node2:
            return False
        return node1.val == node2.val and self.check(node1.left, node2.right) and self.check(node1.right, node2.left)
```

--------------------------
### 112. 路径总和
    给定一个二叉树和一个目标和，判断该树中是否存在根节点到叶子节点的路径，这条路径上所有节点值相加等于目标和。说明: 叶子节点是指没有子节点的节点。
#### 示例 1：
    给定如下二叉树，以及目标和 sum = 22，返回 true, 因为存在目标和为 22 的根节点到叶子节点的路径 5->4->11->2。
```python
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
```
#### solution：
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def hasPathSum(self, root: TreeNode, sum: int) -> bool:
        if not root:
            return False
        
        sum -= root.val
        if not root.left and not root.right:
            # 说明是叶子结点
            return sum == 0
        
        # 如果还不是叶子结点的话
        return self.hasPathSum(root.left, sum) or self.hasPathSum(root.right, sum)
```

--------------------------
### 125. 验证回文串
    给定一个字符串，验证它是否是回文串，只考虑字母和数字字符，可以忽略字母的大小写。说明：本题中，我们将空字符串定义为有效的回文串。
#### 示例 1：
    输入: "A man, a plan, a canal: Panama"
    输出: true

#### 示例 2:
    输入: "race a car"
    输出: false

#### solution：
```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        if not s:
            return True
        
        s = ''.join(filter(lambda x: (x>='a' and x<='z') or (x>='A' and x<='Z') or (x>='0' and x<='9'), s)).lower()
        
        if len(s) % 2 == 0:
            # 说明是偶数长度
            return s[:len(s)//2] == s[len(s)//2:][::-1]
        else:
            return s[:len(s)//2] == s[len(s)//2+1:][::-1]
```

#### best solution:
```python
class Solution:
    def isPalindrome(self, s: str) -> bool:
        import re
        if not s:
            return True
        
        s = s.lower()
        s = re.sub(r'\W+', '', s, 0)
        
        return s == s[::-1]
```

--------------------------
### 171. Excel表列序号
    给定一个Excel表格中的列名称，返回其相应的列序号.
    A -> 1
    B -> 2
    C -> 3
    ...
    Z -> 26
    AA -> 27
    AB -> 28 
    ...
#### 示例 1:
    输入: "A"
    输出: 1
#### 示例 2:
    输入: "ZY"
    输出: 701
#### solution：
```python
class Solution:
    def titleToNumber(self, s: str) -> int:
        nums = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4,
            'E': 5, 'F': 6, 'G': 7, 'H': 8,
            'I': 9, 'J': 10, 'K': 11, 'L': 12,
            'M': 13, 'N': 14, 'O': 15, 'P': 16, 
            'Q': 17, 'R': 18, 'S': 19, 'T': 20,
            'U': 21, 'V': 22, 'W': 23, 'X': 24,
            'Y': 25, 'Z': 26
        }
        
        rst = 0
        for index, value in enumerate(s[::-1]):
            rst += nums[value] * (26 ** index)
        
        return rst
```

#### best solution:
```python
class Solution:
    def titleToNumber(self, s: str) -> int:
        rst = 0
        for i in s:
            rst *= 26
            rst += ord(i) - 64
        return rst
```

--------------------------
### 189. 旋转数组
    给定一个数组，将数组中的元素向右移动 k 个位置，其中 k 是非负数。
#### 示例 1：
    输入: [1,2,3,4,5,6,7] 和 k = 3
    输出: [5,6,7,1,2,3,4]
    解释:
    向右旋转 1 步: [7,1,2,3,4,5,6]
    向右旋转 2 步: [6,7,1,2,3,4,5]
    向右旋转 3 步: [5,6,7,1,2,3,4]
#### 示例 2：
    输入: [-1,-100,3,99] 和 k = 2
    输出: [3,99,-1,-100]
    解释: 
    向右旋转 1 步: [99,-1,-100,3]
    向右旋转 2 步: [3,99,-1,-100]
#### solution：
```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        if len(nums) == 1 or not nums:
            return None
        
        k = k % len(nums)
        self.reverse(0, len(nums)-1, nums)
        self.reverse(0, k-1, nums)
        self.reverse(k, len(nums)-1, nums)
        
        
    def reverse(self, start, end, nums):
        while(start<end):
            tmp = nums[start]
            nums[start] = nums[end]
            nums[end] = tmp
            start += 1
            end -= 1
        
```

#### best solution:
```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums) 
        # 注意看这个 为什么nums[:] = ... 但是nums[:] 不是开辟一块新的空间吗
        nums[:]= nums[len(nums)-k:] + nums[0:len(nums)-k]
```

--------------------------
### 191. 位1的个数
    编写一个函数，输入是一个无符号整数，返回其二进制表达式中数字位数为 ‘1’ 的个数（也被称为汉明重量）。
#### 示例 1:
    输入：00000000000000000000000000001011
    输出：3
    解释：输入的二进制串 00000000000000000000000000001011 中，共有三位为 '1'。
#### 示例 2:
    输入：00000000000000000000000010000000
    输出：1
    解释：输入的二进制串 00000000000000000000000010000000 中，共有一位为 '1'。
#### 示例 3:
    输入：11111111111111111111111111111101
    输出：31
    解释：输入的二进制串 11111111111111111111111111111101 中，共有 31 位为 '1'。
#### solution:
```python
class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        return str(bin(n)).count('1')
```

#### best solution:
```python
class Solution(object):
    def hammingWeight(self, n):
        """
        :type n: int
        :rtype: int
        """
        cnt = 0
        while n:
            if n & 1:
                cnt += 1
            n >>= 1
        return cnt
```

--------------------------
### 204. 计数质数
    统计所有小于非负整数 n 的质数的数量。
#### 示例 1:
    输入: 10
    输出: 4
    解释: 小于 10 的质数一共有 4 个, 它们是 2, 3, 5, 7 。
#### solution：
    使用厄拉多塞筛法进行筛选
```python
    class Solution:
    def countPrimes(self, n):
        count = 0
        signs = [True] * n
        for i in range(2, n):
            if signs[i]:
                count += 1
                for j in range(i+i, n, i):
                    signs[j] = False
        return count
```
#### another solution:
    实际上不需要全部都遍历一遍 只需要遍历一半即可
```python
class Solution:
    def countPrimes(self, n):
        if n == 0 or n == 1:
            return 0
        signs = [1] * n
        signs[0], signs[1] = 0, 0
        for i in range(2, n//2+1):
            if signs[i]:
                for j in range(i+i, n, i):
                    signs[j] = 0
        return sum(signs)
```
#### best solution:
```python
class Solution:
    def countPrimes(self, n):
        if n < 2: return 0
        isPrimes = [1] * n
        isPrimes[0] = isPrimes[1] = 0
        for i in range(2, int(n ** 0.5) + 1):    #range(2, 3)
            if isPrimes[i] == 1:
                # [4:10:2] = [0] * [4:10:2] 注意这一句的写法
                isPrimes[i * i: n: i] = [0] * len(isPrimes[i * i: n: i])
        return sum(isPrimes)
```

--------------------------
### 232. 用栈实现队列
    push(x) -- 将一个元素放入队列的尾部。
    pop() -- 从队列首部移除元素。
    peek() -- 返回队列首部的元素。
    empty() -- 返回队列是否为空。

#### 示例 1:
```python
MyQueue queue = new MyQueue();
queue.push(1);
queue.push(2);  
queue.peek();  // 返回 1
queue.pop();   // 返回 1
queue.empty(); // 返回 false
```

#### solution:
```python
    class MyQueue:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.l = []
        
    def push(self, x: int) -> None:
        """
        Push element x to the back of queue.
        """
        self.l.append(x)
        
    def pop(self) -> int:
        """
        Removes the element from in front of queue and returns that element.
        """
        return self.l.pop(0)
        
    def peek(self) -> int:
        """
        Get the front element.
        """
        return self.l[0]
        
    def empty(self) -> bool:
        """
        Returns whether the queue is empty.
        """
        return len(self.l)==0
        
# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()
```

--------------------------
### 237. 删除链表中的节点
    请编写一个函数，使其可以删除某个链表中给定的（非末尾）节点，你将只被给定要求被删除的节点。
    现有一个链表 -- head = [4,5,1,9]，它可以表示为:
    4->5->1->9
    其实传入的node参数是 链表里面的某个结点，所以可以直接在上面进行操作
#### 示例 1
    输入: head = [4,5,1,9], node = 5
    输出: [4,1,9]
    解释: 给定你链表中值为 5 的第二个节点，那么在调用了你的函数之后，该链表应变为 4 -> 1 -> 9.
#### 示例 2
    输入: head = [4,5,1,9], node = 1
    输出: [4,5,9]
    解释: 给定你链表中值为 1 的第三个节点，那么在调用了你的函数之后，该链表应变为 4 -> 5 -> 9.
#### 说明
    链表至少包含两个节点。
    链表中所有节点的值都是唯一的。
    给定的节点为非末尾节点并且一定是链表中的一个有效节点。
    不要从你的函数中返回任何结果。
#### solution：
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteNode(self, node):
        """
        :type node: ListNode
        :rtype: void Do not return anything, modify node in-place instead.
        """
        node.val = node.next.val
        node.next = node.next.next
```

--------------------------
### 258. 各位相加
    给定一个非负整数 num，反复将各个位上的数字相加，直到结果为一位数。
    你可以不使用循环或者递归，且在 O(1) 时间复杂度内解决这个问题吗？
#### 示例 1
    输入: 38
    输出: 2 
    解释: 各位相加的过程为：3 + 8 = 11, 1 + 1 = 2。 由于 2 是一位数，所以返回 2。

#### solution
```python
class Solution:
    def addDigits(self, num: int) -> int:
        
        while num // 10:
            num = num % 10 + num // 10
            
        return num
```

#### best solution:
+ 1. 比如4399 假设现在有一个字符串'4399' 相当于abcd
+ 2. old_value = 1000 * a + 100 * b + 10 * c + d
+ 3. new_value = a + b + c + d
+ 4. old_value - new_value = 999a + 99b+ 9c = 9(111a+11b+c)
+ 5. 所以说每次都是减去一个9的倍数的值
+ 6. 9*value1 + 9*value2 + ... + nums(<9) = old_value
+ 7. 所以说只有取9的模就是最后的结果了

```python
class Solution:
    def addDigits(self, num: int) -> int:
        return num if num == 0 else num % 9 or 9
```

--------------------------
### 270. 最接近的二叉搜索树值(注意是搜索树)
    给定一个不为空的二叉搜索树和一个目标值 target，请在该二叉搜索树中找到最接近目标值 target 的数值。
    注意：
    给定的目标值 target 是一个浮点数
    题目保证在该二叉搜索树中只会存在一个最接近目标值的数
#### 示例 1:
```python
输入: root = [4,2,5,1,3]，目标值 target = 3.714286

    4
   / \
  2   5
 / \
1   3

输出: 4
```
#### 准备活动：
```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

# 测试数据
root = TreeNode(4)
root_left = TreeNode(2)
root_right = TreeNode(5)
left_left = TreeNode(1)
left_right = TreeNode(3)
root.left = root_left
root.right = root_right
root_left.left = left_left
root_left.right = left_right
```

#### 前序遍历
```python
def preorder(root):
    if not root:
        return
    print(root.val)
    preorder(root.left)
    preorder(root.right)
```

#### 中序遍历
```python
def midorder(root):
    if not root:
        return
    midorder(root.left)
    print(root.val)
    midorder(root.right)
```

#### 后序遍历
```python
def postorder(root):
    if not root:
        return
    postorder(root.left)
    postorder(root.right)
    print(root.val)
```

#### solution：
```python
class Solution:
    def closestValue(self, root: TreeNode, target: float) -> int:
        
        #if (target > root.val and not root.right) or \ 
        #   (target < root.val and not root.left) or (not root.right and not root.left):
        #    return root.val
        values = {}
    
        def inner(root, target):
            if not root:
                min_key = min(values.keys())
                return values[min_key]
    
            values[abs(target-root.val)] = root.val
            
            if target == root.val:
                return root.val
            
            if target > root.val:
                a = inner(root.right, target)
                return a
            if target < root.val:
                b = inner(root.left, target)
                return b
            
        return inner(root, target)
```

--------------------------
### 387. 字符串中的第一个唯一字符
    给定一个字符串，找到它的第一个不重复的字符，并返回它的索引。如果不存在，则返回 -1。
#### 示例 1：
    s = "leetcode"
    返回 0.

    s = "loveleetcode"
    返回 2.
#### solution：
```python
    class Solution:
    def firstUniqChar(self, s: str) -> int:
        import collections
        a = collections.Counter(s)    # 这个也要算时间复杂度才对啊
        for key in a:
            if a[key] == 1:
                return s.index(key)
                break
        return -1
```

--------------------------
### 443. 压缩字符串
    给定一组字符，使用原地算法将其压缩。压缩后的长度必须始终小于或等于原数组长度。数组的每个元素应该是长度为1 的字符（不是 int 整数类型）。在完成原地修改输入数组后，返回数组的新长度。

    注意: 所有字符都有一个ASCII值在[35, 126]区间内。1 <= len(chars) <= 1000。
#### 示例 1：
```python
输入：
["a","a","b","b","c","c","c"]

输出：
返回6，输入数组的前6个字符应该是：["a","2","b","2","c","3"]

说明：
"aa"被"a2"替代。"bb"被"b2"替代。"ccc"被"c3"替代。
```
#### 示例 2：
```python
输入：
["a"]

输出：
返回1，输入数组的前1个字符应该是：["a"]

说明：
没有任何字符串被替代。
```
#### 示例 3:
```python
输入：
["a","b","b","b","b","b","b","b","b","b","b","b","b"]

输出：
返回4，输入数组的前4个字符应该是：["a","b","1","2"]。

说明：
由于字符"a"不重复，所以不会被压缩。"bbbbbbbbbbbb"被“b12”替代。
注意每个数字在数组中都有它自己的位置。
```
#### solution:
```python

```

--------------------------
### . 压缩字符串