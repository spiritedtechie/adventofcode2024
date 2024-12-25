from collections import defaultdict
from itertools import product


def read_file(filename):
    with open(filename) as file:
        blocks = file.read().strip().split("\n\n")
        return [[list(line) for line in block.splitlines()] for block in blocks]


def convert_to_heights(grid):
    return [sum(1 for cell in col if cell == "#") - 1 for col in zip(*grid)]


def group_by_type(grids):
    lock_keys = defaultdict(list)
    for grid in grids:
        key_type = "lock" if grid[0][0] == "#" else "key"
        lock_keys[key_type].append(convert_to_heights(grid))
    return lock_keys


def does_key_fit_lock(key, lock, max_height=6):
    return all(h1 + h2 < max_height for h1, h2 in zip(key, lock))


# Main
grids = read_file("day25.txt")
lk = group_by_type(grids)

count = sum(
    1 for lock, key in product(lk["lock"], lk["key"]) if does_key_fit_lock(key, lock)
)
print("part 1:", count)
