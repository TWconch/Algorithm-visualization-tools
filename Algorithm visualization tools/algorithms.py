import time

def bubble_sort(data):
    steps = []
    arr = data[:]
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            steps.append((arr[:], (j, j+1), False))  # 比較
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append((arr[:], (j, j+1), True))  # 交換
    return steps

def insertion_sort(data):
    steps = []
    arr = data[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # 暫時用一個變數記錄目前狀態
        temp = arr[:]
        # 在 key 被「拿起來」的時候，先記錄一次
        steps.append((temp[:], (j, i), False))

        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]
            temp = arr[:]
            temp[j] = key   # 把 key 保持在動畫中，不要消失
            steps.append((temp[:], (j, j+1), True))
            j -= 1
            
        arr[j+1] = key
        steps.append((arr[:], (j+1, i), False))     # 插入完成
    return steps
