import heapq
from itertools import *
from functools import cache

# Keypad entries and adjacent neighbours (and direction to get to them)
NUMERIC_KEYPAD = {
    "0": [("2", "^"), ("A", ">")],
    "1": [("2", ">"), ("4", "^")],
    "2": [("0", "v"), ("1", "<"), ("3", ">"), ("5", "^")],
    "3": [("2", "<"), ("6", "^"), ("A", "v")],
    "4": [("1", "v"), ("5", ">"), ("7", "^")],
    "5": [("2", "v"), ("4", "<"), ("6", ">"), ("8", "^")],
    "6": [("3", "v"), ("5", "<"), ("9", "^")],
    "7": [("4", "v"), ("8", ">")],
    "8": [("5", "v"), ("7", "<"), ("9", ">")],
    "9": [("6", "v"), ("8", "<")],
    "A": [("0", "<"), ("3", "^")],
}

DIRECTIONAL_KEYPAD = {
    "^": [("A", ">"), ("v", "v")],
    "v": [("<", "<"), (">", ">"), ("^", "^")],
    "<": [("v", ">")],
    ">": [("A", "^"), ("v", "<")],
    "A": [("^", "<"), (">", "v")],
}


def read_file(filename):
    with open(filename) as file:
        return [line.strip() for line in file]


# Find all shortest 'sequences' on the keypad from a start to end button.
# There can be multiple shortest sequences for any pair of start/end, as
# there are multiple pathways from start to end on any keypad.
#
# A priority queue ensures only the shortest paths are explored
# and captured/returned from the function.
def bfs_shortest_sequences(keypad, start, end) -> list[str]:
    queue = [(0, start, "")]
    visited = set()
    shortest_seqs = []

    while queue:
        cur_score, cur, cur_path = heapq.heappop(queue)

        if cur == end:
            shortest_seqs.append(cur_path + "A")
            continue

        visited.add(cur)

        # process neighbours
        for ncur, ndir in keypad[cur]:
            if (ncur) not in visited:
                nscore = cur_score + 1
                heapq.heappush(queue, (nscore, ncur, cur_path + ndir))

    return shortest_seqs


# Every sequence at level n maps to one or more seqs at level n-1 i.e. the layered
# sequences form a tree structure down to level 0 (the level of control that the human operates).
#
# This tree can be recursively processed to find the shortest possible sequence at level 0.
#
# By caching the results of this function, we can avoid recomputing sequences already processed,
# thus saving a lot of time (repeated calculations) in the recursion. It allow for much greater
# depths of tree (levels of control).
@cache
def dfs_shortest_seq(sequence, level_of_control, first_level=True):
    keypad = NUMERIC_KEYPAD if first_level else DIRECTIONAL_KEYPAD
    sequence = "A" + sequence # starting on new keypad so append A

    # Base case: if at level 0 (leaf of tree)
    if level_of_control == 0:
        return sum(
            min(len(seq) for seq in bfs_shortest_sequences(keypad, start, end))
            for start, end in pairwise(sequence)
        )

    # Reduce level_of_control and find shortest seqs for each pair recursively
    return sum(
        min(
            dfs_shortest_seq(seq, level_of_control - 1, False)
            for seq in bfs_shortest_sequences(keypad, start, end)
        )
        for start, end in pairwise(sequence)
    )


# Main
numeric_codes = read_file("day21.txt")

part_1_result = sum(dfs_shortest_seq(code, 2) * int(code[:3]) for code in numeric_codes)
print("part 1:", part_1_result)

part_2_result = sum(
    dfs_shortest_seq(code, 25) * int(code[:3]) for code in numeric_codes
)
print("part 2:", part_2_result)
