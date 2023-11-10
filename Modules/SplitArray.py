def split_array_into_tuples(arr, n):
    if  n == 0:
        n = len(arr) // 3 if len(arr) >= 3 else len(arr)
    return [tuple(arr[i:i+n]) for i in range(0, len(arr), n)]