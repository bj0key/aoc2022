import copy
import re


def main() -> tuple[str, str]:
    with open("day5/input") as file:
        data = file.read()
    init_stacks, moves = data.split("\n\n", 1)
    init_stacks = init_stacks.splitlines()[::-1]
    first_line = init_stacks.pop(0)

    stacks = [[] for _ in range(len(first_line.replace(" ", "")))]
    for s in init_stacks:
        letters = s[1::4]
        for s, l in zip(stacks, letters):
            if l != " ":
                s.append(l)

    stacks2 = copy.deepcopy(stacks)

    pttrn = re.compile(r"move (\d+) from (\d+) to (\d+)")
    buffer = []
    for move in moves.splitlines():
        amount, frm, to = map(int, pttrn.match(move).groups())
        for _ in range(amount):
            stacks[to - 1].append(stacks[frm - 1].pop())
            buffer.append(stacks2[frm - 1].pop())
        for _ in range(amount):
            stacks2[to - 1].append(buffer.pop())

    return "".join(s[-1] for s in stacks), "".join(s[-1] for s in stacks2)


if __name__ == "__main__":
    p1, p2 = main()
    print(f"Part 1: {p1}, part 2: {p2}")
