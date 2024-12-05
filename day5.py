from collections import defaultdict


def is_correctly_ordered(before_rules, index, nums_list) -> bool:
    # empty list of beyond end of list
    if len(nums_list) == 0 or index == len(nums_list):
        return True

    # for a non-zero index, check previous value is before current
    if index != 0:
        item = nums_list[index]
        prev_item = nums_list[index - 1]
        if prev_item not in before_rules[item]:
            return False

    # recurse and check the next position
    return is_correctly_ordered(before_rules, index + 1, nums_list)


if __name__ == "__main__":
    with open("day5_updates.txt") as file:
        updates = [list(map(int, line.rstrip().split(","))) for line in file]

    # inverted index for fast O(n) lookup
    before_rules = defaultdict(set)
    with open("day5_rules.txt") as file:
        for line in file:
            left, right = map(int, line.rstrip().split("|"))
            before_rules[right].add(left)

    total = sum(
        update[len(update) // 2]
        for update in updates
        if is_correctly_ordered(before_rules, 0, update)
    )

    print(total)
