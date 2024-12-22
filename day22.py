def read_file(filename):
    with open(filename) as file:
        yield from map(int, file)


def price(secret):
    return secret % 10


def apply_process(secret):
    secret = (secret ^ secret * 64) % 16777216
    secret = (secret ^ secret // 32) % 16777216
    return (secret ^ secret * 2048) % 16777216


def part_1():
    num_price_changes = 2000
    total = 0

    for curr_secret in initial_numbers:
        for _ in range(num_price_changes):
            curr_secret = apply_process(curr_secret)

        total += curr_secret

    print(total)




# Main
initial_numbers = read_file("day22.txt")
part_1()

