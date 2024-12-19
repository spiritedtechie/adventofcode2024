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
        op_code = program[pointer]
        operand = program[pointer + 1]

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


# Main
registers, program = parse_file("day17.txt")

# Part 1
r_a = int(registers["A"])
r_b = int(registers["B"])
r_c = int(registers["C"])
r_a, r_b, r_c, output = compute(r_a, r_b, r_c, program)
print("part 1:", output)


# # Part 2
# r_a = 43980465111040
# r_b = 0
# r_c = 0
# while r_a != 0:
#     _, _, _, output = execute(r_a, r_b, r_c, program)
#     print(r_a, r_b, r_c, output)

#     if output == program:
#         print(r_a, output)

#     import time
#     time.sleep(0.5)

#     r_a += 1
