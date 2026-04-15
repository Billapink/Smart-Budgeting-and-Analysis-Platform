def merge_sort(data):
    L = len(data)
    if L < 2:  # base case: zero or one elements in the list; nothing to sort
        return data
    
    # recursively sorting 
    split = L // 2 
    left = merge_sort(data[:split]) 
    right = merge_sort(data[split:])

    merged = []

    while len(left)>0 and len(right)>0:
        # take the smallest value from the front of the left or right lists and append to the merged list
        if left[0] < right[0]:
            next = left.pop(0)
        else:
            next = right.pop(0)
        merged.append(next)
    
    # either left or right still has values. these need to be appended
    if len(left)>0:
        merged.extend(left)
    
    if len(right)>0:
        merged.extend(right)

    return merged
