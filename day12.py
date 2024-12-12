from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def dfs(grid, r, c, visited):
    visited.add((r, c))
    area = 1
    perimeter = 0

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if is_out_of_bounds(grid, nr, nc) or grid[nr][nc] != grid[r][c]:
            perimeter += 1
        elif (nr, nc) not in visited:
            sub_area, sub_perimeter = dfs(grid, nr, nc, visited)
            area += sub_area
            perimeter += sub_perimeter

    return area, perimeter


def calculate_cost(grid):
    visited = set()
    total_cost = 0
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if (r, c) not in visited:
            area, perimeter = dfs(grid, r, c, visited)
            total_cost += area * perimeter

    return total_cost


# Main
grid = read_file("day12.txt")
result = calculate_cost(grid)
print("part_1:", result)
