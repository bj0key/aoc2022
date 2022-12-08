from itertools import count, product

with open("day8/input") as file:
    data = [[int(i) for i in l.strip()] for l in file.readlines()]


# ========PART 1========


def reverse_enumerate(lst: list):
    i = len(lst)
    for n in reversed(lst):
        i -= 1
        yield i, n


def make_visibility_mask(data: list[list[int]]) -> list[list[bool]]:
    visibility_mask = [[False] * len(row) for row in data]
    for iterable in (enumerate, reverse_enumerate):
        for i, row in enumerate(data):
            curr_max = -1
            for j, n in iterable(row):
                if curr_max < n:
                    visibility_mask[i][j] = True
                    curr_max = n
    for iterable in (enumerate, reverse_enumerate):
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


def on_edge(data: list[list[int]], y: int, x: int) -> int:
    return x == 0 or y == 0 or x == len(data) - 1 or y == len(data) - 1


def get_prettiness(data: list[list[int]], y: int, x: int) -> int:
    height = data[y][x]
    # look right
    dist_right = next(
        i
        for i in count()
        if on_edge(data, y, x + i) or (i != 0 and data[y][x + i] >= height)
    )
    dist_left = next(
        i
        for i in count()
        if on_edge(data, y, x - i) or (i != 0 and data[y][x - i] >= height)
    )
    dist_down = next(
        i
        for i in count()
        if on_edge(data, y + i, x) or (i != 0 and data[y + i][x] >= height)
    )
    dist_up = next(
        i
        for i in count()
        if on_edge(data, y - i, x) or (i != 0 and data[y - i][x] >= height)
    )
    return dist_down * dist_left * dist_right * dist_up


max_prettiness = max(
    max(get_prettiness(data, y, x) for x in range(len(data[0])))
    for y in range(len(data))
)

print(f"Part 2: {max_prettiness}")
