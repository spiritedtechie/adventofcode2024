from collections import deque
from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(map(int, line.strip())) for line in file]


# Directions for movement
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def bfs(matrix, start_row, start_col):
    rows, cols = len(matrix), len(matrix[0])

    # Store the number of ways to reach each cell
    counts = [[0] * cols for _ in range(rows)]
    counts[start_row][start_col] = 1

    queue = deque([(start_row, start_col)])
    while queue:
        row, col = queue.popleft()

        for dr, dc in directions:
            n_row, n_col = row + dr, col + dc

            if is_out_of_bounds(matrix, n_row, n_col):
                continue

            if matrix[n_row][n_col] == matrix[row][col] + 1:
                # Not visited this cell, so add to the queue
                if counts[n_row][n_col] == 0:
                    queue.append((n_row, n_col))

                # Number of ways to reach new position on path
                counts[n_row][n_col] += counts[row][col]

    # Count 9s and number of ways to reach them for this tail head
    num_paths = sum(
        counts[i][j] for i, j in product(range(rows), range(cols)) if matrix[i][j] == 9
    )
    reachable_nines = sum(
        1
        for i, j in product(range(rows), range(cols))
        if matrix[i][j] == 9 and counts[i][j] > 0
    )

    return num_paths, reachable_nines


def run(matrix, result_pos=0):
    return sum(
        bfs(matrix, row, col)[result_pos]
        for row, col in product(range(len(matrix)), range(len(matrix[0])))
        if matrix[row][col] == 0
    )


# map_grid = [
#     [8, 9, 0, 1, 0, 1, 2, 3],
#     [7, 8, 1, 2, 1, 8, 7, 4],
#     [8, 7, 4, 3, 0, 9, 6, 5],
#     [9, 6, 5, 4, 9, 8, 7, 4],
#     [4, 5, 6, 7, 8, 9, 0, 3],
#     [3, 2, 0, 1, 9, 0, 1, 2],
#     [0, 1, 3, 2, 9, 8, 0, 1],
#     [1, 0, 4, 5, 6, 7, 3, 2],
# ]

map_grid = read_file("day10.txt")

result = run(map_grid, result_pos=1)
print(f"part_1:", result)

result = run(map_grid)
print(f"part_2:", result)
