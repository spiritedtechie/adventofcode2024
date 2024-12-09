def read_file(filename):
    with open(filename) as file:
        return list(file.readline().strip())


def explode_input(line):
    return [
        i // 2 if i % 2 == 0 else "."
        for i, char in enumerate(line)
        for _ in range(int(char))  # Repeat character based on its count
    ]


def calculate_checksum(line):
    return sum(ind * val for ind, val in enumerate(line) if val != ".")


def find_contiguous_blocks(line, freespace=True):
    matcher = lambda chr: chr != "." if freespace else chr == "."
    blocks = []
    i = 0
    while i < len(line):
        # get to start of contiguous data
        if matcher(line[i]):
            i += 1
            continue

        # find end of next contiguous data
        j = i
        while j + 1 < len(line) and line[j + 1] == line[i]:
            j += 1

        # store the contiguous data range
        blocks.append((i, j))

        # repeat
        i = j + 1

    return blocks


def move_blocks_to_free_space(line: list, file_blocks: list, free_space_blocks: list):
    # process blocks in reverse to move into first possible free space
    for block_start, block_end in file_blocks[::-1]:
        block_size = block_end - block_start + 1

        for idx, (free_start, free_end) in enumerate(free_space_blocks):
            free_space_size = free_end - free_start + 1
            if free_start < block_start and free_space_size >= block_size:
                # move block into free space
                line[free_start : free_start + block_size] = line[block_start : block_end + 1]
                line[block_start : block_end + 1] = ["."] * (block_size)

                # update free space now used
                if free_end == free_start + block_size -1:
                    free_space_blocks.remove((free_start, free_end))
                else:
                    free_space_blocks[idx] = (free_start + block_size, free_end)

                break


def part_2(line: list):
    line = explode_input(line)

    file_blocks = find_contiguous_blocks(line, freespace=False)
    free_space_blocks = find_contiguous_blocks(line)

    move_blocks_to_free_space(line, file_blocks, free_space_blocks)

    checksum = calculate_checksum(line)
    print(checksum)


# O(n)
def part_1(line: list):
    def swap_elements(line: list, left_idx: int, right_idx: int):
        line[left_idx], line[right_idx] = line[right_idx], line[left_idx]

    line = explode_input(line)

    # use two pointers to swap relevant positions and calculate checksum on the way
    left_ptr, right_ptr = 0, len(line) - 1
    while left_ptr < right_ptr:
        if line[left_ptr] == "." and line[right_ptr] != ".":
            swap_elements(line, left_ptr, right_ptr)

        # shift to next positions
        left_ptr += 1 if line[left_ptr] != "." else 0
        right_ptr -= 1 if line[right_ptr] == "." else 0

    checksum = calculate_checksum(line)
    print(checksum)


if __name__ == "__main__":
    line = read_file("day9.txt")

    part_1(line)
    part_2(line)
