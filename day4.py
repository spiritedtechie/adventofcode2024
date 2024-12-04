from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip()) for line in file]


adjacent_deltas = {
    "up_left": (-1, -1),
    "up_right": (-1, +1),
    "up": (-1, 0),
    "down_left": (+1, -1),
    "down_right": (+1, +1),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def get_next_cell(row, col, direction):
    delta_row, delta_col = adjacent_deltas[direction]
    return row + delta_row, col + delta_col


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def matches_text(matrix, row, col, text, direction):
    if not text:
        return True

    if is_out_of_bounds(matrix, row, col) or matrix[row][col] != text[0]:
        return False

    row, col = get_next_cell(row, col, direction)

    # recursive call to match substring in same direction
    return matches_text(matrix, row, col, text[1:], direction)


def part1_count_matches(matrix, text):
    matrix_depth, matrix_width = len(matrix[0]), len(matrix)

    count = 0
    for row, col in product(range(matrix_depth), range(matrix_width)):
        count += sum(1 for direction in adjacent_deltas
            if matches_text(matrix, row, col, text, direction)
        )

    return count


def part2_count_matches(matrix):
    # going to for a left diagonal and right diagonal for each position in matrix
    # and check that it matches these 
    to_match_1 = ['S', 'A', 'M']
    to_match_2 = ['M', 'A', 'S']

    matrix_depth, matrix_width = len(matrix[0]), len(matrix)

    count = 0
    for mid_row, mid_col in product(range(matrix_depth), range(matrix_width)):
        # get diagonal cell positions around middle cell
        up_left_row,  up_left_col = get_next_cell(mid_row, mid_col, "up_left")
        down_right_row, down_right_col = get_next_cell(mid_row, mid_col, "down_right")
        up_right_row,  up_right_col = get_next_cell(mid_row, mid_col, "up_right")
        down_left_row, down_left_col = get_next_cell(mid_row, mid_col, "down_left")

        # if part of diagonal out of bounds, continue
        if is_out_of_bounds(matrix, up_left_row, up_left_col) or \
            is_out_of_bounds(matrix, down_right_row, down_right_col) or\
            is_out_of_bounds(matrix, up_right_row, up_right_col) or \
            is_out_of_bounds(matrix, down_left_row, down_left_col):
            continue

        x_left_slant = [matrix[up_left_row][up_left_col], matrix[mid_row][mid_col], matrix[down_right_row][down_right_col]]
        y_left_slant = [matrix[down_left_row][down_left_col], matrix[mid_row][mid_col], matrix[up_right_row][up_right_col]]

        if (x_left_slant == to_match_1 or x_left_slant == to_match_2) and (y_left_slant == to_match_1 or y_left_slant == to_match_2):
            count += 1

    return count


if __name__ == "__main__":
    matrix = read_file("day4.txt")

    # # smaller test matrix - expect output of 18
    # matrix = [
    #     ['M', 'M', 'M', 'S', 'X', 'X', 'M', 'A', 'S', 'M'],
    #     ['M', 'S', 'A', 'M', 'X', 'M', 'S', 'M', 'S', 'A'],
    #     ['A', 'M', 'X', 'S', 'X', 'M', 'A', 'A', 'M', 'M'],
    #     ['M', 'S', 'A', 'M', 'A', 'S', 'M', 'S', 'M', 'X'],
    #     ['X', 'M', 'A', 'S', 'A', 'M', 'X', 'A', 'M', 'M'],
    #     ['X', 'X', 'A', 'M', 'M', 'X', 'X', 'A', 'M', 'A'],
    #     ['S', 'M', 'S', 'M', 'S', 'A', 'S', 'X', 'S', 'S'],
    #     ['S', 'A', 'X', 'A', 'M', 'A', 'S', 'A', 'A', 'A'],
    #     ['M', 'A', 'M', 'M', 'M', 'X', 'M', 'M', 'M', 'M'],
    #     ['M', 'X', 'M', 'X', 'A', 'X', 'M', 'A', 'S', 'X']
    # ]

    print(part1_count_matches(matrix, "XMAS"))

    # # smaller test matrix - expect output of 18
    # matrix = [
    #     ['.', 'M', '.', 'S', '.', '.', '.', '.', '.', '.'],
    #     ['.', '.', 'A', '.', '.', 'M', 'S', 'M', 'S', '.'],
    #     ['.', 'M', '.', 'S', '.', 'M', 'A', 'A', '.', '.'],
    #     ['.', '.', 'A', '.', 'A', 'S', 'M', 'S', 'M', '.'],
    #     ['.', 'M', '.', 'S', '.', 'M', '.', '.', '.', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.'],
    #     ['S', '.', 'S', '.', 'S', '.', 'S', '.', 'S', '.'],
    #     ['.', 'A', '.', 'A', '.', 'A', '.', 'A', '.', '.'],
    #     ['M', '.', 'M', '.', 'M', '.', 'M', '.', 'M', '.'],
    #     ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.']
    # ]
    print(part2_count_matches(matrix))
