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


def is_equation_possible(expected, nums: tuple, op_applicator_func) -> bool:
    # best option for O(1) appends to beginning
    queue = deque([nums[0]])

    for cur_idx in range(1, len(nums)):
        for _ in range(len(queue)):
            prev = queue.pop()
            next_calculated: list = op_applicator_func(prev, nums[cur_idx])

            if cur_idx == len(nums) - 1 and expected in next_calculated:
                return True

            queue.extendleft(next_calculated)

    return False


def part_1_op_applicator(lhs: int, rhs: int):
    return [lhs + rhs, lhs * rhs]


def part_2_op_applicator(lhs: int, rhs: int):
    return part_1_op_applicator(lhs, rhs) + [int(str(lhs) + str(rhs))]


def part_1(lines):
    total_sum = sum(
        line[0]
        for line in lines
        if is_equation_possible(line[0], line[1], part_1_op_applicator)
    )
    print("part 1:", total_sum)


def part_2(lines):
    total_sum = sum(
        line[0]
        for line in lines
        if is_equation_possible(line[0], line[1], part_2_op_applicator)
    )
    print("part 2:", total_sum)


if __name__ == "__main__":
    lines = read_file("day7.txt")
    part_1(lines)
    part_2(lines)
