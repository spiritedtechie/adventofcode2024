import re

pattern = re.compile(
    r"Button A: X([+-]\d+), Y([+-]\d+)\s*"
    r"Button B: X([+-]\d+), Y([+-]\d+)\s*"
    r"Prize: X=(\d+), Y=(\d+)"
)


# return list of tuples ((94, 34), (22, 67), (8400, 5400))
# in form ((button A x and y increments), (button B x and y increments), (target x and y))
def parse_file(filename, target_add=0):
    with open(filename, "r") as file:
        data = file.read()

    matches = pattern.findall(data)

    parsed_data = []
    for match in matches:
        button_a = (int(match[0]), int(match[1]))
        button_b = (int(match[2]), int(match[3]))
        prize = (int(match[4]) + target_add, int(match[5]) + target_add)
        parsed_data.append((button_a, button_b, prize))

    return parsed_data


def calculate_for_machine(machine_data):
    (Xa, Ya), (Xb, Yb), (Xp, Yp) = machine_data

    for a in range(1, 101):
        for b in range(1, 101):
            if Xa * a + Xb * b == Xp and Ya * a + Yb * b == Yp:
                return a, b

    return 0, 0


def fast_calculate_for_machine(machine_data):
    from sympy import symbols, Eq, solve

    (Xa, Ya), (Xb, Yb), (Xp, Yp) = machine_data

    a, b = symbols("a,b")

    # simultaneous equations to solve
    eq1 = Eq(Xa * a + Xb * b, Xp)
    eq2 = Eq(Ya * a + Yb * b, Yp)

    solutions = solve([eq1, eq2], (a, b))

    if all(solutions[var].is_integer for var in [a, b]):
        return solutions[a], solutions[b]

    return 0, 0


# Read about Cramers rule for solving linear equations
# and it seemed like the fastest and easiest method in the end
def cramers_rule_calculate_for_machine(machine_data):
    (Xa, Ya), (Xb, Yb), (Xp, Yp) = machine_data

    A = (Xa * Yb) - (Ya * Xb)
    A1 = (Xp * Yb) - (Yp * Xb)
    A2 = (Xa * Yp) - (Ya * Xp)

    a = A1 / A
    b = A2 / A

    if a % 1 == 0 and b % 1 == 0:
        return int(a), int(b)

    return 0, 0


def calculate(machines, alg_func):
    return sum(3 * a + b for machine in machines for a, b in [alg_func(machine)])


# Main
machines = parse_file("day13.txt")
machines_complex = parse_file("day13.txt", target_add=10000000000000)

print("part_1:", calculate(machines, calculate_for_machine))
print("part_2:", calculate(machines_complex, fast_calculate_for_machine))
print(
    "part_2 (cramers):", calculate(machines_complex, cramers_rule_calculate_for_machine)
)
