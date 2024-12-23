from collections import defaultdict


def read_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]


network_map = read_file("day23.txt")

graph = defaultdict(set)
for line in network_map:
    node1, node2 = line.split("-")
    graph[node1].add(node2)
    graph[node2].add(node1)


#  part 1
groups_with_t = 0
visited = set()
for n1 in graph:
    for n2 in graph[n1]:
        common_neighbors = graph[n1].intersection(graph[n2])

        for c in common_neighbors:
            connected_group = frozenset([n1, n2, c])

            # ignore essentially the same triple
            if connected_group in visited:
                continue
            visited.add(connected_group)

            if any(node.startswith("t") for node in connected_group):
                groups_with_t += 1


print("part 1:", groups_with_t)
