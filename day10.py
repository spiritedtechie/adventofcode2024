from collections import deque
from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(map(int, line.strip())) for line in file]


# Directions for movement
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def paths_from_trailhead(matrix, th_row, th_col):
    rows, cols = len(matrix), len(matrix[0])

    # Function to BFS from trailhead to find valid path positions
    # Every valid path position stores a count of ways to reach that position
    def bfs(matrix, start_row, start_col) -> list:
        # Build up the number of ways to reach each position
        counts = [[0] * cols for _ in range(rows)]
        counts[start_row][start_col] = 1

        queue = deque([(start_row, start_col)])
        while queue:
            row, col = queue.popleft()

            for row_delta, col_delta in directions:
                n_row, n_col = row + row_delta, col + col_delta

                if is_out_of_bounds(matrix, n_row, n_col):
                    continue

                if matrix[n_row][n_col] == matrix[row][col] + 1:
                    # Not visited this position, so add to the queue to explore
                    if counts[n_row][n_col] == 0:
                        queue.append((n_row, n_col))

                    # Update no of ways to reach new position on path
                    counts[n_row][n_col] += counts[row][col]

        return counts

    # Get paths + position counts for tailhead
    path_counts = bfs(matrix, th_row, th_col)

    num_paths = sum(
        path_counts[i][j]
        for i, j in product(range(rows), range(cols))
        if matrix[i][j] == 9
    )
    reachable_nines = sum(
        1
        for i, j in product(range(rows), range(cols))
        if matrix[i][j] == 9 and path_counts[i][j] > 0
    )

    return num_paths, reachable_nines


def process_trail_heads(matrix, result_pos=0):
    rows, cols = len(matrix), len(matrix[0])
    return sum(
        paths_from_trailhead(matrix, th_row, th_col)[result_pos]
        for th_row, th_col in product(range(rows), range(cols))
        if matrix[th_row][th_col] == 0
    )


# Main
map_grid = read_file("day10.txt")

result = process_trail_heads(map_grid, result_pos=1)
print(f"part_1:", result)

result = process_trail_heads(map_grid)
print(f"part_2:", result)
