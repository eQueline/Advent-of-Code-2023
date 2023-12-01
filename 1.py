import utils
import re

input_str = utils.get_input("1")
DIGIT_MAP = {"one": "1", "two": "2", "three": "3",
             "four": "4", "five": "5", "six": "6",
             "seven": "7", "eight": "8", "nine": "9"}


def solve_p1(input_str):
    value_sum = 0
    for line in input_str.split('\n'):
        digits = re.findall(r"(\d)", line)
        value_sum += int(digits[0] + digits[-1])
    return value_sum


def solve_p2(input_str):
    value_sum = 0
    for line in input_str.split('\n'):
        str_digits = re.findall(fr"(?=(\d|{'|'.join(DIGIT_MAP.keys())}))", line)
        str_digits = [DIGIT_MAP[i] if len(i) > 1 else i for i in str_digits]
        value_sum += int(str_digits[0] + str_digits[-1])
    return value_sum


part1 = utils.time_function(solve_p1, input_str)
print("Part 1:", part1)
part2 = utils.time_function(solve_p2, input_str)
print("Part 2:", part2)
