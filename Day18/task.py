import unittest
from dataclasses import dataclass
from enum import StrEnum
from typing import Sequence, Self, Iterator

from utils import Map, Vector, hexstr_to_int


class Direction(StrEnum):
    RIGHT = 'R'
    LEFT = 'L'
    DOWN = 'D'
    UP = 'U'


@dataclass
class Instruction:
    direction: Direction
    len: int

    @classmethod
    def parse(cls, line: str, alternate: bool = False) -> Self:
        direction_part, len_part, color_part = line.split(' ')
        if not alternate:
            return cls(
                Direction(direction_part),
                int(len_part)
            )
        else:
            color_part = color_part.strip('()#\n ')
            direction = Direction.UP
            match color_part[5]:
                case '0':
                    direction = Direction.RIGHT
                case '1':
                    direction = Direction.DOWN
                case '2':
                    direction = Direction.LEFT
                case '3':
                    direction = Direction.UP

            return cls(
                direction,
                hexstr_to_int(color_part[0:5])
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
        vertical_bonus = 1 if self.direction in [Direction.UP, Direction.DOWN] else 0
        for i in range(1 - vertical_bonus, self.len + vertical_bonus):
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
    def parse(cls, lines: Iterator[str], alternate: bool = False) -> Self:
        ret = []
        while (line := next(lines, None)) is not None:
            ret.append(Instruction.parse(line, alternate))
        return cls(ret)


def load(input: str, alternate: bool = False) -> Input:
    from utils import load_file_lines
    data = load_file_lines(input)
    return Input.parse(data, alternate)


def debug_print(map: Map):
    for iy in range(0, map.height):
        line = ""
        for ix in range(0, map.width):
            position = Vector(ix, iy)
            line += map[position]
        print(line + '\n')


def task(input: Input) -> int:
    position = Vector(0, 0)
    max = Vector(0, 0)
    min = Vector(0, 0)
    for instruction in input.instructions:
        position = instruction.apply(position)
        max = max.max_dim(position)
        min = min.min_dim(position)

    map = Map(max.x - min.x + 1, max.y - min.y + 1, '.')
    position = min.multiply(-1)
    for instruction in input.instructions:
        for it in instruction.walk(position):
            map[it] = instruction.direction.value
        position = instruction.apply(position)

    # debug_print(map)

    def find_next(iy: int, ix: int, interesting: list[str]) -> int:
        while ix < map.width:
            if map[Vector(ix, iy)] in interesting:
                break
            ix += 1
        return ix

    for iy in range(0, map.height):
        ix = 0
        while True:
            if (begin_ix := find_next(iy, ix, ['U', 'D'])) >= map.width:
                break
            begin_value = map[Vector(begin_ix, iy)]
            if (end_ix := find_next(iy, begin_ix, ['D' if begin_value == 'U' else 'D'])) >= map.width:
                break
            for i in range(begin_ix, end_ix + 1):
                map[Vector(i, iy)] = '#'
            ix = end_ix + 1


    # print("------------------------")
    # debug_print(map)

    ret = 0
    for iy in range(0, map.height):
        for ix in range(0, map.width):
            position = Vector(ix, iy)
            if map[position] != '.':
                ret += 1
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse_primary(self):
        input = load('task_example.txt')
        self.assertEqual(14, len(input.instructions))
        self.assertEqual(Direction.DOWN, input.instructions[1].direction)
        self.assertEqual(2, input.instructions[13].len)

    def test_parse_secondary(self):
        input = load('task_example.txt', True)
        self.assertEqual(14, len(input.instructions))
        self.assertEqual(Direction.RIGHT, input.instructions[0].direction)
        self.assertEqual(461937, input.instructions[0].len)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load('task_example.txt')
        self.assertEqual(62, task(input))

    def test_challenge(self):
        input = load("task_challenge.txt")
        self.assertEqual(35991, task(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load('task_example.txt', True)
        self.assertEqual(952408144115, task(input))

    def test_challenge(self):
        input = load("task_challenge.txt")
        self.assertEqual(-1, task(input))


if __name__ == '__main__':
    unittest.main()