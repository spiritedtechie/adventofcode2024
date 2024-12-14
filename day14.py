import re
from collections import defaultdict
import math

pattern = re.compile(r"p=([-]?\d+),([-]?\d+) v=([-]?\d+),([-]?\d+)")


def parse_file(filename):
    with open(filename, "r") as file:
        return [
            [int(match[1]), int(match[0]), int(match[3]), int(match[2])]
            for line in file
            for match in pattern.findall(line)
        ]


def move_robots(iterations=1):
    quadrant_totals = defaultdict(int)
    for pos_r, pos_c, vel_r, vel_c in robots:
        new_r = (pos_r + vel_r * iterations) % grid_depth
        new_col = (pos_c + vel_c * iterations) % grid_width

        if new_r != mid_row and new_col != mid_col:
            quadrant = (new_r >= mid_row) * 2 + (new_col >= mid_col)
            quadrant_totals[quadrant] += 1

    return quadrant_totals


# robots = parse_file("day14_test.txt")
# grid_depth, grid_width = 7, 11

robots = parse_file("day14.txt")
grid_depth, grid_width = 103, 101
mid_row, mid_col = grid_depth // 2, grid_width // 2
number_second = 100

quadrant_totals = move_robots(number_second)
safety_factor = math.prod(quadrant_totals.values(), start=1)
print("part_1:", safety_factor)

