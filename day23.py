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


# part 1
groups = set()
for n1 in graph:
    for n2 in graph[n1]:
        common_neighbors = graph[n1].intersection(graph[n2])
        for c in common_neighbors:
            connected_group = frozenset((n1, n2, c))
            groups.add(connected_group)


groups_with_t = sum(any(node.startswith("t") for node in group) for group in groups)


print("part 1:", groups_with_t)
