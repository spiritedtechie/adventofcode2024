def read_file(filename):
    with open(filename) as file:
        for line in file:
            yield list(map(int, line.split()))

def is_safe(row:list) -> bool:    
    diffs = [j - i for i,j in zip(row, row[1:])]
    return all(-3 <= n <=-1 for n in diffs) or all(1 <= n <= 3 for n in diffs)

def is_safe_dampened(row:list) -> bool:    
    row_with_item_removed = lambda row, index_to_remove : row[:index_to_remove] + row[index_to_remove+1:]
    return is_safe(row) or any(is_safe(row_with_item_removed(row, i)) for i in range(len(row)))


if __name__ == "__main__":
    rows = read_file("day2.txt")
    print(sum(1 for row in rows if is_safe(row)))

    rows = read_file("day2.txt")
    print(sum(1 for row in rows if is_safe_dampened(row)))

    # print(is_safe_dampened([7, 6, 4, 2, 1]))
    # print(is_safe_dampened([1, 2, 7, 8, 9]))
    # print(is_safe_dampened([9, 7, 6, 2, 1]))
    # print(is_safe_dampened([1, 3, 2, 4, 5]))
    # print(is_safe_dampened([8, 6, 4, 4, 1]))
    # print(is_safe_dampened([1, 3, 6, 7, 9]))

