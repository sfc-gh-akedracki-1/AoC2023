import unittest
from typing import Sequence, Self, List, Optional
from dataclasses import dataclass, field

from utils.utils import load_file


@dataclass
class PartNumber:
    x: int
    y: int
    len: int
    value: int


@dataclass
class Gear:
    x: int
    y: int
    adjacent_part_numbers: List[PartNumber] = field(default_factory=list)


@dataclass
class Grid:
    width: int
    height: int
    data: List[str]
    gears: List[Gear] = field(default_factory=list)

    @classmethod
    def load(cls, input: str) -> Self:
        lines = input.splitlines()
        return Grid(
            width=len(lines[0]),
            height=len(lines),
            data=lines
        )

    def get(self, x: int, y: int) -> str:
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return '.'
        return self.data[y][x]

    @staticmethod
    def test_symbol(value: str) -> bool:
        return value != '.' and not value.isdigit()

    def is_symbol(self, x: int, y: int) -> bool:
        value = self.get(x, y)
        return value != '.' and not value.isdigit()

    def is_adjacent_to_symbol(self, x: int, y: int) -> bool:
        return self.is_symbol(x - 1, y - 1) or self.is_symbol(x - 1, y) or self.is_symbol(x - 1, y + 1) or \
            self.is_symbol(x, y - 1) or self.is_symbol(x, y + 1) or \
            self.is_symbol(x + 1, y - 1) or self.is_symbol(x + 1, y) or self.is_symbol(x + 1, y + 1)

    def is_gear(self, x: int, y: int) -> Optional[Gear]:
        value = self.get(x, y)
        if value != '*':
            return None

        candidate = next((gear for gear in self.gears if gear.x == x and gear.y == y), None)
        if candidate is None:
            candidate = Gear(x, y)
            self.gears.append(candidate)

        return candidate

    def adjacent_gears(self, x: int, y: int) -> Sequence[Gear]:
        ret = []

        def test(tx: int, ty: int):
            candidate = self.is_gear(tx, ty)
            if candidate is None:
                return
            ret.append(candidate)

        test(x - 1, y - 1)
        test(x - 1, y)
        test(x - 1, y + 1)
        test(x, y - 1)
        test(x, y + 1)
        test(x + 1, y - 1)
        test(x + 1, y)
        test(x + 1, y + 1)
        return ret


def task1(input: str) -> int:
    grid = Grid.load(input)
    ret = 0
    valid = False
    value = 0
    for iy in range(0, grid.height):
        for ix in range(0, grid.width + 1):
            cell = grid.get(ix, iy)
            if cell.isdigit():
                value = value * 10 + int(cell)
                valid = valid or grid.is_adjacent_to_symbol(ix, iy)
            else:
                if valid:
                    ret += value
                value = 0
                valid = False

    return ret


def task2(input: str) -> int:
    grid = Grid.load(input)
    ret = 0

    gears: List[Gear] = list()
    start = -1
    value = 0
    for iy in range(0, grid.height):
        for ix in range(0, grid.width + 1):
            cell = grid.get(ix, iy)
            if cell.isdigit():
                if start == -1:
                    start = ix
                value = value * 10 + int(cell)
                cell_gears = grid.adjacent_gears(ix, iy)
                for gear in cell_gears:
                    if gear not in gears:
                        gears.append(gear)
            else:
                if start != -1 and len(gears) > 0:
                    part_number = PartNumber(start, iy, ix - start, value)
                    for gear in gears:
                        gear.adjacent_part_numbers.append(part_number)
                gears.clear()
                value = 0
                start = -1

    ret = 0
    for gear in grid.gears:
        if len(gear.adjacent_part_numbers) != 2:
            continue
        ret += gear.adjacent_part_numbers[0].value * gear.adjacent_part_numbers[1].value

    return ret


class GridTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file('task1_example.txt')
        grid = Grid.load(input)
        self.assertEqual('4', grid.get(0,0))
        self.assertEqual('7', grid.get(2,0))
        self.assertEqual('6', grid.get(0,4))

    def test_is_symbol(self):
        input = load_file('task1_example.txt')
        grid = Grid.load(input)
        self.assertFalse(grid.is_symbol(0, 0))  # 4 is not
        self.assertFalse(grid.is_symbol(0, 1))  # . is not
        self.assertTrue(grid.is_symbol(3, 1))   # * is

    def test_is_adjacent_to_symbol(self):
        input = load_file('task1_example.txt')
        grid = Grid.load(input)
        self.assertFalse(grid.is_adjacent_to_symbol(0, 0))
        self.assertTrue(grid.is_adjacent_to_symbol(2, 0))
        self.assertFalse(grid.is_adjacent_to_symbol(1, 0))

    def test_adjacent_gears(self):
        input = load_file('task1_example.txt')
        grid = Grid.load(input)
        output1 = grid.adjacent_gears(2, 0)
        output2 = grid.adjacent_gears(2, 2)
        output3 = grid.adjacent_gears(3, 2)
        output4 = grid.adjacent_gears(6, 2)
        self.assertEqual(1, len(grid.gears))
        self.assertEqual(1, len(output1))
        self.assertEqual(1, len(output2))
        self.assertEqual(1, len(output3))
        self.assertEqual(0, len(output4))
        self.assertIn(output1[0], grid.gears)
        self.assertIn(output2[0], grid.gears)
        self.assertIn(output3[0], grid.gears)
        self.assertIs(output1[0], output2[0])
        self.assertIs(output2[0], output3[0])


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(4361, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(532428, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(467835, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()