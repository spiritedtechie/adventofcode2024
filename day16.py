import heapq


DIRECTIONS = {"^": (-1, 0), ">": (0, 1), "V": (1, 0), "<": (0, -1)}


def read_file(filename):
    with open(filename) as file:
        return [list(line.strip()) for line in file]


def get_neighbours(grid, r, c, direction):
    neighbours = []

    # same direction
    dr, dc = DIRECTIONS[direction]
    nr, nc = r + dr, c + dc
    if grid[nr][nc] != "#":
        neighbours.append((nr, nc, direction, 1))

    # rotations (clockwise and counter)
    dir_list = list(DIRECTIONS)
    new_dir = dir_list[(dir_list.index(direction) + 1) % 4]
    neighbours.append((r, c, new_dir, 1000))
    new_dir = dir_list[(dir_list.index(direction) - 1) % 4]
    neighbours.append((r, c, new_dir, 1000))

    return neighbours

# The priority queue is key to ensuring this function always
# explores the lowest cost path as priority on each iteration 
# and ultimately returns the lowest score possible to get to end of maze
def walk_maze(grid, start_position, end_position):
    start_r, start_c = start_position
    end_r, end_c = end_position

    queue = []
    heapq.heappush(queue, (0, start_r, start_c, ">"))

    visited = set()

    while queue:
        # The head position of the lowest score path so far
        score, r, c, direction = heapq.heappop(queue)

        # Skip if aleady visited
        if (r, c, direction) in visited:
            continue
        visited.add((r, c, direction))

        # Reached the end
        if (r, c) == (end_r, end_c):
            return score

        # Otherwise, explore neighbours
        for nr, nc, ndir, move_cost in get_neighbours(grid, r, c, direction):
            n_score = score + move_cost
            if (nr, nc, ndir) not in visited:
                heapq.heappush(queue, (n_score, nr, nc, ndir))

    return -1


# Main
grid = read_file("day16.txt")

start_r, start_c = len(grid) - 2, 1
end_r, end_c = 1, len(grid[0]) - 2

result = walk_maze(grid, (start_r, start_c), (end_r, end_c))
print("part_1:", result)
