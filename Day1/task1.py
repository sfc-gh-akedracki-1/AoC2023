import unittest
from typing import Sequence

from Day1.utils import load_file


def extract_digits(line: str) -> Sequence[int]:
    valid_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for ch in line:
        if ch in valid_digits:
            yield int(ch)


def task1(input: str) -> int:
    sum = 0
    for line in input.splitlines():
        digits = list(extract_digits(line))
        sum += digits[0]*10 + digits[-1]
    return sum


class Task1TestCase(unittest.TestCase):
    def test_extract_digits(self):
        cases = {
            "pqr3stu8vwx": [3, 8],
            "a1b2c3d4e5f": [1, 2, 3, 4, 5],
            "treb7uchet": [7]
        }
        for input, expected in cases.items():
            output = list(extract_digits(input))
            self.assertEqual(expected, output)

    def test_example(self):
        input = load_file('task1_testinput.txt')
        expected = 142
        output = task1(input)
        self.assertEqual(expected, output)

    def test_challenge(self):
        data = load_file("task1_input.txt")
        output = task1(data)
        self.assertEqual(54159, output)


if __name__ == '__main__':
    unittest.main()