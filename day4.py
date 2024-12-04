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

    # recursive call to match substring in same direction
    row, col = get_next_cell(row, col, direction)
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
    # approach is to form a left diagonal and right diagonal at each index of the matrix
    # and check that value of the diagonal matches one of these
    to_match = [["S", "A", "M"], ["M", "A", "S"]]

    def do_diagonals_at_coordinate_match(matrix, row, col):
        # get coordinates of the diagonals
        diag_right = [ get_next_cell(row, col, "up_right"), (row, col), get_next_cell(row, col, "down_left") ]
        diag_left = [ get_next_cell(row, col, "up_left"), (row, col), get_next_cell(row, col, "down_right") ]

        # skip if any diagonal coordinates are out of bounds
        if any(is_out_of_bounds(matrix, *coord) for coord in diag_right + diag_left):
            return False

        # map coordinates to actual values and check they match
        diag_right_vals = [matrix[row][col] for row,col in diag_right]
        diag_left_vals = [matrix[row][col] for row,col in diag_left]

        return diag_right_vals in to_match and diag_left_vals in to_match


    return sum(1 for row, col in product(range(len(matrix[0])), range(len(matrix)))
                if do_diagonals_at_coordinate_match(matrix, row, col))


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

    # smaller test matrix - expect output of 9
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
