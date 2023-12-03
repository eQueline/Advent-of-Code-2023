from __future__ import annotations
from typing import Sequence
from dataclasses import dataclass
import re
import functools as f

import utils

input_str = utils.get_input("3")
NEIGHBOURS_OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


@dataclass
class Coordinates:
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coordinates):
            return Coordinates(self.x + other.x, self.y + other.y)
        elif isinstance(other, Sequence):
            return Coordinates(self.x + other[0], self.y + other[1])

    def __hash__(self):
        return hash((self.x, self.y))


class Number:
    def __init__(self, number_str: str, coordinates: Coordinates):
        self.number = int(number_str)
        self.span = [coordinates + (dx, 0) for dx in range(len(number_str))]
        self.neighbours = set()
        for coord in self.span:
            self.neighbours.update(coord + offset for offset in NEIGHBOURS_OFFSETS)

    def detect_part(self, symbols: list[Symbol]):
        has_symbol = False
        for symbol in symbols:
            if symbol.coordinates in self.neighbours:
                symbol.numbers.add(self)
                has_symbol = True
        return has_symbol

    def __hash__(self):
        return hash(self.span[0])


class Symbol:
    def __init__(self, symbol: str, coordinates: Coordinates):
        self.symbol, self.coordinates = symbol, coordinates
        self.numbers = set()


def parse_input(input_str):
    numbers, symbols = [], []
    for y, line in enumerate(input_str.split('\n')):
        for match in re.finditer(r'(\d+)', line):
            numbers.append(Number(match.group(), Coordinates(match.start(), y)))
        for match in re.finditer(r'([^\d.])', line):
            symbols.append(Symbol(match.group(), Coordinates(match.start(), y)))
    return symbols, numbers


def solve_p1(input_str):
    symbols, numbers = parse_input(input_str)

    parts = set()
    for number in numbers:
        if number.detect_part(symbols):
            parts.add(number)
    return f.reduce(lambda a, b: a + b.number, parts, 0)


def solve_p2(input_str):
    symbols, numbers = parse_input(input_str)

    for number in numbers:
        number.detect_part(symbols)

    gears = [f.reduce(lambda a, b: a.number * b.number, symbol.numbers)
             for symbol in symbols
             if symbol.symbol == '*' and len(symbol.numbers) == 2]
    return f.reduce(lambda a, b: a + b, gears)


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
