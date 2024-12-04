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
    "right": (0, +1)
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


def count_matches(matrix, text):
    matrix_depth, matrix_width = len(matrix[0]), len(matrix)

    count = 0
    for row, col in product(range(matrix_depth), range(matrix_width)):
        count += sum(1 for direction in adjacent_deltas if matches_text(matrix, row, col, text, direction))

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

    print(count_matches(matrix, "XMAS"))