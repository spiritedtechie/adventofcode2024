from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(line.rstrip()) for line in file]


direction_deltas = {"<": (0, -1), "^": (-1, 0), ">": (0, +1), "V": (+1, 0)}
next_direction = {"<": "^", "^": ">", ">": "V", "V": "<"}


def find_starting_position(matrix):
    for row, col in product(range(len(matrix)), range(len(matrix[0]))):
        if matrix[row][col] in direction_deltas.keys():
            return (row, col), matrix[row][col]
    return None, None


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def find_way_out_of_grid(
    matrix,
    start_pos: tuple[int, int],
    start_direction,
    obstructions: set[tuple[int, int]] = set(),
) -> tuple[bool, set]:
    
    visited_directional_positions, visited_positions = set(), set()
    stack = [(start_pos, start_direction)]
    
    while stack:
        cur_pos, cur_direction = stack.pop()

        # exited grid
        if is_out_of_bounds(matrix, *cur_pos):
            return True, visited_positions

        # repeating visit to directional position so ignore
        if (*cur_pos, cur_direction) in visited_directional_positions:
            continue

        visited_directional_positions.add((*cur_pos, cur_direction))
        visited_positions.add(cur_pos)

        # proposed next pos
        cur_row, cur_col = cur_pos
        delta_row, delta_col = direction_deltas[cur_direction]
        next_row, next_col = cur_row + delta_row, cur_col + delta_col

        if not is_out_of_bounds(matrix, next_row, next_col) and (
            matrix[next_row][next_col] == "#" or (next_row, next_col) in obstructions
        ):
            # if proposed next position in same direction is a blocker, change direction
            stack.append(((cur_row, cur_col), next_direction[cur_direction]))

        else:
            # else move to it
            stack.append(((next_row, next_col), cur_direction))

    return False, visited_positions


def part_1():
    starting_pos, starting_dir = find_starting_position(matrix)
    _, visited_pos = find_way_out_of_grid(matrix, starting_pos, starting_dir)
    print("part 1:", len(visited_pos))


def part_2():
    starting_pos, starting_dir = find_starting_position(matrix)
    _, visited_pos = find_way_out_of_grid(matrix, starting_pos, starting_dir)  # get successful path

    # try obstruct every visited position on successful path and see if it prevents leaving
    obstruction_successful_count = sum(
        not find_way_out_of_grid(matrix, starting_pos, starting_dir, {pos})[0]
        for pos in visited_pos
    )

    print("part 2:", obstruction_successful_count)


if __name__ == "__main__":
    matrix = read_file("day6.txt")

    part_1()
    part_2()
