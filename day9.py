from collections import defaultdict
import re

def read_file(filename):
    with open(filename) as file:
        return list(file.readline().strip())


def explode_input(line):
    # explode original line
    newlist = []
    for ind, val in enumerate(line):
        if ind % 2 == 0:
            newlist.extend([ind // 2] * int(val))
        else:
            new_entries = ["."] * int(val)
            if new_entries:
                newlist.extend(new_entries)

    return newlist


def calculate_checksum(list):
    checksum = 0
    for ind, val in enumerate(list):
        if val != ".":
            # checksum remainder
            checksum += ind * val
    return checksum

# O(n)
def part_1(line: list):
    newlist = explode_input(line)

    # use two pointers to swap relevant positions and calculate checksum on the way
    left_ptr = 0
    right_ptr = len(newlist) - 1

    while left_ptr < right_ptr:
        if newlist[left_ptr] == "." and newlist[right_ptr] != ".":
            # swap
            tmp = newlist[left_ptr]
            newlist[left_ptr] = newlist[right_ptr]
            newlist[right_ptr] = tmp

        # shift to next positions
        while newlist[left_ptr] != ".":
            left_ptr += 1
        while newlist[right_ptr] == ".":
            right_ptr -= 1

    # calculate checksum
    checksum = calculate_checksum(newlist)

    print(checksum)


def part_2(line: list):
    line = explode_input(line)

    def find_contiguous_blocks(line, freespace=True):
        matcher = lambda chr : chr != '.' if freespace else chr == '.'
        blocks = list()
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



    blocks_to_move = find_contiguous_blocks(line, freespace=False)
    free_space = find_contiguous_blocks(line)
    

    # process blocks to move into first possible free space that can take it
    for bi, bj in blocks_to_move[::-1]:

        block_size = bj - bi

        for idx, (fi, fj) in enumerate(free_space):
            if fi < bi and fj-fi >= block_size:
                # swap
                n2 = (['.'] * int(bj-bi+1))
                n1 =  line[bi: bj + 1]

                line[fi: fi+block_size+1] = n1
                line[bi: bj+1] = n2

                # update free space now used
                if fj == fi+block_size:
                    free_space.remove((fi, fj))
                else:
                    free_space[idx] = (fi+block_size+1, fj)

                break

                

    # calculate checksum
    checksum = calculate_checksum(line)
    print(checksum) 


if __name__ == "__main__":
    line = read_file("day9.txt")

    # part_1(line)
    part_2(line)
