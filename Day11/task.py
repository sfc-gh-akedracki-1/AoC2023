import unittest
from dataclasses import dataclass, field
from typing import Sequence, Self, List


from utils import load_file


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int


@dataclass
class Sky:
    galaxies: list[Position]
    width: int
    height: int

    @classmethod
    def parse(cls, input: str) -> Self:
        lines = input.splitlines()
        height = len(lines)
        width = len(lines[0])

        galaxies = []
        for iy in range(0, height):
            line = lines[iy]
            for ix in range(0, width):
                if line[ix] == '#':
                    galaxies.append(Position(ix, iy))

        return cls(
            galaxies,
            width,
            height
        )

    def gravity_adjusted(self, factor: int) -> Self:
        def calculate_adjusts(input: list[int], dim: int) -> list[int]:
            ret = []
            value = 0
            for it in input:
                while len(ret) < it:
                    ret.append(value)
                value += factor - 1
            while len(ret) < dim:
                ret.append(value)
            return ret

        column_adjust = calculate_adjusts(self.empty_columns(), self.width)
        row_adjust = calculate_adjusts(self.empty_rows(), self.height)
        return Sky(
            [Position(it.x + column_adjust[it.x], it.y + row_adjust[it.y]) for it in self.galaxies],
            self.width + column_adjust[-1],
            self.height + row_adjust[-1],
        )

    def empty_columns(self) -> list[int]:
        taken : set[int] = set()
        for galaxy in self.galaxies:
            taken.add(galaxy.x)
        return [i for i in range(0, self.width) if i not in taken]

    def empty_rows(self) -> list[int]:
        taken : set[int] = set()
        for galaxy in self.galaxies:
            taken.add(galaxy.y)
        return [i for i in range(0, self.height) if i not in taken]


def task(input: str, factor: int) -> int:
    ret = 0
    sky = Sky.parse(input)
    adjusted_sky = sky.gravity_adjusted(factor)
    for i in range(0, len(adjusted_sky.galaxies) - 1):
        for j in range(i+1, len(adjusted_sky.galaxies)):
            first = adjusted_sky.galaxies[i]
            second = adjusted_sky.galaxies[j]
            ret += abs(first.x - second.x) + abs(first.y - second.y)
    return ret


class InputTestCase(unittest.TestCase):
    def load(self) -> Sky:
        input = load_file('task_example.txt')
        return Sky.parse(input)

    def test_parse(self):
        sky = self.load()
        self.assertEqual(10, sky.width)
        self.assertEqual(10, sky.height)
        self.assertEqual(9, len(sky.galaxies))

    def test_empty_columns(self):
        sky = self.load()
        self.assertListEqual([2, 5, 8], sky.empty_columns())

    def test_empty_rows(self):
        sky = self.load()
        self.assertListEqual([3, 7], sky.empty_rows())

    def test_gravity_adjusted_factor1(self):
        sky = self.load()
        adjusted_sky = sky.gravity_adjusted(2)
        self.assertEqual(sky.galaxies[0], Position(3, 0))
        self.assertEqual(sky.galaxies[3], Position(6, 4))
        self.assertEqual(adjusted_sky.galaxies[0], Position(4, 0))
        self.assertEqual(adjusted_sky.galaxies[3], Position(8, 5))

    def test_gravity_adjusted_factor10(self):
        sky = self.load()
        adjusted_sky = sky.gravity_adjusted(10)
        self.assertEqual(sky.galaxies[0], Position(3, 0))
        self.assertEqual(sky.galaxies[3], Position(6, 4))
        self.assertEqual(adjusted_sky.galaxies[0], Position(12, 0))
        self.assertEqual(adjusted_sky.galaxies[3], Position(24, 13))


class TaskTestCase(unittest.TestCase):
    def test_example_factor1(self):
        input = load_file('task_example.txt')
        self.assertEqual(374, task(input, 2))

    def test_challenge_factor2(self):
        input = load_file("task_challenge.txt")
        self.assertEqual(9521776, task(input,2))

    def test_example_factor10(self):
        input = load_file('task_example.txt')
        self.assertEqual(1030, task(input, 10))

    def test_example_factor100(self):
        input = load_file('task_example.txt')
        self.assertEqual(8410, task(input, 100))

    def test_challenge_factor1m(self):
        input = load_file('task_challenge.txt')
        self.assertEqual(553224415344, task(input, 1000000))


if __name__ == '__main__':
    unittest.main()