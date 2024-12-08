from itertools import product
from collections import defaultdict
import re

ANTENNA_MATCH_REGEX = r"^[A-Z]+$|^[a-z]+$|^\d+$"


def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip()) for line in file]


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def part_1_find_antinodes(
    matrix, cur_row, cur_col, previous_antennas
) -> set[tuple[int, int]]:
    # calculate valid antinode positions based on relation to all previous antennas
    antinodes = set()

    for prev_row, prev_col in previous_antennas:
        delta_row, delta_col = -(cur_row - prev_row), -(cur_col - prev_col)

        # possible antinode positions in both directions
        anti_pos_1 = (prev_row + delta_row, prev_col + delta_col)
        anti_pos_2 = (cur_row - delta_row, cur_col - delta_col)

        if not is_out_of_bounds(matrix, *anti_pos_1):
            antinodes.add(anti_pos_1)

        if not is_out_of_bounds(matrix, *anti_pos_2):
            antinodes.add(anti_pos_2)

    return antinodes


def part_2_find_antinodes(
    matrix, cur_row, cur_col, previous_antennas
) -> set[tuple[int, int]]:
    # calculate valid antinode positions based on relation to all previous antennas
    antinodes = set()

    for prev_row, prev_col in previous_antennas:
        # Antennas themselves are antinodes
        antinodes.add((prev_row, prev_col))
        antinodes.add((cur_row, cur_col))

        delta_row, delta_col = -(cur_row - prev_row), -(cur_col - prev_col)

        # Loop deltas forward along the line from prev to current
        anti_row, anti_col = prev_row + delta_row, prev_col + delta_col
        while not is_out_of_bounds(matrix, anti_row, anti_col):
            antinodes.add((anti_row, anti_col))
            anti_row, anti_col = anti_row + delta_row, anti_col + delta_col

        # Loop deltas forward along the line from curr to previous
        anti_row, anti_col = cur_row - delta_row, cur_col - delta_col
        while not is_out_of_bounds(matrix, anti_row, anti_col):
            antinodes.add((anti_row, anti_col))
            anti_row, anti_col = anti_row - delta_row, anti_col - delta_col

    return antinodes


def run(matrix, find_func):
    prev_antennas = defaultdict(set)  # for fast lookup
    antinodes = set()  # all possible antinode position

    for cur_row, cur_col in product(range(len(matrix)), range(len(matrix[0]))):
        cur_val = matrix[cur_row][cur_col]

        # find antinodes against previous antennas of same frequency
        if re.fullmatch(ANTENNA_MATCH_REGEX, cur_val):
            antinodes.update(
                find_func(matrix, cur_row, cur_col, prev_antennas[cur_val])
            )
            prev_antennas[cur_val].add((cur_row, cur_col))

    print(f"{find_func.__name__}:", len(antinodes))


if __name__ == "__main__":
    matrix = read_file("day8.txt")
    run(matrix, part_1_find_antinodes)
    run(matrix, part_2_find_antinodes)
