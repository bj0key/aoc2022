from itertools import cycle

with open("day3/input") as file:
    lines = file.readlines()


def priority(c: str) -> int:
    if c.islower():
        return ord(c) - 96
    elif c.isupper():
        return ord(c) - 38


def main(lines: list[str]) -> tuple[int, int]:

    total = 0
    badge_total = 0
    elf_group = []
    for i, line in zip(cycle(range(3)), lines):
        first, second = line[: len(line) // 2], line[len(line) // 2 :]
        shared = next(x for x in first for y in second if x == y)
        total += priority(shared)
        if i == 2:
            badge = next(x for x in line if all(x in elf for elf in elf_group))
            badge_total += priority(badge)
            elf_group.clear()
        else:
            elf_group.append(line)
    return total, badge_total


if __name__ == "__main__":
    total, badge_total = main(lines)
    print(f"{total = }, {badge_total = }")
