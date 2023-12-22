import unittest
from dataclasses import dataclass
from typing import Sequence, Self, List, Tuple

from utils import load_file

def is_all_zeros(input : list[int]) -> bool:
    for it in input:
        if it != 0:
            return False
    return True


def reduce(line: str) -> Tuple[list[int], list[int]]:
    readings = [int(it.strip()) for it in line.split(' ') if it != ' ']
    endings = []
    beginnings = []
    while True:
        if is_all_zeros(readings):
            break
        beginnings.append(readings[0])
        endings.append(readings[-1])
        readings = [readings[i] - readings[i-1] for i in range(1, len(readings))]
    return beginnings, endings


def task1(input: str) -> int:
    ret = 0
    lines = input.splitlines()
    for line in lines:
        _, endings = reduce(line)
        ret += sum(endings)
    return ret


def task2(input: str) -> int:
    ret = 0
    lines = input.splitlines()
    for line in lines:
        beginnings, _ = reduce(line)
        accum = 0
        beginnings.reverse()
        for it in beginnings:
            accum = it - accum
        ret += accum
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        pass


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(114, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(1853145119, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(2, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(923, task2(input))


if __name__ == '__main__':
    unittest.main()