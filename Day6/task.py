import math
import unittest
from dataclasses import dataclass
from typing import Sequence, Self, List


from utils import load_file

@dataclass
class Run:
    time: int
    distance: int

    @property
    def solve(self) -> list[int]:
        delta = self.time * self.time - 4 * self.distance
        if delta <= 0:
            raise "non-positive delta case"

        def ceil_top(f : float) -> int:
            i = int(math.ceil(f))
            if i == f:
                i += 1
            return i

        def floor_bottom(f: float) -> int:
            i = int(math.floor(f))
            if i == f:
                i -= 1
            return i

        x1 = (self.time - math.sqrt(delta))/2
        x2 = (self.time + math.sqrt(delta))/2
        return [ceil_top(x1), floor_bottom(x2)]

@dataclass
class Puzzle:
    runs: list[Run]

    @classmethod
    def parse(cls, input: str) -> Self:
        time_line, distance_line, *_ = input.splitlines()
        times = [int(it.strip()) for it in time_line.split(':', maxsplit=1)[1].split(' ') if it != '']
        distances = [int(it.strip()) for it in distance_line.split(':', maxsplit=1)[1].split(' ') if it != '']

        return Puzzle(
            [Run(times[i], distances[i]) for i in range(0, len(times))]
        )

    @classmethod
    def parse_kerning(cls, input: str) -> Self:
        time_line, distance_line, *_ = input.splitlines()
        time = int(time_line.split(':', maxsplit=1)[1].replace(' ', '').strip())
        distance = int(distance_line.split(':', maxsplit=1)[1].replace(' ', '').strip())

        return Puzzle([Run(time, distance)])

def task1(input: str) -> int:
    ret = 1
    puzzle = Puzzle.parse(input)
    for run in puzzle.runs:
        mint, maxt = run.solve
        ret *= maxt - mint + 1
    return ret


def task2(input: str) -> int:
    ret = 1
    puzzle = Puzzle.parse_kerning(input)
    for run in puzzle.runs:
        mint, maxt = run.solve
        ret *= maxt - mint + 1
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file('task1_example.txt')
        puzzle = Puzzle.parse(input)
        self.assertEqual(3, len(puzzle.runs))

    def test_parse_kerning(self):
        input = load_file('task2_example.txt')
        puzzle = Puzzle.parse_kerning(input)
        self.assertEqual(1, len(puzzle.runs))
        self.assertEqual(Run(71530, 940200), puzzle.runs[0])

    def test_run_min_max(self):
        self.assertEqual([2, 5], Run(7, 9).solve)
        self.assertEqual([11, 19], Run(30, 200).solve)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(288, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(211904, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(71503, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()