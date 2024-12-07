from collections import deque
import timeit


def read_file(filename):
    with open(filename) as file:
        return [
            (int(test_value), tuple(map(int, numbers_str.split())))
            for line in file
            for test_value, numbers_str in [line.split(": ")]
        ]


def part_1_op_applicator(left: int, right: int):
    added = left + right if left else 0 + right
    multiplied = left * right if left else 1 * right
    return [added, multiplied]


def part_2_op_applicator(left: int, right: int):
    combined = int(str(left) + str(right)) if left else right
    return part_1_op_applicator(left, right) + [combined]


# Breadth first search of the calculation space
def is_equation_possible_bfs(expected, nums: tuple, op_applicator_func) -> bool:
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


# Depth first search of the calculation space
def is_equation_possible_dfs(expected, nums: tuple, op_applicator_func) -> bool:
    def check_rec(nums, expected, sum=None) -> bool:
        new_sums = op_applicator_func(sum, nums[0])

        if len(nums) == 1:  # i.e. end of calculation
            return expected in new_sums

        return any(check_rec(nums[1:], expected, sum) for sum in new_sums)

    return check_rec(nums, expected)


def runner(lines, algorithm_func, op_applications_func):
    total_sum = sum(
        line[0]
        for line in lines
        if algorithm_func(line[0], line[1], op_applications_func)
    )
    print(f"{algorithm_func.__name__} -- {op_applications_func.__name__} -->", total_sum)


if __name__ == "__main__":
    lines = read_file("day7.txt")

    timer = timeit.Timer(lambda: runner(lines, is_equation_possible_bfs, part_1_op_applicator))
    elapsed = timer.timeit(1)
    print(f"Time taken: {elapsed:.6f} seconds\n")

    timer = timeit.Timer(lambda: runner(lines, is_equation_possible_dfs, part_1_op_applicator))
    elapsed = timer.timeit(1)
    print(f"Time taken: {elapsed:.6f} seconds\n")

    timer = timeit.Timer(lambda: runner(lines, is_equation_possible_bfs, part_2_op_applicator))
    elapsed = timer.timeit(1)
    print(f"Time taken: {elapsed:.6f} seconds\n")

    timer = timeit.Timer(lambda: runner(lines, is_equation_possible_dfs, part_2_op_applicator))
    elapsed = timer.timeit(1)
    print(f"Time taken: {elapsed:.6f} seconds\n")
