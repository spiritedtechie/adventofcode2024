from itertools import product
import sys

sys.setrecursionlimit(10000)


def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip()) for line in file]


direction_deltas = {"<": (0, -1), "^": (-1, 0), ">": (0, +1), "V": (+1, 0)}
next_direction = {"<": "^", "^": ">", ">": "V", "V": "<"}


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def rec(matrix, visited, cur_pos, cur_direction):

    if is_out_of_bounds(matrix, *cur_pos):
        return

    visited.add(cur_pos)

    # figure out next pos
    cur_row, cur_col = cur_pos
    delta_row, delta_col = direction_deltas[cur_direction]
    next_row, next_col = cur_row + delta_row, cur_col + delta_col

    if not is_out_of_bounds(matrix, next_row, next_col) and matrix[next_row][next_col] == "#":
        # change direction and repeat
        new_direction = next_direction[cur_direction]
        return rec(matrix, visited, (cur_row, cur_col), new_direction)
    else:
        # repeat for next position in same direction
        return rec(matrix, visited, (next_row, next_col), cur_direction)


if __name__ == "__main__":
    matrix = read_file("day6.txt")

    starting_pos, starting_dir = None, None
    for row, col in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[row][col] in direction_deltas.keys():
            starting_dir = matrix[row][col]
            starting_pos = (row, col)

    visited = set()
    rec(matrix, visited, starting_pos, starting_dir)
    print("part 1:", len(visited))
