from itertools import product
from collections import defaultdict
import re

ANTENNA_MATCH_REGEX = r"^[A-Z]+$|^[a-z]+$|^\d+$"


def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip()) for line in file]


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def delta(pos1: tuple[int, int], pos2: tuple[int, int], negate=False):
    delta_row, delta_col = -(pos1[0] - pos2[0]), -(pos1[1] - pos2[1])
    return (-delta_row, -delta_col) if negate else (delta_row, delta_col)


def transverse_line(pos: tuple[int, int], delta: tuple[int, int]):
    return pos[0] + delta[0], pos[1] + delta[1]


def part_1_find_antinodes(matrix, antenna_pos, prev_antennas) -> set[tuple[int, int]]:
    # calculate valid antinode positions based on relation to all previous antennas
    return {
        pos
        for prev in prev_antennas
        for pos in [
            transverse_line(prev, delta(antenna_pos, prev)),
            transverse_line(antenna_pos, delta(antenna_pos, prev, negate=True)),
        ]
        if not is_out_of_bounds(matrix, *pos)
    }


def part_2_find_antinodes(matrix, antenna_pos, prev_antennas) -> set[tuple[int, int]]:
    def antinodes_from(pos, dir_delta):
        while not is_out_of_bounds(matrix, *pos):
            yield pos
            pos = transverse_line(pos, dir_delta)

    antinodes = set()
    for prev in prev_antennas:
        # transverse from and including prev
        antinodes.update(antinodes_from(prev, delta(antenna_pos, prev)))
        # transverse from and including current
        antinodes.update(
            antinodes_from(antenna_pos, delta(antenna_pos, prev, negate=True))
        )

    return antinodes


def run(matrix, find_func):
    prev_antennas = defaultdict(set)  # for fast lookup
    antinodes = set()  # all possible antinode position

    for cur_row, cur_col in product(range(len(matrix)), range(len(matrix[0]))):
        cur_val = matrix[cur_row][cur_col]

        # find antinodes against previous antennas of same frequency
        if re.fullmatch(ANTENNA_MATCH_REGEX, cur_val):
            antinodes.update(
                find_func(matrix, (cur_row, cur_col), prev_antennas[cur_val])
            )
            prev_antennas[cur_val].add((cur_row, cur_col))

    print(f"{find_func.__name__}:", len(antinodes))


if __name__ == "__main__":
    matrix = read_file("day8.txt")
    run(matrix, part_1_find_antinodes)
    run(matrix, part_2_find_antinodes)
