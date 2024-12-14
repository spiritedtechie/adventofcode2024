import re
from collections import defaultdict
import math

pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


def parse_file(filename):
    with open(filename, "r") as file:
        return [
            [int(match[1]), int(match[0]), int(match[3]), int(match[2])]
            for line in file
            for match in pattern.findall(line)
        ]


def move_robots(grid_depth, grid_width, robots, iterations=1):
    # use the modulus operator to keep iterated new positions within grid bounds
    return [
        (
            (pos_r + vel_r * iterations) % grid_depth,
            (pos_c + vel_c * iterations) % grid_width,
            vel_r,
            vel_c,
        )
        for pos_r, pos_c, vel_r, vel_c in robots
    ]


def find_safety_factor(grid_depth, grid_width, robots):
    mid_row, mid_col = grid_depth // 2, grid_width // 2

    quadrant_totals = defaultdict(int)
    for r, c, _, _ in robots:
        if r != mid_row and c != mid_col:
            quadrant_number = (r >= mid_row) * 2 + (c >= mid_col)
            quadrant_totals[quadrant_number] += 1

    return math.prod(quadrant_totals.values(), start=1)


def plot_on_grid(grid_depth, grid_width, robots):
    grid = [["."] * grid_width for _ in range(grid_depth)]

    for pos_r, pos_c, _, _ in robots:
        grid[pos_r][pos_c] = "X"

    return grid


def grid_to_string(grid):
    return "\n".join("".join(row) for row in grid)


def part_1(grid_depth, grid_width, robots):
    new_robots = move_robots(grid_depth, grid_width, robots, iterations=100)
    print("part_1:", find_safety_factor(grid_depth, grid_width, new_robots))


# output to a file, then manually grep the file for some XXXXX patterns
# to find the iteration number with the xmas tree pattern!
def part_2(grid_depth, grid_width, robots):
    with open("tmp/day_14_part_2_output.txt", "w") as file:
        for i in range(1, 10000):
            file.write(f"Iteration {i}\n")

            robots = move_robots(grid_depth, grid_width, robots, iterations=1)
            grid = plot_on_grid(grid_depth, grid_width, robots)

            file.write(grid_to_string(grid))
            file.write("\n")


# Main
robots = parse_file("day14.txt")
grid_depth, grid_width = 103, 101

part_1(grid_depth, grid_width, robots)
part_2(grid_depth, grid_width, robots)
