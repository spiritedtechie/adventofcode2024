from itertools import product

def read_file(filename):
    with open(filename, "r") as f:
        patterns = f.readline().strip().split(", ")
        f.readline()
        designs = [line.strip() for line in f.readlines()]
        
    return patterns, designs


def ways_to_make_design(design, patterns):
    # Each position in the design and the number of ways to 'reach' it
    counts = [0] * (len(design) + 1)
    counts[0] = 1

    for i, pattern in product(range(1, len(design) + 1), patterns):
        if len(pattern) <= i and design[i - len(pattern) : i] == pattern:
            counts[i] += counts[i - len(pattern)]

    # ways to reach last position in design
    return counts[-1]


# Main
patterns, designs = read_file("day19.txt")

total = sum(1 for design in designs if ways_to_make_design(design, patterns))
print("part 1:", total)

total = sum(ways_to_make_design(design, patterns) for design in designs)
print("part 2:", total)
