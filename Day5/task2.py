import math
import unittest
from dataclasses import dataclass, field
from collections.abc import Sequence
from typing import Self, List, Iterator, Optional, Tuple

from utils import load_file, load_file_lines

INF = 2**48


@dataclass
class Span:
    begin: int
    end: int

    @property
    def length(self) -> int:
        return self.end - self.begin

    @classmethod
    def infinite(cls) -> Self:
        return cls(-INF, INF)


@dataclass
class DataSpan(Span):
    value: int = 0

    def __post_init__(self):
        if self.begin == self.end:
            print("arghhh")


@dataclass
class Layer:
    spans: list[DataSpan] = field(init=False, default_factory=list)

    def __post_init__(self):
        self.spans.append(DataSpan.infinite())

    def add_span(self, span: DataSpan):
        new_spans = []
        for it in self.spans:
            if it.begin >= span.end or it.end < span.begin:
                new_spans.append(it)
                continue

            if it.begin < span.begin:
                new_spans.append(DataSpan(it.begin, span.begin, it.value))
                new_spans.append(span)
                if it.end > span.end:
                    new_spans.append(DataSpan(span.end, it.end, it.value))
            else:
                if it.end > span.end:
                    new_spans.append(DataSpan(span.end, it.end, it.value))

        self.spans = new_spans

    def query(self, position: int) -> DataSpan:
        for span in self.spans:
            if span.begin <= position < span.end:
                return span

    def intersect(self, span: Span) -> list[DataSpan]:
        ret = []
        for it in self.spans:
            if it.begin >= span.end or it.end <= span.begin:
                continue
            if it.begin < span.begin:
                if it.end > span.end:
                    ret.append(DataSpan(span.begin, span.end, it.value))
                else:
                    ret.append(DataSpan(span.begin, it.end, it.value))
            else:
                if it.end > span.end:
                    ret.append(DataSpan(it.begin, span.end, it.value))
                else:
                    ret.append(DataSpan(it.begin, it.end, it.value))
        return ret

    @classmethod
    def parse(cls, input: Iterator[str]) -> Optional[Self]:
        header_line = next(input, None)
        if header_line is None:
            return None

        layer = Layer()
        while True:
            line = next(input, None)
            if line is None or line == '\n':
                break
            parts = [int(it) for it in line.split(' ')]

            layer.add_span(DataSpan(
                parts[1],
                parts[1] + parts[2],
                parts[0] - parts[1]
            ))
        return layer


@dataclass
class Almanac2:
    seeds: list[Span]
    layers: list[Layer]

    @classmethod
    def parse(cls, input: Iterator[str]) -> Self:
        seed_parts = next(input).split(":", maxsplit=1)[1].strip().split(' ')
        seeds = [
            Span(
                int(seed_parts[i*2]),
                int(seed_parts[i*2]) + int(seed_parts[i*2+1])
            )
            for i in range(0, len(seed_parts)//2)
        ]
        next(input) # empty line
        layers = []
        while True:
            layer = Layer.parse(input)
            if layer is None:
                break
            layers.append(layer)
        return cls(seeds, layers)


def task2(input: Iterator[str]) -> int:
    almanac = Almanac2.parse(input)
    ret = math.inf
    for sit in almanac.seeds:
        current_spans = [sit]
        for lit in almanac.layers:
            next_span = []
            for csit in current_spans:
                intersected = lit.intersect(csit)
                next_span.extend([Span(i.begin + i.value, i.end + i.value) for i in intersected])
            current_spans = next_span
        for csit in current_spans:
            if csit.begin < ret:
                ret = csit.begin
    return ret


class InputTestCase(unittest.TestCase):
    def test_parse_almanac2(self):
        lines = load_file_lines('task2_example.txt')
        almanac = Almanac2.parse(lines)
        self.assertListEqual([Span(79, 93), Span(55, 68)], almanac.seeds)
        self.assertEqual(7, len(almanac.layers))

    def test_layer(self):
        layer = Layer()
        self.assertEqual(DataSpan.infinite(), layer.query(5))
        self.assertEqual(DataSpan.infinite(), layer.query(15))

        layer.add_span(DataSpan(5, 15, 3))
        self.assertEqual(DataSpan(-INF, 5, 0), layer.query(2))
        self.assertEqual(DataSpan(15, INF, 0), layer.query(15))
        self.assertEqual(DataSpan(15, INF, 0), layer.query(16))
        self.assertEqual(DataSpan(5, 15, 3), layer.query(5))
        self.assertEqual(DataSpan(5, 15, 3), layer.query(6))
        self.assertEqual(DataSpan(5, 15, 3), layer.query(14))

        layer.add_span(DataSpan(10, 20, 2))
        self.assertEqual(DataSpan(-INF, 5, 0), layer.query(2))
        self.assertEqual(DataSpan(5, 10, 3), layer.query(5))
        self.assertEqual(DataSpan(10, 20, 2), layer.query(10))
        self.assertEqual(DataSpan(10, 20, 2), layer.query(19))
        self.assertEqual(DataSpan(20, INF, 0), layer.query(20))

        layer.add_span(DataSpan(12, 15, 5))
        self.assertEqual(DataSpan(-INF, 5, 0), layer.query(2))
        self.assertEqual(DataSpan(5, 10, 3), layer.query(5))
        self.assertEqual(DataSpan(10, 12, 2), layer.query(10))
        self.assertEqual(DataSpan(12, 15, 5), layer.query(12))
        self.assertEqual(DataSpan(15, 20, 2), layer.query(15))
        self.assertEqual(DataSpan(20, INF, 0), layer.query(20))

        self.assertListEqual(
            [
                DataSpan(8, 10, 3),
                DataSpan(10, 12, 2),
                DataSpan(12, 15, 5),
            ],
            layer.intersect(Span(8, 15))
        )

        self.assertListEqual(
            [
                DataSpan(1, 5, 0),
                DataSpan(5, 10, 3),
                DataSpan(10, 12, 2),
                DataSpan(12, 15, 5),
            ],
            layer.intersect(Span(1, 15))
        )


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task2_example.txt')
        self.assertEqual(46, task2(input))

    def test_challenge(self):
        input = load_file_lines("task2_challenge.txt")
        self.assertEqual(2008785, task2(input))


if __name__ == '__main__':
    unittest.main()