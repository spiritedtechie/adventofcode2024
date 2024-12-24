from collections import defaultdict


def read_file(filename):
    with open(filename, "r") as file:
        return [line.strip() for line in file]


def build_adj_matrix(network_map):
    adj_matrix = defaultdict(set)
    for line in network_map:
        node1, node2 = line.split("-")
        adj_matrix[node1].add(node2)
        adj_matrix[node2].add(node1)
    return adj_matrix


# part 1
def part_1(adj_matrix):
    groups = set()
    for n1 in adj_matrix:
        for n2 in adj_matrix[n1]:
            common_neighbors = adj_matrix[n1].intersection(adj_matrix[n2])
            for c in common_neighbors:
                groups.add(frozenset((n1, n2, c)))

    return sum(any(node.startswith("t") for node in group) for group in groups)


def part_2(adj_matrix):
    # initialise a lan group for each node
    lan_groups = set(frozenset([node]) for node in adj_matrix.keys())

    # Continue processing groups merging in other nodes until there is 1 group left
    while len(lan_groups) > 1:
        new_groups = set()

        for group in lan_groups:
            # find potentials nodes to add, not already part of group
            potentials = [node for node in adj_matrix if node not in group]

            # if potential connected with every existing members of group, merge it with the group
            # if none of potentials can merge with group, that group is effectively eliminated
            for pot in potentials:
                if all(pot in adj_matrix[node] for node in group):
                    new_groups.add(group | {pot})

        lan_groups = new_groups

    return ",".join(sorted(list(lan_groups)[0]))


# Main
network_map = read_file("day23.txt")
adj_matrix = build_adj_matrix(network_map)
print("part 1:", part_1(adj_matrix))
print("part 2:", part_2(adj_matrix))
