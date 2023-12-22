from dataclasses import dataclass, field
from typing import Sequence, Iterator, List, Self


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

    def __getitem__(self, key: Vector) -> T:
        if 0 <= key.x < self.width and 0 <= key.y < self.height:
            return self.fields[key.y][key.x]
        return self.fallback
