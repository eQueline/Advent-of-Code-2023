from __future__ import annotations

from collections import defaultdict
from typing import Sequence
from dataclasses import dataclass
import re
import functools as f

import utils

input_str = utils.get_input("5")


class Mapping:
    def __init__(self, source_range, dest_range):
        self.dest_range = dest_range
        self.source_range = source_range

    def __repr__(self):
        return f'{self.source_range} -> {self.dest_range}'

def intersect(seed: Mapping, mapping: Mapping):
    intersection_mapping = None
    ranges = []
    if seed.dest_range[0] <= mapping.source_range[1] and seed.dest_range[1] >= mapping.source_range[0]:
        intersection = (max(seed.dest_range[0], mapping.source_range[0]),
                        min(seed.dest_range[1], mapping.source_range[1]))
        intersection_mapping = Mapping(intersection,
                                       (intersection[0] - mapping.source_range[0] + mapping.dest_range[0],
                                        intersection[1] - mapping.source_range[0] + mapping.dest_range[0]))
        if seed.dest_range[0] < intersection[0]:
            ranges.append(Mapping((seed.dest_range[0], intersection[0] - 1),
                                  (seed.dest_range[0], intersection[0] - 1)))
        if seed.dest_range[1] > intersection[1]:
            ranges.append(Mapping((intersection[1] + 1, seed.dest_range[1]),
                                  (intersection[1] + 1, seed.dest_range[1])))
    else:
        ranges.append(seed)
    return ranges, intersection_mapping


def parse_input(input_str, part):
    mappings = defaultdict(list)
    seeds = []
    for i, mapping in enumerate(input_str.split('\n\n')):
        if i == 0:
            seed_list = [*map(lambda x: int(x), mapping[mapping.index(':') + 2:].split(' '))]
            # Each seed as mapping with single number range for part1
            if part == 1:
                for seed in seed_list:
                    seeds.append(Mapping(None, (seed, seed)))
            # Range mapping for part2
            elif part == 2:
                for j in range(0, len(seed_list) - 1, 2):
                    seeds.append(Mapping(None, (seed_list[j], seed_list[j] + seed_list[j + 1] - 1)))
        else:
            # Mappings
            name, *ranges = mapping.split('\n')
            for r in ranges:
                dest_start, source_start, source_length = map(lambda x: int(x), r.split(' '))
                mappings[name].append(Mapping((source_start, source_start + source_length),
                                              (dest_start, dest_start + source_length)))
    return seeds, mappings


def solve(seeds, map_list):
    """For each step, for each seed, save intersections with mappings and aggregate leftover ranges"""
    for name, mappings in map_list.items():
        new_seeds = []
        for i, seed in enumerate(seeds):
            range_list = [seed]  # all ranges for seed
            for mapping in mappings:
                new_ranges = []
                for range_mapping in range_list:
                    ranges, intersection = intersect(range_mapping, mapping)
                    if len(ranges) > 0:
                        # aggregate ranges left after intersections
                        new_ranges.extend(ranges)
                    if intersection is not None:
                        new_seeds.append(intersection)
                range_list = new_ranges
            new_seeds.extend(range_list)
        # For next iteration
        seeds = new_seeds
    return min(map(lambda x: x.dest_range[0], seeds))


def solve_p1(input_str):
    return solve(*parse_input(input_str, 1))


def solve_p2(input_str):
    return solve(*parse_input(input_str, 2))


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
