import heapq


def read_file(filename):
    coordinates = []
    with open(filename, "r") as f:
        for line in f.readlines():
            c, r = line.strip().split(",")
            coordinates.append((int(r), int(c)))
    return coordinates


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def grid_to_string(grid):
    return "\n".join("".join(row) for row in grid)


def is_out_of_bounds(matrix, row, col):
    return not (0 <= row < len(matrix) and 0 <= col < len(matrix[0]))


def get_neighbours(grid, r, c):
    neighbours = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if not is_out_of_bounds(grid, nr, nc) and grid[nr][nc] != "#":
            neighbours.append((nr, nc, 1))

    return neighbours


def walk_space(grid, start_position, end_position):
    start_r, start_c = start_position
    end_r, end_c = end_position

    queue = []
    heapq.heappush(queue, (0, start_r, start_c))
    visited = set()

    while queue:
        # The head position of the lowest score path so far
        score, r, c = heapq.heappop(queue)

        # To ensure we don't loop back round infinitely on the graph
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Reached the end
        if (r, c) == (end_r, end_c):
            return score

        # Otherwise, explore neighbours
        for nr, nc, move_cost in get_neighbours(grid, r, c):
            n_score = score + move_cost
            heapq.heappush(queue, (n_score, nr, nc))

    return -1


# Main
coordinates = read_file("day18.txt")

grid_size = 71
grid = [["."] * grid_size for _ in range(grid_size)]

to_drop = 1024
for r, c in coordinates[:to_drop]:
    grid[r][c] = "#"

start_coord = (0, 0)
end_coord = (grid_size - 1, grid_size - 1)

result = walk_space(grid, start_coord, end_coord)
print("part 1", result)
