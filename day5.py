from collections import defaultdict

def read_file(filename):
    with open(filename) as file:
        return [line.rstrip().split(',') for line in file]
    

if __name__ == "__main__":
    rules = read_file("day5_rules.txt")
    updates = read_file("day5_updates.txt")

    # index 
    afters = defaultdict(set)
    # inverted index
    befores = defaultdict(set)

    with open("day5_rules.txt") as file:
        for line in file:
            tokens = line.rstrip().split("|")
            afters[tokens[0]].add(tokens[1])
            befores[tokens[1]].add(tokens[0])

    def is_before(item, rest) -> bool:
        if not rest:
            return True
        
        prev_item = int(item)
        item = int(item)
        next_item = int(rest[0])

        if next_item in afters(item) and item:
            is_before(next_item, rest[1:])

        
    
    print(updates)