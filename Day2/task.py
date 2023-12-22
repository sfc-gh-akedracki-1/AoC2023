import unittest
from typing import Sequence, Self, Tuple
from dataclasses import dataclass

from Day2.utils import load_file


@dataclass
class Draw:
    red: int
    green: int
    blue: int

    @classmethod
    def parse(cls, chunk: str) -> Self:
        r, g, b = 0, 0, 0
        for color_chunk in chunk.split(','):
            count, color = color_chunk.strip().split(' ')
            match color:
                case 'red':
                    r = int(count)
                case 'green':
                    g = int(count)
                case 'blue':
                    b = int(count)

        return Draw(r, g, b)


@dataclass
class Game:
    number: int
    draws: Sequence[Draw]

    @classmethod
    def parse(cls, line: str) -> Self:
        game_segment, draws_segment = line.split(':', maxsplit=1)
        number = int(game_segment.replace("Game", "").strip())

        return cls(
            number=number,
            draws=[Draw.parse(chunk.strip()) for chunk in draws_segment.split(';')]
        )

    def validate(self, max_red: int, max_green: int, max_blue: int) -> bool:
        for draw in self.draws:
            if draw.red > max_red or draw.green > max_green or draw.blue > max_blue:
                return False
        return True

    def required(self) -> Tuple[int, int, int]:
        r, b, g = 0, 0, 0
        for draw in self.draws:
            r = max(r, draw.red)
            g = max(g, draw.green)
            b = max(b, draw.blue)

        return r, g, b

    def power(self) -> int:
        r, g, b = self.required()
        return r * g * b


def task1(input: str) -> int:
    max_red, max_green, max_blue = 12, 13, 14
    games = [Game.parse(line) for line in input.splitlines()]
    ret = 0
    for game in games:
        if game.validate(max_red, max_green, max_blue):
            ret += game.number
    return ret


def task2(input: str) -> int:
    games = [Game.parse(line) for line in input.splitlines()]
    ret = 0
    for game in games:
        ret += game.power()
    return ret


class ParseGameTestCase(unittest.TestCase):
    def test_parse_game(self):
        self.assertEqual(
            Game(
                number=2,
                draws=[
                    Draw(4, 0, 3),
                    Draw(1, 2, 6),
                    Draw(0, 2, 0)
                ]
            ),
            Game.parse("Game 2: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
        )


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task1_example.txt')
        self.assertEqual(8, task1(input))

    def test_challenge(self):
        input = load_file("task1_challenge.txt")
        self.assertEqual(2207, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(2286, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(62241, task2(input))


if __name__ == '__main__':
    unittest.main()