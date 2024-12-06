from collections import defaultdict
from functools import cmp_to_key


def is_correctly_ordered(before_rules, index, nums_list) -> bool:
    # empty list or beyond end of list
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


def part_1(updates, before_rules):
    total = sum(
        update[len(update) // 2]
        for update in updates
        if is_correctly_ordered(before_rules, 0, update)
    )

    print("part 1", total)


def part_2(updates, before_rules):
    total = 0
    for update in updates:
        if not is_correctly_ordered(before_rules, 0, update):
            # sort update
            sorted_update = sorted(update, 
                key=cmp_to_key(lambda i1, i2: -1 if i1 in before_rules[i2] else 0 )
            )
            # add middle to total
            total += sorted_update[len(sorted_update) // 2]
    
    print("part 2", total)


def parse_input():
    with open("day5_updates.txt") as file:
        updates = [list(map(int, line.rstrip().split(","))) for line in file]

    # inverted index for fast O(1) lookup
    # represent a set of numbers that come BEFORE the keyed number
    before_rules = defaultdict(set)
    with open("day5_rules.txt") as file:
        for line in file:
            left, right = map(int, line.rstrip().split("|"))
            before_rules[right].add(left)

    return updates, before_rules

if __name__ == "__main__":
    updates, before_rules = parse_input()

    part_1(updates, before_rules)
    part_2(updates, before_rules)

