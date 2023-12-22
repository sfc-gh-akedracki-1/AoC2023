import unittest
from copy import deepcopy
from dataclasses import dataclass
from enum import StrEnum, property
from typing import Self, Iterator, Optional, Tuple

from _distutils_hack import override

from utils import load_file_lines


@dataclass
class Part:
    values: dict[str, int]

    @classmethod
    def parse(cls, line: str) -> Self:
        parts = line.strip('{}').split(',')
        return cls(
            {k: int(v) for k, v in [it.split('=', maxsplit=1) for it in parts]}
        )

    @property
    def total(self) -> int:
        return sum(self.values.values())


@dataclass
class Predicate:
    min: int
    max: int

    @property
    def len(self) -> int:
        return self.max - self.min


@dataclass
class PredicateSet:
    predicates: dict[str: Predicate]
    target: str

    @classmethod
    def uniform(cls, keys: list[str], min: int, max: int, target: str) -> Self:
        return cls(
            {key: Predicate(min, max) for key in keys},
            target
        )


class Operator(StrEnum):
    LESS = '<'
    MORE = '>'

    def evaluate(self, a: int, b: int) -> bool:
        match self:
            case self.LESS:
                return a < b
            case self.MORE:
                return a > b
            case _:
                return False

    def match(self, predicate: Predicate, value: int) -> Tuple[Optional[Predicate], Optional[Predicate]]:
        match self:
            case self.LESS:
                if value <= predicate.min:
                    return None, predicate
                if value > predicate.max:
                    return predicate, None
                return Predicate(predicate.min, value - 1), Predicate(value, predicate.max)
            case self.MORE:
                if value >= predicate.max:
                    return None, predicate
                if value < predicate.min:
                    return predicate, None
                return Predicate(value + 1, predicate.max), Predicate(predicate.min, value)
            case _:
                return None, predicate

    @classmethod
    def parse(cls, input: str) -> Optional[Tuple[Self, str, str]]:
        for op in cls:
            if (inx := input.find(op)) == -1:
                continue
            return cls(op), input[0:inx], input[inx+1:]
        else:
            return None


class Step:
    def process(self, part: Part) -> Optional[str]:
        return None

    def match(self, predicate_set: PredicateSet) -> Tuple[Optional[PredicateSet], Optional[PredicateSet]]:
        return predicate_set, None

    @classmethod
    def parse(cls, input: str) -> Optional[Self]:
        return None


@dataclass
class FallbackStep(Step):
    fallback: str

    def process(self, part: Part) -> Optional[str]:
        return self.fallback

    def match(self, predicate_set: PredicateSet) -> Tuple[Optional[PredicateSet], Optional[PredicateSet]]:
        ret = deepcopy(predicate_set)
        ret.target = self.fallback
        return ret, None

    @classmethod
    def parse(cls, input: str) -> Optional[Self]:
        return cls(input)


@dataclass
class ConditionalStep(Step):
    key: str
    value: int
    operator: Operator
    target: str

    def process(self, part: Part) -> Optional[str]:
        if self.operator.evaluate(part.values[self.key], self.value):
            return self.target
        return None

    def match(self, predicate_set: PredicateSet) -> Tuple[Optional[PredicateSet], Optional[PredicateSet]]:
        predicate = predicate_set.predicates[self.key]
        matching, mismatching = self.operator.match(predicate, self.value)

        if matching is not None:
            matching_set = deepcopy(predicate_set)
            matching_set.target = self.target
            matching_set.predicates[self.key] = matching
        else:
            matching_set = None

        if mismatching is not None:
            mismatching_set = deepcopy(predicate_set)
            mismatching_set.predicates[self.key] = mismatching
        else:
            mismatching_set = None

        return matching_set, mismatching_set

    @classmethod
    def parse(cls, input: str) -> Optional[Self]:
        if len(parts := input.split(':', maxsplit=1)) != 2:
            return None
        target = parts[1]
        if (op_match := Operator.parse(parts[0])) is None:
            return None

        return cls(
            op_match[1],
            int(op_match[2]),
            op_match[0],
            target
        )


@dataclass
class Workflow:
    name: str
    steps: list[Step]

    @classmethod
    def parse(cls, line: str) -> Self:
        name, rest = line.split('{', maxsplit=1)
        step_parts = rest.split('}', maxsplit=1)[0].split(',')
        steps = []
        step_types = [
            ConditionalStep,
            FallbackStep
        ]
        for it in step_parts:
            for step_type in step_types:
                if (step := step_type.parse(it)) is None:
                    continue
                steps.append(step)
                break
            else:
                raise "Failed to parse step"

        return cls(
            name,
            steps
        )


@dataclass
class System:
    workflows: dict[str, Workflow]
    parts: list[Part]

    @classmethod
    def parse(cls, lines: Iterator[str]) -> Self:
        workflows = {}
        while (line := next(lines, None)) is not None and len(line := line.strip()) > 0:
            workflow = Workflow.parse(line)
            workflows[workflow.name] = workflow

        parts = []
        while (line := next(lines, None)) is not None and len(line := line.strip()) > 0:
            part = Part.parse(line)
            parts.append(part)

        return cls(
            workflows,
            parts
        )


def load(input: str) -> System:
    input = load_file_lines(input)
    return System.parse(input)


def task1(system: System) -> int:
    ret = 0

    def process(workflow: Workflow, part: Part) -> str:
        for step in workflow.steps:
            if (next_id := step.process(part)) is not None:
                return next_id

    for part in system.parts:
        workflow_id = 'in'
        while True:
            if workflow_id == 'A':
                ret += part.total
                break
            elif workflow_id == 'R':
                break
            else:
                workflow_id = process(system.workflows[workflow_id], part)

    return ret


def task2(system: System) -> int:
    ret = 0
    keys = ['x', 'm', 'a', 's']

    accepted: list[PredicateSet] = []
    queue: list[PredicateSet] = [PredicateSet.uniform(keys,  1, 4000, 'in')]

    while len(queue) > 0:
        it = queue.pop()
        if it.target == 'A':
            accepted.append(it)
            continue
        if it.target == 'R':
            continue

        workflow = system.workflows[it.target]
        for step in workflow.steps:
            matching, mismatching = step.match(it)

            if matching is not None:
                queue.append(matching)
            if mismatching is not None:
                it = mismatching
            else:
                break

    for it in accepted:
        accum = 1
        for key in keys:
            accum *= it.predicates[key].len + 1
        ret += accum

    return ret

# 167409079868000 <<
# 167474394229030

class InputTestCase(unittest.TestCase):
    def test_parse(self):
        system = load('task_example.txt')
        self.assertEqual(11, len(system.workflows))
        self.assertEqual(5, len(system.parts))

        self.assertEqual(3, len(system.workflows['px'].steps))
        self.assertIsInstance(system.workflows['px'].steps[0], ConditionalStep)
        self.assertIsInstance(system.workflows['px'].steps[-1], FallbackStep)

        self.assertEqual(787, system.parts[0].values['x'])
        self.assertEqual(1013, system.parts[4].values['s'])


class Task1TestCase(unittest.TestCase):
    def test_example(self):
        system = load('task_example.txt')
        self.assertEqual(19114, task1(system))

    def test_challenge(self):
        system = load("task_challenge.txt")
        self.assertEqual(350678, task1(system))


class Task2TestCase(unittest.TestCase):
    def test_example(self):
        system = load('task_example.txt')
        self.assertEqual(167409079868000, task2(system))

    def test_challenge(self):
        system = load("task_challenge.txt")
        self.assertEqual(124831893423809, task2(system))


if __name__ == '__main__':
    unittest.main()