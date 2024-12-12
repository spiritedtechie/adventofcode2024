from itertools import product


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def is_out_of_bounds(grid, row, col):
    return not (0 <= row < len(grid) and 0 <= col < len(grid[0]))


def get_corners(grid, r, c):
    val = grid[r][c]

    def check_position(r, c):
        return is_out_of_bounds(grid, r, c) or grid[r][c] != val

    add_corner_rules = [
        lambda r, c: check_position(r - 1, c) and check_position(r, c - 1), # top left corner
        lambda r, c: check_position(r - 1, c) and check_position(r, c + 1), # top right corner
        lambda r, c: check_position(r, c - 1) and check_position(r + 1, c), # bottom right corner
        lambda r, c: check_position(r + 1, c) and check_position(r, c + 1), # bottom left corner
        lambda r, c: r > 0 and c > 0 and grid[r - 1][c - 1] != val and grid[r][c - 1] == val and grid[r - 1][c] == val, # top left L shape
        lambda r, c: r > 0 and c < len(grid[0]) - 1 and grid[r - 1][c + 1] != val and grid[r - 1][c] == val and grid[r][c + 1] == val, # top right L shape
        lambda r, c: r < len(grid) - 1 and c > 0 and grid[r + 1][c - 1] != val and grid[r][c - 1] == val and grid[r + 1][c] == val, # bottom left L shape
        lambda r, c: r < len(grid) - 1 and c < len(grid[0]) - 1 and grid[r + 1][c + 1] != val and grid[r][c + 1] == val and grid[r + 1][c] == val # bottom right L shape
    ]
    
    return sum(1 for rule in add_corner_rules if rule(r, c))


def dfs(grid, r, c, visited):
    visited.add((r, c))
    area = 1
    perimeter = 0
    corners = get_corners(grid, r, c)

    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if is_out_of_bounds(grid, nr, nc) or grid[nr][nc] != grid[r][c]:
            perimeter += 1
        elif (nr, nc) not in visited:
            sub_area, sub_perimeter, sub_corners = dfs(grid, nr, nc, visited)
            area += sub_area
            perimeter += sub_perimeter
            corners += sub_corners

    return area, perimeter, corners


def calculate(grid, calc_perimeter=True):
    visited = set()
    total_cost = 0
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if (r, c) not in visited:
            area, perimeter, corners = dfs(grid, r, c, visited)
            total_cost += area * perimeter if calc_perimeter else area * corners

    return total_cost


# Main
grid = read_file("day12.txt")

result = calculate(grid)
print("part_1:", result)

result = calculate(grid, calc_perimeter=False)
print("part_2:", result)
