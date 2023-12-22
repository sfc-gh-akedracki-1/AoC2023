import unittest
from dataclasses import dataclass
from typing import Sequence, Self, List, Iterator


@dataclass
class Input:

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        pass


def load(input: str) -> Input:
    from utils import load_file_lines
    data = load_file_lines(input)
    return Input.parse(data)


def task1(input: Input) -> int:
    ret = 0
    return ret


def task2(input: Input) -> int:
    ret = 0
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        pass


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load('task_example.txt')
        self.assertEqual(-1, task1(input))

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