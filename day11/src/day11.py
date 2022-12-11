import operator
from pprint import pprint
import re
from dataclasses import dataclass, field
from typing import Callable, ClassVar

MONKEY_PATTERN = re.compile(
    r"""Monkey (?P<id>\d+):
  Starting items: (?P<items>(?:(?:\d+), )*?\d+)
  Operation: (?P<operation>.+)
  Test: (?P<test>.+)
    If true: throw to monkey (?P<to_t>\d+)
    If false: throw to monkey (?P<to_f>\d+)"""
)
OP_PATTERN = re.compile(r"new = (.+) ([\*\+]) (.+)")
TEST_PATTERN = re.compile(r"divisible by (\d+)")
OP_DICT = {"+": operator.add, "*": operator.mul}


def parse_operation(op_string: str) -> Callable[[int], int]:
    m = OP_PATTERN.match(op_string)
    if m is None:
        raise ValueError("Couldn't parse operation!")
    first, op_str, second = m.groups()
    op = OP_DICT[op_str]
    if first == second == "old":
        return lambda i: op(i, i)
    elif first == "old":
        second = int(second)
        return lambda i: op(i, second)
    else:
        first = int(first)
        return lambda i: op(first, i)


def parse_test(test_str: str) -> Callable[[int], bool]:
    m = TEST_PATTERN.match(test_str)
    if m is None:
        raise ValueError("Couldn't parse test!")
    n = int(m.group(1))
    return lambda i: i % n == 0


@dataclass
class Monkey:
    all_monkeys: ClassVar[dict[int, "Monkey"]] = {}

    id: int
    items: list[int]
    operation: Callable[[int], int]
    test: Callable[[int], bool]
    dest_true: int
    dest_false: int
    inspections: int = field(default=0, init=False)

    def __post_init__(self):
        all_monkeys = self.all_monkeys
        id = self.id
        if id in all_monkeys:
            raise ValueError(f"ID {id} already in use by another monkey!")
        all_monkeys[id] = self

    @classmethod
    def from_lines(cls, lines: str) -> "Monkey":
        match = MONKEY_PATTERN.match(lines)
        if match is None:
            raise ValueError("Could not parse lines into a monkey")
        (
            id_str,
            items_str,
            operation_str,
            test_str,
            dest_true_str,
            dest_false_str,
        ) = match.groups()
        id = int(id_str)
        items = [int(i) for i in items_str.split(", ")]
        operation = parse_operation(operation_str)
        test = parse_test(test_str)
        dest_true = int(dest_true_str)
        dest_false = int(dest_false_str)

        return Monkey(id, items, operation, test, dest_true, dest_false)

    @classmethod
    def reset_monkeys(cls):
        cls.all_monkeys.clear()

    def inspect(self, part1: bool):
        for item in self.items:
            item = self.operation(item)
            if part1:
                item //= 3
            if self.test(item):
                self.all_monkeys[self.dest_true].items.append(item)
            else:
                self.all_monkeys[self.dest_false].items.append(item)
        self.inspections += len(self.items)
        self.items.clear()


with open("day11/input") as file:
    monkey_data = file.read().split("\n\n")


def part1():
    Monkey.reset_monkeys()
    monkeys = [Monkey.from_lines(l) for l in monkey_data]
    for _ in range(20):
        for monkey in monkeys:
            monkey.inspect(part1=True)

    # for m in monkeys:
    #     print(f"Monkey {m.id}: {', '.join(map(str, m.items))}")
    # for m in monkeys:
    #     print(f"Monkey {m.id} inspected items {m.inspections} times.")

    sorted_inspections = sorted((m.inspections for m in monkeys), reverse=True)
    monkey_business = sorted_inspections[0] * sorted_inspections[1]
    print(monkey_business)

def part2():
    Monkey.reset_monkeys()
    monkeys = [Monkey.from_lines(l) for l in monkey_data]
    for _ in range(1000):
        for monkey in monkeys:
            monkey.inspect(part1=False)
    sorted_inspections = sorted((m.inspections for m in monkeys), reverse=True)
    monkey_business = sorted_inspections[0] * sorted_inspections[1]
    print(monkey_business)

if __name__ == "__main__":
    part1()
    # part2()