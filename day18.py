import heapq

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def read_file(filename):
    with open(filename, "r") as f:
        return [
            (int(r), int(c))
            for c, r in (line.strip().split(",") for line in f.readlines())
        ]


def create_empty_grid(grid_size):
    return [["."] * grid_size for _ in range(grid_size)]


def grid_to_string(grid):
    return "\n".join("".join(row) for row in grid)


def is_out_of_bounds(grid, row, col):
    return not (0 <= row < len(grid) and 0 <= col < len(grid[0]))


def get_neighbours(grid, r, c):
    neighbours = []
    for dr, dc in DIRECTIONS:
        nr, nc = r + dr, c + dc
        if not is_out_of_bounds(grid, nr, nc) and grid[nr][nc] != "#":
            neighbours.append((nr, nc, 1))

    return neighbours


# Once again a priority queue keeps track of the lowest scoring
# path, and prioritises exploring that path. O(log n) for heap push and pop.
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


def part_1(grid, byte_coordinates, bytes_to_drop):
    start_coord = (0, 0)
    end_coord = (grid_size - 1, grid_size - 1)

    for r, c in byte_coordinates[:bytes_to_drop]:
        grid[r][c] = "#"

    result = walk_space(grid, start_coord, end_coord)
    print("part 1", result)


def part_2(grid, byte_coordinates):
    start_coord = (0, 0)
    end_coord = (grid_size - 1, grid_size - 1)

    # This is brute force, but is fast enough for the example
    # I may come back to this to improve it when I have time
    for r, c in byte_coordinates:
        grid[r][c] = "#"

        result = walk_space(grid, start_coord, end_coord)

        if result == -1:
            print("part 2:", (c, r))
            break


# Main
coordinates = read_file("day18.txt")

# Part 1
grid_size = 71
grid = create_empty_grid(grid_size)
part_1(grid, coordinates, 1024)

# part 2
grid_size = 71
grid = create_empty_grid(grid_size)
part_2(grid, coordinates)
