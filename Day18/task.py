import unittest
from dataclasses import dataclass
from enum import StrEnum
from typing import Sequence, Self, List, Iterator

from utils import Map, Vector


class Direction(StrEnum):
    RIGHT = 'R'
    LEFT = 'L'
    DOWN = 'D'
    UP = 'U'


@dataclass
class Instruction:
    direction: Direction
    len: int
    color: str

    @classmethod
    def parse(cls, line: str) -> Self:
        direction_part, len_part, color_part = line.split(' ')
        color_part = color_part.strip('()#\n ')
        return cls(
            Direction(direction_part),
            int(len_part),
            color_part
        )

    def apply(self, position: Vector) -> Vector:
        match self.direction:
            case Direction.DOWN:
                return Vector(position.x, position.y + self.len)
            case Direction.UP:
                return Vector(position.x, position.y - self.len)
            case Direction.LEFT:
                return Vector(position.x - self.len, position.y)
            case Direction.RIGHT:
                return Vector(position.x + self.len, position.y)

    def walk(self, position: Vector) -> Sequence[Vector]:
        for i in range(0, self.len):
            match self.direction:
                case Direction.DOWN:
                    yield Vector(position.x, position.y + i)
                case Direction.UP:
                    yield Vector(position.x, position.y - i)
                case Direction.LEFT:
                    yield Vector(position.x - i, position.y)
                case Direction.RIGHT:
                    yield Vector(position.x + i, position.y)

@dataclass
class Input:
    instructions: list[Instruction]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        ret = []
        while (line := next(lines, None)) is not None:
            ret.append(Instruction.parse(line))
        return cls(ret)


def load(input: str) -> Input:
    from utils import load_file_lines
    data = load_file_lines(input)
    return Input.parse(data)


def debug_print(map: Map):
    for iy in range(0, map.height):
        line = ""
        for ix in range(0, map.width):
            position = Vector(ix, iy)
            line += map[position]
        print(line + '\n')


def task1(input: Input) -> int:
    position = Vector(0, 0)
    max = Vector(0, 0)
    for instruction in input.instructions:
        position = instruction.apply(position)
        max = max.max_dim(position)

    map = Map(max.x + 1, max.y + 1, '.')
    position = Vector(0, 0)
    for instruction in input.instructions:
        for it in instruction.walk(position):
            map[it] = '#'
        position = instruction.apply(position)

    debug_print(map)

    for iy in range(0, map.height):
        prev = False
        switches = 0
        for ix in range(0, map.width):
            position = Vector(ix, iy)
            next = map[position] == '#'
            if prev is False and next is True:
                switches += 1
            if not next and switches % 2 == 1:
                map[position] = '#'
            prev = next

    print("------------------------")
    debug_print(map)

    ret = 0
    for iy in range(0, map.height):
        for ix in range(0, map.width):
            position = Vector(ix, iy)
            if map[position] == '#':
                ret += 1
    return ret


def task2(input: Input) -> int:
    ret = 0
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load('task_example.txt')
        self.assertEqual(14, len(input.instructions))
        self.assertEqual(Direction.DOWN, input.instructions[1].direction)
        self.assertEqual("5713f0", input.instructions[2].color)
        self.assertEqual(2, input.instructions[13].len)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load('task_example.txt')
        self.assertEqual(62, task1(input))

    def test_challenge(self):
        input = load("task_challenge.txt")
        self.assertEqual(-1, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load('task_example.txt')
        self.assertEqual(-1, task2(input))

    def test_challenge(self):
        input = load("task_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()