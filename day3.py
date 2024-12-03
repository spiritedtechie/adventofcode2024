import re

def read_file(filename):
    with open(filename) as file:
        return file.readlines()


def calculate_part1(lines):
    total = 0
    for line in lines:
        matches = re.findall(r"mul\((\d+),(\d+)\)", line)
        total += sum(int(num1) * int(num2) for num1, num2 in matches)

    return total

def calculate_part2(lines):
    def process_line(enabled, line):
        # opting to keep regex simple and do the processing of ordered parsed regex
        # match groups in code
        matches = re.findall(r"(do\(\))|(don't\(\))|mul\((\d+),(\d+)\)", line)     
        line_total = 0   
        for do, dont, num1, num2 in matches:
            if do: 
                enabled = True
            elif dont: 
                enabled = False
            elif enabled and num1 and num2: 
                line_total += int(num1) * int(num2)
        return enabled, line_total

    total, enabled = 0, True
    for line in lines:
        enabled, line_total = process_line(enabled, line)
        total += line_total

    return total

if __name__ == "__main__":
    lines = read_file("day3.txt")
    print(calculate_part1(lines))
    print(calculate_part2(lines))