import unittest
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Sequence, Self, List, Optional, Tuple

from utils import load_file


class Direction(IntEnum):
    NONE = 0
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    def __str__(self):
        match self:
            case Direction.WEST:
                return "<"
            case Direction.EAST:
                return ">"
            case Direction.SOUTH:
                return "V"
            case Direction.NORTH:
                return "A"
            case _:
                return "0"

class Field(IntEnum):
    GROUND = 0
    START = 1
    NORTH_SOUTH = 2
    WEST_EAST = 3
    NORTH_EAST = 4
    NORTH_WEST = 5
    SOUTH_EAST = 6
    SOUTH_WEST = 7

    @classmethod
    def from_symbol(cls, str) -> Self:
        match str:
            case '.':
                return cls.GROUND
            case 'S':
                return cls.START
            case '|':
                return cls.NORTH_SOUTH
            case '-':
                return cls.WEST_EAST
            case 'L':
                return cls.NORTH_EAST
            case 'J':
                return cls.NORTH_WEST
            case 'F':
                return cls.SOUTH_EAST
            case '7':
                return cls.SOUTH_WEST

    def next(self, direction: Direction) -> Direction:
        match self:
            case Field.GROUND:
                return Direction.NONE
            case Field.START:
                return Direction.NONE
            case Field.NORTH_SOUTH:
                match direction:
                    case Direction.SOUTH:
                        return Direction.SOUTH
                    case Direction.NORTH:
                        return Direction.NORTH
                    case _:
                        return Direction.NONE
            case Field.WEST_EAST:
                match direction:
                    case Direction.WEST:
                        return Direction.WEST
                    case Direction.EAST:
                        return Direction.EAST
                    case _:
                        return Direction.NONE
            case Field.NORTH_EAST:
                match direction:
                    case Direction.SOUTH:
                        return Direction.EAST
                    case Direction.WEST:
                        return Direction.NORTH
                    case _:
                        return Direction.NONE
            case Field.NORTH_WEST:
                match direction:
                    case Direction.SOUTH:
                        return Direction.WEST
                    case Direction.EAST:
                        return Direction.NORTH
                    case _:
                        return Direction.NONE
            case Field.SOUTH_EAST:
                match direction:
                    case Direction.NORTH:
                        return Direction.EAST
                    case Direction.WEST:
                        return Direction.SOUTH
                    case _:
                        return Direction.NONE
            case Field.SOUTH_WEST:
                match direction:
                    case Direction.NORTH:
                        return Direction.WEST
                    case Direction.EAST:
                        return Direction.SOUTH
                    case _:
                        return Direction.NONE
            case _:
                return Direction.NONE


@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int

    def next(self, direction: Direction) -> Self:
        match direction:
            case Direction.NORTH:
                return Position(self.x, self.y - 1)
            case Direction.SOUTH:
                return Position(self.x, self.y + 1)
            case Direction.WEST:
                return Position(self.x - 1, self.y)
            case Direction.EAST:
                return Position(self.x + 1, self.y)


@dataclass
class Step:
    position: Position
    direction: Direction
    distance: int


@dataclass
class Map:
    fields: list[list[Field]]
    width: int = field(init=False)
    height: int = field(init=False)

    def __post_init__(self):
        self.height = len(self.fields)
        self.width = len(self.fields[0] if self.height > 0 else 0)

    @classmethod
    def parse(cls, input: str) -> Self:
        lines = input.splitlines()

        return cls(
            [[Field.from_symbol(symbol) for symbol in line] for line in lines]
        )

    def get(self, position: Position) -> Field:
        if 0 <= position.x < self.width and 0 <= position.y < self.height:
            return self.fields[position.y][position.x]
        return Field.GROUND

    def find_start(self) -> Position:
        for iy in range(0, len(self.fields)):
            for ix in range(0, len(self.fields[iy])):
                position = Position(ix, iy)
                if self.get(position) == Field.START:
                    return position
        raise "Erghhh"


def task1(input: str) -> int:
    map = Map.parse(input)
    start_position = map.find_start()
    steps = [
        Step(start_position, direction, 0) for direction in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
    ]
    visited: set[Position] = set()
    while len(steps) > 0:
        next_steps = []
        for step in steps:
            next_position = step.position.next(step.direction)
            if next_position in visited:
                return step.distance + 1
            field = map.get(next_position)
            next_direction = field.next(step.direction)
            if next_direction == Direction.NONE:
                continue
            next_steps.append(Step(next_position, next_direction, step.distance + 1))
            visited.add(next_position)
        steps = next_steps
    return 0


def task2(input: str) -> int:
    map = Map.parse(input)
    start_position = map.find_start()
    steps = [
        Step(start_position, direction, 0) for direction in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
    ]
    direction_map = [[Direction.NONE for _ in range(0, map.width)] for _ in range(0, map.height)]
    loop_completed = False
    while loop_completed is False:
        for step in steps:
            direction_map[step.position.y][step.position.x] = step.direction
            next_position = step.position.next(step.direction)
            if next_position == start_position:
                loop_completed = True
                break
            field = map.get(next_position)
            next_direction = field.next(step.direction)
            if next_direction is Direction.NONE:
                continue
            next_step = Step(next_position, next_direction, step.distance + 1)
            steps = [next_step]
            break

    ret = 0

    flow_map = [['0' for _ in range(0, map.width)] for _ in range(0, map.height)]

    for iy in range(0, map.height):
        inside = False
        accum = 0
        ix = 0
        while ix < map.width:
            direction = direction_map[iy][ix]
            if direction == Direction.NONE:
                # no change of situation
                if inside:
                    accum += 1
                    flow_map[iy][ix] = 'X'
                ix += 1
            else:
                # begin of pipe -> find end and flip state
                while ix < map.width - 1:
                    ix += 1
                    next_direction = direction_map[iy][ix]
                    if next_direction in [Direction.WEST, Direction.EAST]:
                        continue
                    if inside:
                        ret += accum
                        accum = 0
                    inside = not inside
                    break
                ix += 1
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file('task1_example.txt')
        map = Map.parse(input)
        self.assertEqual(Field.WEST_EAST, map.get(Position(0, 0)))
        self.assertEqual(Field.START, map.get(Position(1, 1)))
        self.assertEqual(Field.NORTH_EAST, map.get(Position(0, 2)))
        self.assertEqual(Field.NORTH_EAST, map.get(Position(0, 2)))


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(4, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(6897, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example1(self):
        input = load_file('task2_example1.txt')
        self.assertEqual(4, task2(input))

    def test_example2(self):
        input = load_file('task2_example2.txt')
        self.assertEqual(4, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()