import re

pattern = re.compile(
    r"Button A: X([+-]\d+), Y([+-]\d+)\s*"
    r"Button B: X([+-]\d+), Y([+-]\d+)\s*"
    r"Prize: X=(\d+), Y=(\d+)"
)


# return list of tuples ((94, 34), (22, 67), (8400, 5400))
# in form ((button A x and y increments), (button B x and y increments), (target x and y))
def parse_file(filename):
    with open(filename, "r") as file:
        data = file.read()

    matches = pattern.findall(data)

    parsed_data = []
    for match in matches:
        button_a = (int(match[0]), int(match[1]))
        button_b = (int(match[2]), int(match[3]))
        prize = (int(match[4]), int(match[5]))
        parsed_data.append((button_a, button_b, prize))

    return parsed_data


def calculate_for_machine(machine_data):
    target_x, target_y = machine_data[2]
    btn_a_x_inc, btn_a_y_inc = machine_data[0]
    btn_b_x_inc, btn_b_y_inc = machine_data[1]

    for a in range(1, 101):
        xi = a * btn_a_x_inc
        yi = a * btn_a_y_inc

        for b in range(1, 101):
            xj = b * btn_b_x_inc
            yj = b * btn_b_y_inc

            if xi + xj == target_x and yi + yj == target_y:
                return a, b

    return (0, 0)


# Main
machines = parse_file("day13.txt")

cost = sum(
    3 * a + b for machine in machines for a, b in [calculate_for_machine(machine)]
)
print(cost)
