import re

register_pattern = r"Register (\w): (\d+)"
program_pattern = r"Program: ([\d,]+)"


def parse_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    registers = dict(re.findall(register_pattern, data))
    program = list(map(int, re.findall(program_pattern, data)[0].split(",")))

    return registers, program


def compute(r_a, r_b, r_c, program):
    combos = {
        0: lambda: 0,
        1: lambda: 1,
        2: lambda: 2,
        3: lambda: 3,
        4: lambda: r_a,
        5: lambda: r_b,
        6: lambda: r_c,
    }

    output = []

    pointer = 0
    while pointer < len(program) - 1:
        op_code, operand = program[pointer], program[pointer + 1]

        match op_code:
            case 0:
                r_a = r_a // (2 ** combos[operand]())
            case 1:
                r_b = r_b ^ operand
            case 2:
                r_b = combos[operand]() % 8
            case 3:
                pointer = operand - 2 if r_a != 0 else pointer
            case 4:
                r_b = r_b ^ r_c
            case 5:
                output.append(combos[operand]() % 8)
            case 6:
                r_b = r_a // 2 ** combos[operand]()
            case 7:
                r_c = r_a // 2 ** combos[operand]()

        pointer += 2

    return r_a, r_b, r_c, output


# The easiest way to understand this is to enable the print statements.
#
# Basically each digit in the output can only be 0 to 7 for this computer's logic. As 'a' grows
# the length of the list grows as each digit position is filled from 0-7.
# Using this knowledge, we can control (greatly reduce) the range of 'a' to explore to build up a
# complete match of the program.
#
# As we increase 'a', we are trying to match every growing slice of the program from the end.
# As we match a slice, we increase our value of 'a' accordingly to match the next slice (and so on),
# until we have matched the full program.
def find_min_a_to_output_program(program, a, i) -> int:
    _, _, _, output = compute(a, 0, 0, program)

    # base case - found match
    if output == program:
        # print(f"full match: a={a}, program={program}, output={output}")
        return a

    if output == program[-i:] or i == 0:
        # print(f"partial match: a={a}, program={program[-i:]}, output={output}")
        for n in range(8):
            # print("new a", 8 * a + n)
            result = find_min_a_to_output_program(program, 8 * a + n, i + 1)
            if result:
                return result
    return None


def part_1(registers, program):
    r_a = int(registers["A"])
    r_b = int(registers["B"])
    r_c = int(registers["C"])
    _, _, _, output = compute(r_a, r_b, r_c, program)
    print("part 1:", output)


def part_2(registers, program):
    print("part 2", find_min_a_to_output_program(program, a=0, i=0))


# Main
registers, program = parse_file("day17.txt")
part_1(registers, program)
part_2(registers, program)
