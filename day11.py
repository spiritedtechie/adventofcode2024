from collections import Counter


# using a Counter i.e. dict is constant time insertions
# versus appending to a new list. Plus repeat stones
# are only stored once so more space efficient too
def blink(stones_count):
    new_stones_count = Counter()

    for stone, count in stones_count.items():
        stone_str = str(stone)

        if stone == 0:
            new_stones_count[1] += count
        elif len(stone_str) % 2 == 0:
            mid = len(stone_str) // 2
            left = int(stone_str[:mid])
            right = int(stone_str[mid:])
            new_stones_count[left] += count
            new_stones_count[right] += count
        else:
            new_stones_count[stone * 2024] += count

    return new_stones_count


def run_blinks(initial_stones, num_blinks):
    stones_count = Counter(initial_stones)

    for _ in range(num_blinks):
        stones_count = blink(stones_count)

    return sum(stones_count.values())


# initial_stones = [125, 17]
initial_stones = [0, 44, 175060, 3442, 593, 54398, 9, 8101095]

print(f"part_1:", run_blinks(initial_stones, 25))
print(f"part_2:", run_blinks(initial_stones, 75))
