"""A horrible, horrible solution that uses hella overengineered generators"""
from typing import Iterator, Generator

with open("day1/input") as f:
    lines = f.readlines()


def elf_gen(gen: Iterator[str], first: str) -> Generator[int, None, None]:
    yield int(first)
    for line in gen:
        if line == "\n":
            return
        yield int(line)


def elf_gen_gen(lines: list[str]) -> Generator[Generator[int, None, None], None, None]:
    line_iter = iter(lines)
    while True:
        next_line = next(line_iter, None)
        if next_line is None:
            return
        yield elf_gen(line_iter, next_line)


elf_sums = sorted(sum(elf_scores) for elf_scores in elf_gen_gen(lines))
top_3 = elf_sums[-3:]
x, y, z = top_3
print(f"The top 3 elves scores are {x}, {y}, and {z}, with a total sum of {sum(top_3)}")
