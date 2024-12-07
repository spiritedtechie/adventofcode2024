from collections import deque


def read_file(filename):
    with open(filename) as file:
        result = []
        for line in file:
            test_value_str, numbers_str = line.split(": ")
            test_value = int(test_value_str)
            numbers_tuple = tuple(map(int, numbers_str.split()))
            result.append((test_value, numbers_tuple))
    return result


def can_evaluate_to_expected(expected, nums: tuple) -> bool:
    # best option for O(1) appends to beginning
    queue = deque()
    queue.appendleft(nums[0])

    for cur_idx in range(1, len(nums)):
        for _ in range(len(queue)):
            prev = queue.pop()
            next_1, next_2 = prev + nums[cur_idx], prev * nums[cur_idx]

            if expected in [next_1, next_2]:
                return True

            queue.appendleft(next_1)
            queue.appendleft(next_2)

    return False


if __name__ == "__main__":
    lines = read_file("day7.txt")
    total_sum = sum(
        [line[0] for line in lines if can_evaluate_to_expected(line[0], line[1])]
    )
    print(total_sum)


# 5030892084481
