import unittest
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Sequence, Self, List, Iterator, Optional, Callable

from utils import load_file, load_file_lines


class Field(StrEnum):
    ASH = '.'
    ROCK = '#'

    def __str__(self):
        return self.value


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int


@dataclass
class Pattern:
    fields: list[list[Field]]
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self):
        self.height = len(self.fields)
        self.width = len(self.fields[0] if self.height > 0 else 0)

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Optional[Self]:
        consumed = []
        while True:
            line = next(lines, None)
            if line is None or len(line := line.strip()) == 0:
                break
            consumed.append(line)

        if len(consumed) == 0:
            return None

        return cls(
            [[Field(symbol) for symbol in line] for line in consumed]
        )

    @classmethod
    def parse_multiple(cls, lines: Iterator[str]) -> list[Self]:
        ret = []
        while (pattern := cls.parse(lines)) is not None:
            ret.append(pattern)
        return ret

    def get(self, position: Position) -> str:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return self.fields[position.y][position.x]
        raise IndexError(f"The provided {position} is outside of the map bounds (width: {self.width}, height: {self.height})")

    def find_vertical_reflection(self, target_errors: int) -> Optional[int]:
        return self._find_reflection(self.width, self.height, lambda primary, secondary: Position(primary, secondary), target_errors)

    def find_horizontal_reflection(self, target_errors: int) -> Optional[int]:
        return self._find_reflection(self.height, self.width, lambda primary, secondary: Position(secondary, primary), target_errors)

    def _find_reflection(self, primary_dimension: int, secondary_dimension: int, accessor: Callable[[int, int], Position], target_errors: int) -> Optional[int]:
        candidates = {i: 0 for i in range(0, primary_dimension-1)}
        for secondary in range(0, secondary_dimension):
            for primary, value in candidates.items():
                if value > target_errors:
                    continue
                count = min(primary + 1, primary_dimension - primary - 1)
                for i in range(0, count):
                    near = accessor(primary - i, secondary)
                    far = accessor(primary + i + 1, secondary)
                    if self.get(near) != self.get(far):
                        value += 1
                candidates[primary] = value
        for primary, value in candidates.items():
            if value == target_errors:
                return primary
        else:
            return None


def task1(input: Iterator[str]) -> int:
    ret = 0
    patterns = Pattern.parse_multiple(input)
    for pattern in patterns:
        if (vertical := pattern.find_vertical_reflection(0)) is not None:
            ret += vertical + 1
        if (horizontal := pattern.find_horizontal_reflection(0)) is not None:
            ret += (horizontal + 1) * 100
    return ret


def task2(input: Iterator[str]) -> int:
    ret = 0
    patterns = Pattern.parse_multiple(input)
    for pattern in patterns:
        if (vertical := pattern.find_vertical_reflection(1)) is not None:
            ret += vertical + 1
        if (horizontal := pattern.find_horizontal_reflection(1)) is not None:
            ret += (horizontal + 1) * 100
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file_lines('task_example.txt')
        patterns = Pattern.parse_multiple(input)
        self.assertEqual(2, len(patterns))

    def test_find_vertical_reflection_error0(self):
        input = load_file_lines('task_example.txt')
        patterns = Pattern.parse_multiple(input)
        self.assertEqual(4, patterns[0].find_vertical_reflection(0))
        self.assertEqual(None, patterns[1].find_vertical_reflection(0))

    def test_find_horizontal_reflection_error0(self):
        input = load_file_lines('task_example.txt')
        patterns = Pattern.parse_multiple(input)
        self.assertEqual(None, patterns[0].find_horizontal_reflection(0))
        self.assertEqual(3, patterns[1].find_horizontal_reflection(0))

    def test_find_vertical_reflection_error1(self):
        pass
        # input = load_file_lines('task_example.txt')
        # patterns = Pattern.parse_multiple(input)
        # self.assertEqual(4, patterns[0].find_vertical_reflection(1))
        # self.assertEqual(None, patterns[1].find_vertical_reflection(1))

    def test_find_horizontal_reflection_error1(self):
        input = load_file_lines('task_example.txt')
        patterns = Pattern.parse_multiple(input)
        self.assertEqual(2, patterns[0].find_horizontal_reflection(1))
        self.assertEqual(0, patterns[1].find_horizontal_reflection(1))


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task_example.txt')
        self.assertEqual(405, task1(input))

    def test_challenge(self):
        input = load_file_lines("task_challenge.txt")
        self.assertEqual(28651, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task_example.txt')
        self.assertEqual(400, task2(input))

    def test_challenge(self):
        input = load_file_lines("task_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()