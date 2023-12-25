from __future__ import annotations
from typing import Sequence
from dataclasses import dataclass
import re
import functools as f

import utils

input_str = utils.get_input("4")


def parse_input(input_str):
    cards = []
    for card_str in input_str.split('\n'):
        wins, numbers = card_str[card_str.index(':') + 1:].split('|')
        #print(f'"{wins} "{numbers}"')
        card = [set(int(wins[i:i + 3]) for i in range(0, len(wins) - 3, 3)),
                set(int(numbers[i:i + 3]) for i in range(0, len(numbers) - 2, 3)), 1]
        #print(card)
        cards.append(card)
    return cards


def solve_p1(input_str):
    cards = parse_input(input_str)
    points = 0
    for wins, numbers, _ in cards:
        points += 2 ** (len(numbers.intersection(wins)) - 1) if len(numbers.intersection(wins)) > 0 else 0
    return points

def solve_p2(input_str):
    cards = parse_input(input_str)
    for i, card in enumerate(cards):
        wins = len(card[1].intersection(card[0]))
        for j in range(1, wins+1):
            cards[i+j][2] += cards[i][2]
    points = 0
    for i, card in enumerate(cards):
        points += card[2]
    return points


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
