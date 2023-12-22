import functools
import unittest
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Sequence, Self, TypeVar
from enum import IntEnum


from utils import load_file


class Type(IntEnum):
    FIVE = 7
    FOUR = 6
    FULL_HOUSE = 5
    THREE = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


T = TypeVar('T')


def histogram(input: Sequence[T]) -> dict[T, int]:
    ret = defaultdict(lambda: 0)
    for s in input:
        ret[s] += 1
    return dict(ret)


@dataclass
class Hand:
    cards: str
    bid: int
    type: Type = field(init=False)

    def __post_init__(self):
        card_histogram = histogram(self.cards)
        joker_count = card_histogram.get('J', 0)
        if joker_count > 0:
            del card_histogram['J']
        repeat_histogram = histogram(card_histogram.values())
        if repeat_histogram.get(5, 0) == 1:
            self.type = Type.FIVE
        elif repeat_histogram.get(4, 0) == 1:
            match joker_count:
                case 1:
                    self.type = Type.FIVE
                case 0:
                    self.type = Type.FOUR
        elif repeat_histogram.get(3, 0) == 1:
            if repeat_histogram.get(2, 0) == 1:
                self.type = Type.FULL_HOUSE
            else:
                match joker_count:
                    case 2:
                        self.type = Type.FIVE
                    case 1:
                        self.type = Type.FOUR
                    case 0:
                        self.type = Type.THREE
        elif repeat_histogram.get(2, 0) == 2:
            match joker_count:
                case 1:
                    self.type = Type.FULL_HOUSE
                case 0:
                    self.type = Type.TWO_PAIR
        elif repeat_histogram.get(2, 0) == 1:
            match joker_count:
                case 3:
                    self.type = Type.FIVE
                case 2:
                    self.type = Type.FOUR
                case 1:
                    self.type = Type.THREE
                case 0:
                    self.type = Type.ONE_PAIR
        else:
            match joker_count:
                case 5:
                    self.type = Type.FIVE
                case 4:
                    self.type = Type.FIVE
                case 3:
                    self.type = Type.FOUR
                case 2:
                    self.type = Type.THREE
                case 1:
                    self.type = Type.ONE_PAIR
                case 0:
                    self.type = Type.HIGH_CARD

    @classmethod
    def parse(cls, input: str) -> Self:
        cards, bid = input.strip().split(' ')
        return cls(cards, int(bid))

    @classmethod
    def parse_multiple(cls, input: str) -> list[Self]:
        return [cls.parse(line) for line in input.splitlines()]


def compare_hands(a: Hand, b: Hand) -> int:
    def card_rank(card: str) -> int:
        return "J23456789TQKA".index(card)

    if a.type != b.type:
        return a.type.value - b.type.value
    for i in range(0, len(a.cards)):
        if a.cards[i] != b.cards[i]:
            return card_rank(a.cards[i]) - card_rank(b.cards[i])
    return 0


def task2(input: str) -> int:
    ret = 0
    hands = Hand.parse_multiple(input)
    hands.sort(key=functools.cmp_to_key(compare_hands))
    for i in range(0, len(hands)):
        ret += hands[i].bid * (i + 1)
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse_card(self):
        self.assertEqual("32T3K", Hand.parse("32T3K 765").cards)
        self.assertEqual(765, Hand.parse("32T3K 765").bid)
        self.assertEqual(Type.HIGH_CARD, Hand.parse("32567 765").type)
        self.assertEqual(Type.ONE_PAIR, Hand.parse("32T3K 765").type)
        self.assertEqual(Type.TWO_PAIR, Hand.parse("KK677 765").type)
        self.assertEqual(Type.THREE, Hand.parse("T55A5 765").type)
        self.assertEqual(Type.FULL_HOUSE, Hand.parse("KKQQK 765").type)
        self.assertEqual(Type.FOUR, Hand.parse("AQAAA 765").type)
        self.assertEqual(Type.FIVE, Hand.parse("AAAAA 765").type)

        self.assertEqual(Type.ONE_PAIR, Hand.parse("3256J 765").type)
        self.assertEqual(Type.FOUR, Hand.parse("KTJJT 765").type)
        self.assertEqual(Type.FOUR, Hand.parse("QQQJA 765").type)


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file('task2_example.txt')
        self.assertEqual(5905, task2(input))

    def test_challenge(self):
        input = load_file("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()