import re

register_pattern = r"Register (\w): (\d+)"
program_pattern = r"Program: ([\d,]+)"


def parse_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    registers = dict(re.findall(register_pattern, data))
    program = list(map(int, re.findall(program_pattern, data)[0].split(",")))

    return registers, program


combos = {
    0: lambda r_a, r_b, r_c: 0,
    1: lambda r_a, r_b, r_c: 1,
    2: lambda r_a, r_b, r_c: 2,
    3: lambda r_a, r_b, r_c: 3,
    4: lambda r_a, r_b, r_c: r_a,
    5: lambda r_a, r_b, r_c: r_b,
    6: lambda r_a, r_b, r_c: r_c,
}


def op_0(r_a, r_b, r_c, operand):
    r_a = r_a // (2 ** combos[operand](r_a, r_b, r_c))
    return r_a, r_b, r_c


def op_1(r_a, r_b, r_c, operand):
    r_b = r_b ^ operand
    return r_a, r_b, r_c


def op_2(r_a, r_b, r_c, operand):
    r_b = combos[operand](r_a, r_b, r_c) % 8
    return r_a, r_b, r_c


def op_3(r_a, r_b, r_c, operand):
    return r_a != 0


def op_4(r_a, r_b, r_c, operand):
    r_b = r_b ^ r_c
    return r_a, r_b, r_c


def op_5(r_a, r_b, r_c, operand):
    return combos[operand](r_a, r_b, r_c) % 8


def op_6(r_a, r_b, r_c, operand):
    r_b = r_a // 2 ** combos[operand](r_a, r_b, r_c)
    return r_a, r_b, r_c


def op_7(r_a, r_b, r_c, operand):
    r_c = r_a // 2 ** combos[operand](r_a, r_b, r_c)
    return r_a, r_b, r_c


op_code_function = {
    0: op_0,
    1: op_1,
    2: op_2,
    3: op_3,
    4: op_4,
    5: op_5,
    6: op_6,
    7: op_7,
}


def execute(r_a, r_b, r_c, program):
    output = []

    pointer = 0
    while pointer < len(program) - 1:
        op_code = program[pointer]
        operand = program[pointer + 1]

        func = op_code_function[op_code]

        if op_code == 5:
            output.append(func(r_a, r_b, r_c, operand))
            pointer += 2
        elif op_code == 3:
            if func(r_a, r_b, r_c, operand):
                pointer = operand
            else:
                pointer += 2
        else:
            r_a, r_b, r_c = func(r_a, r_b, r_c, operand)
            pointer += 2

    return r_a, r_b, r_c, output


# Main
registers, program = parse_file("day17_test.txt")

# Part 1
r_a = int(registers["A"])
r_b = int(registers["B"])
r_c = int(registers["C"])
r_a, r_b, r_c, output = execute(r_a, r_b, r_c, program)
print("part 1:", output)
