import random

sum = 0

def quicksort_v1(array: list) -> list:
    """这个解法没有考虑重复值
    """
    if len(array) < 2:
        return array

    pivot = array[0]
    left_array = [i for i in array if i < pivot]
    right_array = [i for i in array if i > pivot]
    return quicksort_v1(left_array) + [pivot] + quicksort_v1(right_array)

def quicksort_v2(array: list, begin: int, end: int) -> None:
    """升序 + 左指针找大 + 右指针找小的, 右边的指针先动
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


def main():
    array = list(range(10))
    random.shuffle(array)

    print("排序前：", array)
    quicksort_v2(array, 0, len(array)-1)
    print("排序后", array)

    sorted()

main()