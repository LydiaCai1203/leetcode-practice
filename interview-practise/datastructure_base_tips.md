## REVIEW OF DATASTRUCTURE

[笨方法学算法](https://python-data-structures-and-algorithms.readthedocs.io/zh/latest/)

------------------
### 1. 几大排序算法

#### 排序算法的执行效率从：
    1. 时间复杂度（最好情况下的时间复杂度，最坏情况下的时间复杂度，平均时间复杂度）
    2. 时间复杂度的系数、常数、低阶 这些都是可以忽略掉的(N特别打的前提下)
    3. 求的其实是比较次数和交换以及移动的次数
    4. 排序算法的内存消耗
    5. 排序算法的稳定性

##### 因为实际开发中，要排序的往往是一组对象，排序的往往是对象的某个key进行排序，但是对象还有其它的属性值，稳定排序算法可以保证对象在排序的时候，key相同的对象之间的相对顺序是正确的。

#### 冒泡排序：
    空间复杂度O(1)       # 是一个原地排序算法
    稳定
    最好的时间复杂度O(N)  # 只需要循环一次，但是元素需要交换N-1次，(N-1)+1=N 
    最坏的时间复杂度O(N)  # 最坏的情况就是循环N-1次，[1+2+3+...+(N-1)] + (N-1) 约等于 N**2
    平均的时间复杂度O(N)  # O(N**2)

#### 插入排序
    首先有一个有序数组，将要插入的数依此和这个有序数组里面的每一个数做对比，然后比较大小进行插入。
    空间复杂度O(1) 
    稳定
    最好的时间复杂度O(N)
    最坏的时间复杂度O(N**2)
    平均的时间复杂度O(N**2)

**实现：**

```python3
def insertion_sort(array):
    """插排
    """
    for index, value in enumerate(array):

        pos = index
        while pos > 0 and value < array[pos-1]:
            array[pos] = array[pos-1]
            pos -= 1
        array[pos] = value
```

#### 选择排序

    每次都会从无序数组中找出最小的，然后放在有序数组的末尾
    空间复杂度O(1)
    不稳定
    最好的时间复杂度O(N**2)
    最坏的时间复杂度O(N**2)
    平均的时间复杂度O(N**2)

**以上三种排序算法适合小规模的排序**

#### 归并排序
    首先有一堆数组，然后一分为二，再分别将两组一分为二，一直分，直到每个小组都只有两个元素，然后再将小组进行归并，
    合成一个有序的长数组。
    稳定
    最好的时间复杂度O(NlogN)
    最坏的时间复杂度O(NlogN)
    平均的时间复杂度O(NlogN)

#### 快速排序
[理解哨兵的算法看这里，这个比较好懂](https://blog.csdn.net/kmyhy/article/details/82991482)

    首先有一堆数组，然后N/2取一个值当pivot, 将所有比pivot小的都排到左边，所有比pivot大的都排到右边去，递归
    空间复杂度 O(1)
    不稳定
    最好的时间复杂度O(NlogN)
    最坏的时间复杂度O(N**2)
    平均的时间复杂度O(NlogN)

**工作过程：**

+ 选择基准值 pivot 将数组分为两个子数组：小于基准值的元素排到左边，大于基准值的元素排到右边，这个过程称为 partition
+ 对子数组再分区，排序，直到有序为止

**实现**：

```python3
# v1 -- 1. 这个解法没有考虑有重复值的情况 2. 使用了额外的存储空间 3. 每次都要两次遍历数组
# 这个算法时间复杂度最好的情况也要 O(2NlogN)

def quicksort(array: list):
		if len(array) < 2:
				return array
    
		pivot = array[0]
		left_array = [i for i in array if i < pivot]
		right_array = [i for i in array if i > pivot]
		return left_array + [pivot] + right_array
```

```python3
# v2 -- 使用双指针 + pivot 的方式，左指针 负责找到比 pivot 更大的，右指针 负责找到比 pivot 更小的
# 谁找到了就停下，没找的继续往左/右挪，直到 l == r, 然后将 pivot 与 l(r) 指向的元素交换
# 递归重复上面步骤即可

def quicksort_v2(array: list, begin: int, end: int) -> None:
    """
    	升序 + 左指针找大 + 右指针找小的, 右边的指针先动
    	注意处理 [2, 4, 3] 的情况
    """
    
    if begin >= end:
        return 

    pivot_idx = begin
    pivot = array[pivot_idx]

    left, right = begin + 1, end

    while True:
        while True:
            if left >= right or array[right] < pivot:
                break
            right = right - 1
        
        while True:
            if left >= right or array[left] > pivot:
                break
            left = left + 1

        if left != right:
            array[left], array[right] = array[right], array[left]
        else:
            break
    
    flag = False
    if array[pivot_idx] > array[left]:
        array[pivot_idx], array[left] = array[left], array[pivot_idx]
        flag = True

    # 左边数组快排
    quicksort_v2(array, begin, left-1)
    # 右边数组快排
    quicksort_v2(array, left+1 if flag else left, end)
```



























































