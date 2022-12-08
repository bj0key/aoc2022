from itertools import count
from typing import Callable, Generator

with open("day8/input") as file:
    data = [[int(i) for i in l.strip()] for l in file.readlines()]


# ========PART 1========


def reverse_enumerate(lst: list) -> Generator[tuple[int, int], None, None]:
    i = len(lst)
    for n in reversed(lst):
        i -= 1
        yield i, n


def make_visibility_mask(data: list[list[int]]) -> list[list[bool]]:
    visibility_mask = [[False] * len(row) for row in data]
    enumerators: list[Callable] = [enumerate, reverse_enumerate]
    for iterable in enumerators:
        for i, row in enumerate(data):
            curr_max = -1
            for j, n in iterable(row):
                if curr_max < n:
                    visibility_mask[i][j] = True
                    curr_max = n
    for iterable in enumerators:
        for j, col in enumerate(zip(*data)):
            curr_max = -1
            for i, n in iterable(col):
                if curr_max < n:
                    visibility_mask[i][j] = True
                    curr_max = n
    return visibility_mask


visibility_mask = make_visibility_mask(data)
# print("\n".join("".join(map(str, map(int, row))) for row in visibility_mask))
total_visible = sum(sum(row) for row in visibility_mask)
print(f"Part 1: {total_visible}")


# ========PART 2========


def on_edge(data: list[list[int]], y: int, x: int) -> bool:
    return x == 0 or y == 0 or x == len(data) - 1 or y == len(data) - 1


def trees_in_direction(
    data: list[list[int]], height: int, y: int, x: int, y_mod: int, x_mod: int, **_
) -> int:
    def is_taller(i: int) -> bool:
        nx = x + (i * x_mod)
        ny = y + (i * y_mod)
        return on_edge(data, ny, nx) or (i != 0 and data[ny][nx] >= height)

    # return inner
    return next(filter(is_taller, count()))


def get_prettiness(data: list[list[int]], y: int, x: int) -> int:
    height = data[y][x]
    dist_right = trees_in_direction(**locals(), y_mod=0, x_mod=+1)
    dist_left = trees_in_direction(**locals(), y_mod=0, x_mod=-1)
    dist_down = trees_in_direction(**locals(), y_mod=+1, x_mod=0)
    dist_up = trees_in_direction(**locals(), y_mod=-1, x_mod=0)
    return dist_down * dist_left * dist_right * dist_up


max_prettiness = max(
    max(get_prettiness(data, y, x) for x in range(len(data[0])))
    for y in range(len(data))
)

print(f"Part 2: {max_prettiness}")
