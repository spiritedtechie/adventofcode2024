import heapq
from collections import defaultdict

DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "V": (1, 0), "<": (0, -1)}


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def get_neighbours(grid, r, c, direction):
    neighbours = []

    dir_list = list(DIRECTIONS)
    same_dir = direction
    clockwise_dir = dir_list[(dir_list.index(direction) + 1) % 4]
    anticlockwise_dir = dir_list[(dir_list.index(direction) - 1) % 4]

    to_process = [(same_dir, 1), (clockwise_dir, 1001), (anticlockwise_dir, 1001)]

    for dir, cost in to_process:
        dr, dc = DIRECTIONS[dir]
        nr, nc = r + dr, c + dc
        if grid[nr][nc] != "#":
            neighbours.append((nr, nc, dir, cost))

    return neighbours


# The priority queue is key to ensuring this function always
# explores the lowest cost path as priority on each iteration
# and ultimately returns the lowest score possible to get to end of maze
def walk_maze(grid, start_position, end_position):
    start_r, start_c = start_position
    end_r, end_c = end_position
    viable_paths = defaultdict(list)

    queue = []
    heapq.heappush(queue, (0, start_r, start_c, ">", [(start_r, start_c)]))
    visited = set()

    while queue:
        # The head position of the lowest score path so far
        score, r, c, dir, path = heapq.heappop(queue)

        visited.add((r, c, dir))

        # Reached the end
        if (r, c) == (end_r, end_c):
            viable_paths[score].append(path)

        # Otherwise, explore neighbours
        for nr, nc, ndir, move_cost in get_neighbours(grid, r, c, dir):
            n_score = score + move_cost
            if (nr, nc, ndir) not in visited:
                heapq.heappush(queue, (n_score, nr, nc, ndir, path + [(nr, nc)]))

    return viable_paths


# Main
grid = read_file("day16.txt")

# start and end
start_r, start_c = len(grid) - 2, 1
end_r, end_c = 1, len(grid[0]) - 2

viable_paths = walk_maze(grid, (start_r, start_c), (end_r, end_c))

lowest_cost = list(viable_paths.keys())[0]
print("part_1:", lowest_cost)

tiles_on_best_paths = set()
for path in viable_paths[lowest_cost]:
    tiles_on_best_paths.update(path)

print("part_2:", len(tiles_on_best_paths))
