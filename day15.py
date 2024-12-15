import re
from itertools import product
import copy

grid_pattern = re.compile(r"([#\.\@O]+(?:\n|$))")
movements_pattern = re.compile(r"([<>^v]+)")

directions = {"<": (0, -1), ">": (0, 1), "v": (1, 0), "^": (-1, 0)}


def parse_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()

    grid_match = grid_pattern.findall(content)
    movements_match = movements_pattern.findall(content)

    grid = [list(line.strip()) for line in grid_match if line.strip()]
    moves = list("".join(movements_match))

    return grid, moves


def find_robot(grid):
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "@":
            return r, c
    return -1, -1


def push_box(grid, box_r, box_c, move):
    delt_r, delt_c = directions[move]
    next_r, next_c = box_r + delt_r, box_c + delt_c

    if grid[next_r][next_c] == "O":
        push_box(grid, next_r, next_c, move)

    if grid[next_r][next_c] == ".":
        grid[next_r][next_c], grid[box_r][box_c] = grid[box_r][box_c], "."


def move_robot(grid, robot_r, robot_c, move):
    delt_r, delt_c = directions[move]
    next_r, next_c = robot_r + delt_r, robot_c + delt_c

    if grid[next_r][next_c] == "O":
        push_box(grid, next_r, next_c, move)

    if grid[next_r][next_c] == ".":
        grid[robot_r][robot_c], grid[next_r][next_c] = ".", "@"
        return next_r, next_c

    return robot_r, robot_c


def process_moves(grid, moves):
    grid = copy.deepcopy(grid)
    robot_r, robot_c = find_robot(grid)

    for move in moves:
        robot_r, robot_c = move_robot(grid, robot_r, robot_c, move)
    
    print("\n".join("".join(row) for row in grid))
    return grid


# Main
grid, moves = parse_file("day15_test.txt")
grid = process_moves(grid, moves)

total = sum(
    (100 * r + c)
    for r, c in product(range(len(grid)), range(len(grid[0])))
    if grid[r][c] == "O"
)

print("part_1:", total)
