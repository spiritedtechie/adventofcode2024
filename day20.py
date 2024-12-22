from itertools import product
from collections import deque
from collections import defaultdict


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def grid_to_string(grid) -> str:
    return "\n".join("".join(row) for row in grid)


def manhattan_distance(from_pos: tuple[int, int], to_pos: tuple[int, int]) -> int:
    return abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1])


def find_start(grid) -> tuple[int, int]:
    for r, c in product(range(len(grid)), range(len(grid[0]))):
        if grid[r][c] == "S":
            return r, c
    raise ValueError("start position not found")


# Valid neighbours of a cell that are not out of bounds
def get_neighbours(grid, r, c) -> list[tuple[int, int]]:
    return [
        (r + dr, c + dc)
        for dr, dc in DIRECTIONS
        if 0 <= r + dr < len(grid) and 0 <= c + dc < len(grid[0])
    ]


# Find the path by walking it.
# Assumption is there is one path from start to end (as detailed in requirement).
# This simplifies the walking of it i.e. no need to find the shortest path.
def walk_path(grid, start) -> list[tuple[int, int]]:
    ordered_path = [start]
    queue = deque([start])
    visited = set([start])

    while queue:
        curr_r, curr_c = queue.pop()

        for nr, nc in get_neighbours(grid, curr_r, curr_c):
            if grid[nr][nc] in [".", "E"] and (nr, nc) not in visited:
                visited.add((curr_r, curr_c))
                ordered_path.append((nr, nc))
                queue.appendleft((nr, nc))

    return ordered_path


def find_cheats(path, minimum_cost_saving=100, max_cheat_length=2):
    savings = defaultdict(int)

    # for each position on the path i.e. where we can start cheating from
    for start_pos_idx, start_pos in enumerate(path):
        # no point exploring path beyond the required saving
        if len(path) - start_pos_idx <= minimum_cost_saving:
            break

        # compare with other points on path that we can cheat to
        # that give minimum required cost saving
        for end_pos_idx in range(start_pos_idx + minimum_cost_saving, len(path)):
            end_pos = path[end_pos_idx]
            distance = manhattan_distance(start_pos, end_pos)

            # ensure the cheat length and minimum saving are met
            if distance <= max_cheat_length:
                saving = end_pos_idx - start_pos_idx - distance
                if saving >= minimum_cost_saving:
                    savings[saving] += 1

    return savings


# Main
grid = read_file("day20.txt")
start = find_start(grid)
path = walk_path(grid, start)

# part 1
savings = find_cheats(path, max_cheat_length=2)
total_cheats = sum(savings.values())
print("part 1:", total_cheats)

# part 2
savings = find_cheats(path, max_cheat_length=20)
total_cheats = sum(savings.values())
print("part 2:", total_cheats)
