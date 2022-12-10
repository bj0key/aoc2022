from __future__ import annotations
from typing import Generator, Literal, Optional, Union
from abc import ABC, abstractmethod


def line_reader(filename) -> Generator[str, None, None]:
    with open(filename) as file:
        for line in file:
            c, i = line.split(None, 1)
            for _ in range(int(i)):
                yield c


class RopePartABC(ABC):
    _x: int
    _y: int
    _next: Optional[RopePartABC]

    @abstractmethod
    def move(self, direction: str) -> None:
        ...

    @property
    @abstractmethod
    def pos(self) -> tuple[int, int]:
        ...


class RopeHead(RopePartABC):
    def __init__(self) -> None:
        self._x = 0
        self._y = 0
        self._next: RopeKnot | None = None

    @property
    def pos(self) -> tuple[int, int]:
        return (self._x, self._y)

    def move(self, direction: str):
        match direction:
            case "R":
                self._x += 1
            case "L":
                self._x -= 1
            case "U":
                self._y += 1
            case "D":
                self._y -= 1
            case _:
                raise ValueError(f"Couldn't recognise direction {direction}!")
        if self._next is not None:
            self._next.move(direction)


class RopeKnot(RopePartABC):
    def __init__(self, to_follow: RopePartABC) -> None:
        self._prev = to_follow
        to_follow._next = self
        self._next: Optional[RopeKnot] = None
        self._x = to_follow._x
        self._y = to_follow._y
        self.visited: set[tuple[int, int]] = {(self._x, self._y)}

    @property
    def pos(self):
        return (self._x, self._y)

    def dist_to(self, other: RopePartABC) -> int:
        return max(abs(self._x - other._x), abs(self._y - other._y))

    def dist_from_last(self):
        return self.dist_to(self._prev)

    def log_pos(self):
        self.visited.add(self.pos)

    def move(self, direction: str):
        dx = self._prev._x - self._x
        dy = self._prev._y - self._y
        dx_n = dx and dx // abs(dx)
        dx_y = dy and dy // abs(dy)
        while self.dist_from_last() > 1:
            self._x += dx_n
            self._y += dx_y
            self.log_pos()
        if self._next is not None:
            self._next.move(direction)

    def visualise(self) -> None:
        min_x = min(p[0] for p in self.visited)
        min_y = min(p[1] for p in self.visited)
        max_x = max(p[0] for p in self.visited)
        max_y = max(p[1] for p in self.visited)
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y) == (0, 0):
                    print("s", end="")
                elif (x, y) in self.visited:
                    print("#", end="")
                else:
                    print("-", end="")
            print()


rope_head = RopeHead()
last: RopePartABC = rope_head
rope: list[RopeKnot] = []
for i in range(9):
    rope.append(RopeKnot(last))
    last = rope[-1]


for move in line_reader("day9/input"):
    rope_head.move(move)

# rope[-1].visualise()
print(len(rope[0].visited))
print(len(rope[-1].visited))
