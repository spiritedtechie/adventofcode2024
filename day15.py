import re
from itertools import product
import copy
from collections import deque


GRID_PATTERN = re.compile(r"([#\.\@O]+(?:\n|$))")
MOVEMENTS_PATTERN = re.compile(r"([<>^v]+)")

DIRECTIONS = {"<": (0, -1), ">": (0, 1), "v": (1, 0), "^": (-1, 0)}
GRID_EXTENSIONS = {"#": ["#", "#"], ".": [".", "."], "@": ["@", "."], "O": ["[", "]"]}


def parse_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    grid_match = GRID_PATTERN.findall(content)
    movements_match = MOVEMENTS_PATTERN.findall(content)

    grid = [list(line.strip()) for line in grid_match if line.strip()]
    moves = list("".join(movements_match))

    return grid, moves


def widen_grid(grid):
    return [
        [new_val for old_val in row for new_val in GRID_EXTENSIONS[old_val]]
        for row in grid
    ]


def find_robot(grid):
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "@":
            return r, c
    return -1, -1


def get_box(grid, r, c):
    val = grid[r][c]
    if val == "O":
        return (r, c, c)
    elif val == "[":
        return (r, c, c + 1)
    elif val == "]":
        return (r, c - 1, c)
    return None


# Breadth-first transversal of connected box chain/tree
def get_moveable_box_chain(grid, box, delta_r, delta_c):
    box_chain = set([box])
    queue = deque([box])

    while len(queue):
        br, bc1, bc2 = queue.pop()
        for bc in range(bc1, bc2 + 1):
            nr, nc = br + delta_r, bc + delta_c

            # if blocker adjacent to box, this chain cannot be moved
            if grid[nr][nc] in ("#"):
                return None

            next_box = get_box(grid, nr, nc)
            if next_box and next_box not in box_chain:
                box_chain.add(next_box)
                queue.appendleft(next_box)

    return box_chain


def try_push_box(grid, box, delta_r, delta_c):
    boxes = get_moveable_box_chain(grid, box, delta_r, delta_c)
    if not boxes:
        return

    transforms = []
    visited = set()

    # put each box in new location
    for br, bc1, bc2 in boxes:
        transforms.append((br + delta_r, bc1 + delta_c, grid[br][bc1]))
        transforms.append((br + delta_r, bc2 + delta_c, grid[br][bc2]))
        visited.update([(br + delta_r, bc1 + delta_c), (br + delta_r, bc2 + delta_c)])

    # mark new empty space where boxes used to be
    for br, bc1, bc2 in boxes:
        for bc in range(bc1, bc2 + 1):
            if (br, bc) not in visited:
                transforms.append((br, bc, "."))

    # apply above transformations to grid
    for r, bc, new_val in transforms:
        grid[r][bc] = new_val


def move_robot(grid, robot_r, robot_c, move):
    delta_r, delta_c = DIRECTIONS[move]
    next_r, next_c = robot_r + delta_r, robot_c + delta_c

    # try push box(es), if the cell in direction of move is a box
    box = get_box(grid, next_r, next_c)
    if box:
        try_push_box(grid, box, delta_r, delta_c)

    # (now) if free space, move to it
    if grid[next_r][next_c] == ".":
        grid[robot_r][robot_c], grid[next_r][next_c] = ".", "@"
        return next_r, next_c

    return robot_r, robot_c


def process_moves(grid, moves):
    grid = copy.deepcopy(grid)

    robot_r, robot_c = find_robot(grid)
    for move in moves:
        robot_r, robot_c = move_robot(grid, robot_r, robot_c, move)

    return grid


def calculate_gps_sum(grid):
    return sum(
        (100 * r + c)
        for r, c in product(range(len(grid)), range(len(grid[0])))
        if grid[r][c] in ["O", "["]
    )


# Main
# Part 1
grid, moves = parse_file("day15.txt")
grid_after = process_moves(grid, moves)
print("part_1:", calculate_gps_sum(grid_after))

#  Part 2
grid = widen_grid(grid)
grid_after = process_moves(grid, moves)
print("part_2:", calculate_gps_sum(grid_after))
