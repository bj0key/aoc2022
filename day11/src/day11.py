import math
import operator
import re
from dataclasses import dataclass, field
from typing import Callable, ClassVar, Optional

MONKEY_PATTERN = re.compile(
    r"""Monkey (\d+):
  Starting items: ((?:(?:\d+), )*?\d+)
  Operation: new = old ([+*]) ((?:\d+)|(?:old))
  Test: divisible by (.+)
    If true: throw to monkey (\d+)
    If false: throw to monkey (\d+)"""
)
OP_DICT = {"+": operator.add, "*": operator.mul}


@dataclass
class Monkey:
    all_monkeys: ClassVar[dict[int, "Monkey"]] = {}
    div_lcm: ClassVar[int] = -1

    id: int
    items: list[int]
    op_func: Callable[[int, int], int]
    op_param: Optional[int]
    test_div_by: int
    dest_true: int
    dest_false: int
    inspections: int = field(default=0, init=False)

    def __post_init__(self):
        all_monkeys = self.all_monkeys
        id = self.id
        if id in all_monkeys:
            raise ValueError(f"ID {id} already in use by another monkey!")
        all_monkeys[id] = self
        if self.__class__.div_lcm == -1:
            self.__class__.div_lcm = self.test_div_by
        else:
            self.__class__.div_lcm = math.lcm(self.__class__.div_lcm, self.test_div_by)

    @classmethod
    def from_lines(cls, lines: str) -> "Monkey":
        match = MONKEY_PATTERN.match(lines)
        if match is None:
            raise ValueError("Could not parse lines into a monkey")
        (
            id_str,
            items_str,
            op_func_str,
            op_param_str,
            test_div_by_str,
            dest_true_str,
            dest_false_str,
        ) = match.groups()
        id = int(id_str)
        items = [int(i) for i in items_str.split(", ")]
        op_func = OP_DICT[op_func_str]
        op_param = None if op_param_str == "old" else int(op_param_str)
        test_div_by = int(test_div_by_str)
        dest_true = int(dest_true_str)
        dest_false = int(dest_false_str)

        return Monkey(id, items, op_func, op_param, test_div_by, dest_true, dest_false)

    @classmethod
    def reset_monkeys(cls):
        cls.div_lcm = -1
        cls.all_monkeys.clear()

    def do_op(self, val: int) -> int:
        """Performs the operation, also doing part 2's mod shenannigans if Monkey.div_lcm has been set."""
        val2 = val if self.op_param is None else int(self.op_param)
        return self.op_func(val, val2)

    def inspect(self, part1: bool):
        for item in self.items:
            item = self.do_op(item)
            if part1:
                item //= 3
            else:
                item %= self.div_lcm

            if item % self.test_div_by == 0:
                self.all_monkeys[self.dest_true].items.append(item)
            else:
                self.all_monkeys[self.dest_false].items.append(item)
        self.inspections += len(self.items)
        self.items.clear()


def part1(monkey_data: list[str]):
    Monkey.reset_monkeys()
    monkeys = [Monkey.from_lines(l) for l in monkey_data]
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect(part1=True)
    sorted_inspections = sorted((m.inspections for m in monkeys), reverse=True)
    monkey_business = sorted_inspections[0] * sorted_inspections[1]
    print(monkey_business)


def part2(monkey_data: list[str]):
    Monkey.reset_monkeys()
    monkeys = [Monkey.from_lines(l) for l in monkey_data]
    for _ in range(10_000):
        for monkey in monkeys:
            monkey.inspect(part1=False)
    sorted_inspections = sorted((m.inspections for m in monkeys), reverse=True)
    monkey_business = math.prod(sorted_inspections[:2])
    print(monkey_business)


with open("day11/input") as file:
    monkey_data = file.read().split("\n\n")

if __name__ == "__main__":
    part1(monkey_data)
    part2(monkey_data)
