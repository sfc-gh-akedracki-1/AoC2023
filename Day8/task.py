import unittest
from dataclasses import dataclass
from typing import Sequence, Self, List, Iterator, Tuple, Callable

from utils import load_file, load_file_lines


@dataclass
class Node:
    id: str
    left: str
    right: str

    @classmethod
    def parse(cls, input: str) -> Self:
        # AAA = (BBB, CCC)
        id, nodes = [it.strip(' \n()') for it in input.split('=', maxsplit=1)]
        nodes = [it.strip() for it in nodes.split(', ', maxsplit=1)]
        return cls(
            id,
            nodes[0],
            nodes[1]
        )


@dataclass
class Map:
    steps: str
    nodes: dict[str, Node]

    @classmethod
    def parse(cls, input: Iterator[str]) -> Self:
        steps = next(input).strip()
        next(input) # empty line
        nodes = []
        while True:
            line = next(input, None)
            if line is None:
                break
            nodes.append(Node.parse(line))
        return cls(steps, {it.id: it for it in nodes})

    def run(self, node: Node, start_at : int, end_test: Callable[[str], bool]) -> Tuple[int, Node]:
        steps_taken = 0
        step_index = start_at % len(self.steps)
        it = node
        while True:
            if end_test(it.id):
                return steps_taken, it
            step = self.steps[step_index]
            step_index = (step_index + 1) % len(self.steps)
            steps_taken += 1

            if step == 'L':
                it = self.nodes[it.left]
            else:
                it = self.nodes[it.right]


def task1(input: Iterator[str]) -> int:
    ret = 0
    map = Map.parse(input)
    return map.run(map.nodes['AAA'], 0, lambda id: id == 'ZZZ')[0]


def task2(input: Iterator[str]) -> int:
    map = Map.parse(input)
    start_nodes = [node for node in map.nodes.values() if node.id[2] == 'A']
    cycles = []
    for node in start_nodes:
        steps_taken, end_node = map.run(node, 0, lambda id: id[2] == 'Z')
        cycles.append(steps_taken)

    accum = cycles.copy()
    while True:
        smallest_value = 2**48
        smallest_inx = 0
        for i in range(0, len(accum)):
            if accum[i] < smallest_value:
                smallest_inx = i
                smallest_value = accum[i]
        for i in range(0, len(accum)):
            if accum[i] != smallest_value:
                break
        else:
            return smallest_value

        accum[smallest_inx] = smallest_value + cycles[smallest_inx]


class InputTestCase(unittest.TestCase):
    def test_parse_node(self):
        node = Node.parse('AAA = (BBB, CCC)\n')
        self.assertEqual('AAA', node.id)
        self.assertEqual('BBB', node.left)
        self.assertEqual('CCC', node.right)


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task1_example.txt')
        self.assertEqual(6, task1(input))

    def test_challenge(self):
        input = load_file_lines("task1_challenge.txt")
        self.assertEqual(12737, task1(input))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        input = load_file_lines('task2_example.txt')
        self.assertEqual(6, task2(input))

    def test_challenge(self):
        input = load_file_lines("task2_challenge.txt")
        self.assertEqual(-1, task2(input))


if __name__ == '__main__':
    unittest.main()