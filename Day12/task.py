import unittest
from dataclasses import dataclass
from typing import Sequence, Self, List


from utils import load_file

@dataclass
class Entry:
    pattern: str
    groups: list[int]

    @classmethod
    def parse(cls, line: str) -> Self:
        pattern, groups_part = line.strip().split(' ')
        return cls(
            pattern,
            [int(group.strip()) for group in groups_part.split(',')]
        )

    @classmethod
    def parse_multiple(cls, input: str) -> list[Self]:
        return [cls.parse(line.strip()) for line in input.splitlines()]

    def print_stats(self):
        sections = [section for section in self.pattern.split('.') if len(section) > 0]
        # print(f"{self.pattern} : {self.groups} -> {len(self.pattern)} - {sum(self.groups)} = {len(self.pattern) -sum(self.groups)} / {self.pattern.count('?')}")
        print(f"{self.pattern} : {self.groups} -> {sections}")


def task1(input: str) -> int:
    ret = 0
    entries = Entry.parse_multiple(input)
    for entry in entries:
        entry.print_stats()
    return ret


def task2(input: str) -> int:
    ret = 0
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file('task1_example.txt')
        entries = Entry.parse_multiple(input)
        self.assertEqual(6, len(entries))
        self.assertEqual('#.#.###', entries[0].pattern)
        self.assertEqual([4,1,1], entries[3].groups)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(21, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(-1, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(-1, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()