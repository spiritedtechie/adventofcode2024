from collections import Counter


def read_file(filename):
    with open(filename) as file:
        yield from map(int, file)


def compute_next_secret(secret):
    secret = (secret ^ secret * 64) % 16777216
    secret = (secret ^ secret // 32) % 16777216
    return (secret ^ secret * 2048) % 16777216


def generate_secrets(secret, iterations=2000):
    secrets = [secret]
    for _ in range(iterations):
        secret = compute_next_secret(secret)
        secrets.append(secret)
    return secrets


def get_prices(secrets):
    prices = [s % 10 for s in secrets]
    price_diffs = [p2 - p1 for p1, p2 in zip(prices, prices[1:])]
    return prices, price_diffs


def part_1(numbers):
    return sum(secrets[-1] for secrets in (generate_secrets(num) for num in numbers))


def part2(numbers, seq_len=4):
    seq_banana_counts = Counter()

    for num in numbers:
        secrets = generate_secrets(num)
        prices, price_diffs = get_prices(secrets)

        visited_seqs = set()
        for seq_start in range(len(price_diffs) - seq_len + 1):
            seq = tuple(price_diffs[seq_start : seq_start + seq_len])

            if seq not in visited_seqs:
                seq_banana_counts[seq] += prices[seq_start + seq_len]
                visited_seqs.add(seq)

    most_common_seq = seq_banana_counts.most_common(1)
    return most_common_seq[0][1] if most_common_seq else 0


# Main
numbers = read_file("day22.txt")
print(part_1(numbers))

numbers = read_file("day22.txt")
print(part2(numbers))
