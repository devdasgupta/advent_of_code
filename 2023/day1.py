"""
The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet

In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?
"""

from utils import read_input_file
from pathlib import Path
import re

def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day1_input"
    return read_input_file(file_path)


def part1():
    data = test_data()
    num = 0
    for x in data:
        val = re.findall(r"\d", x)
        num += int(val[0]) * 10 + int(val[-1])

    return num


"""
--- Part Two ---

Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen

In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?
"""
mappings = {
    "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, 
    "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
}

def part2():
    data = test_data()
    num = 0
    for x in data:
        rex = r"(?=(\d)|(zero)|(one)|(two)|(three)|(four)|(five)|(six)|(seven)|(eight)|(nine))"
        val = map(lambda i: "".join(i), re.findall(rex, x))
        val = [mappings[i] for i in val]
        s = val[0] * 10 + val[-1]
        num += s

    return num


if __name__ == "__main__":
    x = part1()
    print(x)
    y = part2()
    print(y)
