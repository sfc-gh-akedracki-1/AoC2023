from dataclasses import dataclass, field
from typing import Iterator, Self


def load_file(path: str) -> str:
    with open(path, 'r') as fp:
        return fp.read()


def load_file_lines(path: str) -> Iterator[str]:
    with open(path, 'r') as fp:
        return iter(fp.readlines())


@dataclass(frozen=True)
class Vector:
    x: int
    y: int

    def max_dim(self, second: Self) -> Self:
        return Vector(
            max(self.x, second.x),
            max(self.y, second.y)
        )

    def min_dim(self, second: Self) -> Self:
        return Vector(
            min(self.x, second.x),
            min(self.y, second.y)
        )

    def multiply(self, by: int) -> Self:
        return Vector(
            self.x * by,
            self.y * by
        )


@dataclass
class Map[T]:
    width: int
    height: int
    fallback: T
    fields: list[list[T]] = field(init=False)

    def __post_init__(self):
        self.fields = [
            [self.fallback for _ in range(0, self.width)]
            for _ in range(0, self.height)
        ]

    def __setitem__(self, key: Vector, value: T):
        if 0 <= key.x < self.width and 0 <= key.y < self.height:
            self.fields[key.y][key.x] = value
        else:
            raise IndexError()

    def __getitem__(self, key: Vector) -> T:
        if 0 <= key.x < self.width and 0 <= key.y < self.height:
            return self.fields[key.y][key.x]
        return self.fallback


def hexstr_to_int(input: str) -> int:
    value = 0
    for i in input:
        value *= 16
        ch = ord(i)
        if ord('0') <= ch <= ord('9'):
            value += ch - ord('0')
        elif ord('a') <= ch <= ord('f'):
            value += ch - ord('a') + 10
        elif ord('A') <= ch <= ord('F'):
            value += ch - ord('A') + 10
        else:
            raise Exception(f"Invalid character in context of hex string: {i}")
    return value