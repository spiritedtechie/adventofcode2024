import re
from collections import deque

OPERATIONS = {
    "AND": lambda l, r: l & r,
    "OR": lambda l, r: l | r,
    "XOR": lambda l, r: l ^ r,
}


def parse(filename):
    with open(filename, "r") as file:
        content = file.read()

    wire_values = {
        name: int(value) for name, value in re.findall(r"(\w+):\s*(\d)", content)
    }

    connections = [
        (l_wire, op, r_wire, result_wire)
        for l_wire, op, r_wire, result_wire in re.findall(
            r"(\w+)\s*(XOR|OR|AND)\s*(\w+)\s*->\s*(\w+)", content
        )
    ]

    return wire_values, connections


def calculate(l_wire_val, r_wire_val, op_code):
    return OPERATIONS[op_code](l_wire_val, r_wire_val)


def process_connections(connections, wire_vals):
    wire_vals = dict(wire_vals)

    queue = deque(connections)
    while queue:
        l_wire, op_code, r_wire, res_wire = queue.pop()

        if l_wire in wire_vals and r_wire in wire_vals:
            wire_vals[res_wire] = calculate(
                wire_vals[l_wire], wire_vals[r_wire], op_code
            )
        else:
            queue.appendleft((l_wire, op_code, r_wire, res_wire))

    return wire_vals


def get_z_decimal(wire_vals):
    z_wire_vals = sorted(
        [(key, val) for key, val in wire_vals.items() if key.startswith("z")],
        reverse=True,
    )
    z_binary = "".join(str(v) for _, v in z_wire_vals)
    return int(z_binary, 2)


# Main
filename = "day24.txt"
initial_vals, connections = parse(filename)
wire_vals = process_connections(connections, initial_vals)
z_decimal = get_z_decimal(wire_vals)
print("part 1:", z_decimal)
