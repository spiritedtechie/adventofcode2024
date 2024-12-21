from itertools import product
from collections import deque
from collections import defaultdict


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def grid_to_string(grid):
    return "\n".join("".join(row) for row in grid)


def find_start(grid):
    start = None
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "S":
            start = r, c

    if not start:
        raise Exception("start or end not found")

    return start


def get_neighbours(grid, r, c):
    return [
        (r + dr, c + dc)
        for dr, dc in DIRECTIONS
        if 0 <= r + dr < len(grid) and 0 <= c + dc < len(grid[0])
    ]


# assumption is there is one path from start to end, as detailed in requirement
def walk_path(grid, start):
    visited = set()
    path_costs = defaultdict(lambda: 0)
    path_costs[start] = 0  # start position has zero cost
    queue = deque([(start, 0)])

    while queue:
        (curr_r, curr_c), curr_cost = queue.pop()

        if (curr_r, curr_c) in visited:
            continue
        visited.add((curr_r, curr_c))

        for nr, nc in get_neighbours(grid, curr_r, curr_c):
            if grid[nr][nc] in [".", "E"] and (nr, nc) not in visited:
                path_costs[(nr, nc)] = curr_cost + 1
                queue.appendleft(((nr, nc), curr_cost + 1))

    return path_costs


def find_cheats(grid, wall_positions, path_costs, minimum_cost_saving):
    savings = defaultdict(list)

    for r, c in wall_positions:
        # get wall neighbours that are on the path
        adj_path_positions = {
            (ad_r, ad_c)
            for ad_r, ad_c in get_neighbours(grid, r, c)
            if grid[ad_r][ad_c] in [".", "E", "S"]
        }

        # compare every path position adjacent to wall to see if it meet minimum cost saving
        for p1, p2 in product(adj_path_positions, adj_path_positions):
            if p1 != p2:
                p_cost_diff = path_costs[p1] - path_costs[p2] - 2
                if p_cost_diff >= minimum_cost_saving:
                    savings[p_cost_diff].append((r, c))

    return savings


# Main
grid = read_file("day20.txt")
start = find_start(grid)
path_costs = walk_path(grid, start)
wall_positions = {
    (r, c)
    for r, c in product(range(len(grid)), range(len(grid[0])))
    if grid[r][c] == "#"
}
cheats = find_cheats(grid, wall_positions, path_costs, minimum_cost_saving=100)

total_cheats = sum(len(cheat_positions) for saving, cheat_positions in cheats.items())
print("part 1:", total_cheats)
