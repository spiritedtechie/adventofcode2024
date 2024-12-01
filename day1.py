from collections import Counter

def read_file_to_lists(filename):
    list1, list2 = [], []
    # O(n)
    with open(filename) as file:
        for line in file:
            tokens = line.strip().split(" ")
            list1.append(int(tokens[0]))
            list2.append(int(tokens[3]))
    return list1, list2


def part1_distance(list1, list2):
    return sum(abs(a - b) for a, b in zip(sorted(list1), sorted(list2)))

def part2_similarity_score(list1, list2):
    list2_counts = Counter(list2)
    return sum(item * list2_counts[item] for item in list1)
    

if __name__ == "__main__":
    list1, list2 = read_file_to_lists("day1.txt")
    print(part1_distance(list1, list2))
    print(part2_similarity_score(list1, list2))
