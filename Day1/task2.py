import unittest
from typing import Sequence

from Day1.utils import load_file

VALID_DIGITS = {
    '1': 1,
    'one': 1,
    '2': 2,
    'two': 2,
    '3': 3,
    'three': 3,
    '4': 4,
    'four': 4,
    '5': 5,
    'five': 5,
    '6': 6,
    'six': 6,
    '7': 7,
    'seven': 7,
    '8': 8,
    'eight': 8,
    '9': 9,
    'nine': 9
}


def extract_first_digit(line: str) -> int:
    inx = 0
    while inx < len(line):
        for key in VALID_DIGITS:
            if line.startswith(key, inx):
                return VALID_DIGITS[key]
        else:
            inx += 1


def extract_last_digit(line: str) -> int:
    inx = len(line)
    while inx > 0:
        for key in VALID_DIGITS:
            if line.endswith(key, inx - len(key), inx):
                return VALID_DIGITS[key]
        else:
            inx -= 1


def task2(input: str) -> int:
    sum = 0
    for line in input.splitlines():
        sum += extract_first_digit(line) * 10 + extract_last_digit(line)
    return sum


class Task2TestCase(unittest.TestCase):
    def test_extract_first_digit(self):
        cases = {
            "two1nine": 2,
            "xtwone3four": 2,
            "7pqrstsixteen": 7,
        }
        for input, expected in cases.items():
            output = extract_first_digit(input)
            self.assertEqual(expected, output)

    def test_extract_last_digit(self):
        cases = {
            "two1nine": 9,
            "xtwone3x": 3,
            "7pqrstsixteen": 6,
            "5fiveonefour8lhqmltwoeighttwo": 2
        }
        for input, expected in cases.items():
            output = extract_last_digit(input)
            self.assertEqual(expected, output)

    def test_example(self):
        input = load_file('task2_testinput.txt')
        expected = 281
        output = task2(input)
        self.assertEqual(expected, output)

    def test_challenge(self):
        data = load_file("task2_input.txt")
        output = task2(data)
        self.assertEqual(0, output)


if __name__ == '__main__':
    unittest.main()