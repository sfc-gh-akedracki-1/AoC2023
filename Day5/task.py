import math
import unittest
from dataclasses import dataclass
from collections.abc import Sequence
from typing import Self, List, Iterator, Optional, Tuple

from utils import load_file, load_file_lines


@dataclass
class ValueRange:
    begin: int
    length: int
    level: int = 0

    @property
    def end(self) -> int:
        return self.begin + self.length

@dataclass
class MappingRange:
    source: int
    target: int
    length: int

    @classmethod
    def parse(cls, input: str) -> Self:
        parts = input.split(' ')
        return cls(
            int(parts[1]),
            int(parts[0]),
            int(parts[2])
        )

    @property
    def begin(self) -> int:
        return self.source

    @property
    def end(self) -> int:
        return self.source + self.length

    def map_range(self, value_range: ValueRange) -> List[ValueRange]:
        if value_range.end < self.begin:
            return [value_range]
        if value_range.begin > self.end:
            return [value_range]
        if value_range.begin < self.begin:
            if value_range.end <= self.end:
                return [
                    ValueRange(
                        value_range.begin,
                        self.begin - value_range.begin,
                        value_range.level
                    ),
                    ValueRange(
                        self.target,
                        value_range.end - self.begin,
                        value_range.level + 1
                    )
                ]
            else:
                return [
                    ValueRange(
                        value_range.begin,
                        self.begin - value_range.begin,
                        value_range.level
                    ),
                    ValueRange(
                        self.target,
                        self.length,
                        value_range.level + 1
                    ),
                    ValueRange(
                        self.end,
                        value_range.end - self.end,
                        value_range.level
                    )
                ]
        else:
            if value_range.end <= self.end:
                return [
                    ValueRange(
                        self.target + value_range.begin - self.begin,
                        value_range.length,
                        value_range.level + 1
                    )
                ]
            else:
                return [
                    ValueRange(
                        self.target + value_range.begin - self.begin,
                        self.end - value_range.begin,
                        value_range.level + 1
                    ),
                    ValueRange(
                        self.end,
                        value_range.end - self.end,
                        value_range.level
                    )
                ]


@dataclass
class Mapping:
    source: str
    target: str
    ranges: List[MappingRange]

    @classmethod
    def parse(cls, input: Iterator[str]) -> Optional[Self]:
        header_line = next(input, None)
        if header_line is None:
            return None
        source, _, target = header_line.split(' ', maxsplit=1)[0].split('-')
        ranges = []
        while True:
            line = next(input, None)
            if line is None or line == '\n':
                break
            ranges.append(MappingRange.parse(line))
        return Mapping(
            source,
            target,
            ranges
        )

    def map(self, input: int) -> int:
        for it in self.ranges:
            if it.source <= input < it.source + it.length:
                return input - it.source + it.target
        return input

    def map_range(self, input: ValueRange) -> List[ValueRange]:
        ret = []
        vit = input
        for it in self.ranges:
            pass
        return []


@dataclass
class Almanac:
    seeds: List[int]
    mappings: List[Mapping]

    @classmethod
    def parse(cls, input: Iterator[str]) -> Self:
        seed_part = next(input).split(":", maxsplit=1)[1].strip()
        seeds = [int(it.strip()) for it in seed_part.split(' ')]
        next(input) # empty line
        mappings = []
        while True:
            mapping = Mapping.parse(input)
            if mapping is None:
                break
            mappings.append(mapping)
        return cls(seeds, mappings)


def task1(input: Iterator[str]) -> int:
    almanac = Almanac.parse(input)
    ret = math.inf
    for seed in almanac.seeds:
        it = seed
        for mapping in almanac.mappings:
            it = mapping.map(it)
        if it < ret:
            ret = it
    return ret


def task2(input: Iterator[str]) -> int:
    almanac = Almanac.parse(input)
    ret = math.inf
    for i in range(0, len(almanac.seeds)//2):
        start = almanac.seeds[i*2]
        length = almanac.seeds[i*2+1]
        current_layer = [ValueRange(start, length, 1)]
        for mapping in almanac.mappings:
            next_layer = []
            for value in current_layer:
                next_layer.extend(mapping.map_range(value))
            current_layer = next_layer
        for value in current_layer:
            if value.begin < ret:
                ret = value.begin
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse_range(self):
        self.assertEqual(
            MappingRange(53, 49, 8),
            MappingRange.parse("49 53 8\n")
        )

    def test_parse_mapping(self):
        self.assertEqual(
            Mapping(
                'water',
                'light',
                [
                    MappingRange(18, 88, 7),
                    MappingRange(25, 18, 70)
                ]
            ),
            Mapping.parse(iter([
                'water-to-light map:\n',
                '88 18 7\n',
                '18 25 70\n',
                '\n'
            ]))
        )

    def test_parse_mapping_empty(self):
        self.assertIs(
            None,
            Mapping.parse(iter([]))
        )

    def test_parse_almanac(self):
        lines = load_file_lines('task1_example.txt')
        almanac = Almanac.parse(lines)
        self.assertListEqual([79, 14, 55, 13], almanac.seeds)
        self.assertEqual(7, len(almanac.mappings))

    def test_mapping(self):
        mapping = Mapping.parse(iter([
            'water-to-light map:\n',
            '88 18 7\n',
            '18 25 70\n',
            '\n'
        ]))

        self.assertEqual(88, mapping.map(18))
        self.assertEqual(94, mapping.map(24))
        self.assertEqual(18, mapping.map(25))
        self.assertEqual(87, mapping.map(94))
        self.assertEqual(5, mapping.map(5))
        self.assertEqual(95, mapping.map(95))

    def test_mapping_single_range_1(self):
        mapping_range = MappingRange(10, 40, 5)
        self.assertEqual(
            [
                ValueRange(5, 3)
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(5, 3))
        )

    def test_mapping_single_range_2(self):
        self.assertEqual(
            [
                ValueRange(5, 5),
                ValueRange(40, 2, 1)
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(5, 7))
        )

    def test_mapping_single_range_3(self):
        self.assertEqual(
            [
                ValueRange(5, 5),
                ValueRange(40, 5, 1),
                ValueRange(15, 5),
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(5, 15))
        )

    def test_mapping_single_range_4(self):
        self.assertEqual(
            [
                ValueRange(41, 3, 1),
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(11, 3))
        )

    def test_mapping_single_range_5(self):
        self.assertEqual(
            [
                ValueRange(42, 3, 1),
                ValueRange(15, 5)
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(12, 8))
        )

    def test_mapping_single_range_6(self):
        self.assertEqual(
            [
                ValueRange(16, 4)
            ],
            MappingRange(10, 40, 5).map_range(ValueRange(16, 4))
        )


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task1_example.txt')
        self.assertEqual(35, task1(input))

    def test_challenge(self):
        input = load_file_lines("task1_challenge.txt")
        self.assertEqual(88151870, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task2_example.txt')
        self.assertEqual(46, task2(input))

    def test_challenge(self):
        input = load_file_lines("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()