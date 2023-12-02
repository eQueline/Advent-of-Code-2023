import re
import functools

import utils

input_str = utils.get_input("2")
TEST_SET = {"red": 12, "green": 13, "blue": 14}


def parse_input(input_str) -> dict:
    games = dict()
    for line in input_str.split('\n'):
        game_sets = []
        game_id = int(re.search(r'Game (\d+)', line).groups()[0])
        for game_sets_str in line.split(';'):
            game_sets_match = re.findall(r'(\d+) (\w+)', game_sets_str)
            game_set = {}
            for game_set_list in game_sets_match:
                game_set[game_set_list[1]] = int(game_set_list[0])
            game_sets.append(game_set)
        games[game_id] = game_sets
    return games


def check_game(game, test):
    for game_set in game:
        for color in game_set:
            if test[color] < game_set[color]:
                return False
    return True


def get_set_power(game):
    min_set = {"red": 0, 'green': 0, 'blue': 0}
    for game_set in game:
        for color in game_set:
            min_set[color] = max(game_set[color], min_set[color])
    return functools.reduce(lambda a, b: a * b, min_set.values())


def solve_p1(input_str):
    id_sum = 0
    games = parse_input(input_str)
    for game_id, game_set in games.items():
        if check_game(game_set, TEST_SET):
            id_sum += game_id
    return id_sum


def solve_p2(input_str):
    game_power_sum = 0
    games = parse_input(input_str)
    for game_set in games.values():
        game_power_sum += get_set_power(game_set)
    return game_power_sum


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
