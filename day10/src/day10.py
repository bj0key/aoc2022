from typing import Generator
FANCY_MODE = True # If true, makes part 2 use ANSI colours instead of # and .

def line_parser(filename: str) -> Generator[int, None, None]:
    with open(filename) as file:
        for line in file:
            if line.startswith("noop"):
                yield 0
            elif line.startswith("addx"):
                yield 0  # takes 1 cycle that doesn't update register
                yield int(line.split(None, 1)[-1])


register_x = 1
sum_of_20s = 0
for cycle, n in enumerate(line_parser("day10/input"), 1):
    if cycle % 40 == 20:
        # print(f"During the {cycle}th cycle, register X has the value {register_x}, so the signal strength is {cycle} * {register_x} = {cycle*register_x}")
        sum_of_20s += register_x * cycle
    register_x += n

print(sum_of_20s)


register_x = 1
for cycle, n in enumerate(line_parser("day10/input")):
    row_pos = cycle % 40
    if abs(row_pos - register_x) < 2:
        char = "\x1b[37m█\x1b[0m" if FANCY_MODE else "#"
    else:
        char = "\x1b[30m█\x1b[0m" if FANCY_MODE else "."
    print(char, end="")
    if row_pos == 39:
        print()

    register_x += n
