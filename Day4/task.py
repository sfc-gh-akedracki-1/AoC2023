import unittest
from dataclasses import dataclass, field
from typing import Sequence, Self, List


from utils import load_file


@dataclass
class Card:
    number: int
    winning_numbers: List[int]
    your_numbers: List[int]
    matches: int = field(init=False)
    score: int = field(init=False)

    def __post_init__(self):
        ret = 0
        for winning in self.winning_numbers:
            if winning in self.your_numbers:
                ret += 1
        self.matches = ret
        if ret == 0:
            self.score = 0
        else:
            self.score = 2**(ret - 1)

    @classmethod
    def load(cls, line: str) -> Self:
        id_part, numbers_part = line.split(':', maxsplit=1)
        winning_part, your_part = numbers_part.split('|', maxsplit=1)

        return Card(
            number=int(id_part.split(' ', maxsplit=1)[1].strip()),
            winning_numbers=[int(it.strip()) for it in winning_part.strip().split(' ') if len(it) > 0],
            your_numbers=[int(it.strip()) for it in your_part.strip().split(' ') if len(it) > 0]
        )

    @classmethod
    def load_many(cls, input: str) -> List[Self]:
        lines = input.splitlines()
        return [cls.load(line) for line in lines]


def task1(input: str) -> int:
    cards = Card.load_many(input)
    ret = 0
    for card in cards:
        ret += card.score
    return ret


def task2(input: str) -> int:
    ret = 0
    cards = Card.load_many(input)
    multiples = {it: 1 for it in range(1, len(cards) + 1)}
    for card in cards:
        for i in range(0, card.matches):
            key = card.number + i + 1
            if key not in multiples:
                break
            multiples[key] = multiples[key] + multiples[card.number]
    return sum(multiples.values())


class InputTestCase(unittest.TestCase):
    def test_parse(self):
        input = load_file('task1_example.txt')
        cards = Card.load_many(input)
        self.assertEqual(1, cards[0].number)
        self.assertListEqual([41, 48, 83, 86, 17], cards[0].winning_numbers)
        self.assertListEqual([83, 86, 6, 31, 17, 9, 48, 53], cards[0].your_numbers)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(13, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(28750, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(30, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(10212704, task2(input))


if __name__ == '__main__':
    unittest.main()