"""
You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols 
you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included 
in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
"""

from utils import read_input_file, prGreen, prYellow
from pathlib import Path
from functools import reduce
from collections import namedtuple
from typing import List
import re


def test_data(data = None) -> List:
    file_path = f"{Path(__file__).parent.absolute()}/day3_input"
    data = data if data else read_input_file(file_path)
    val = list()
    values = namedtuple("values", "string, numbers, spec_chars")
    
    for x in data:
        
        numbers = [i.span() for i in re.finditer(r"\d+", x)]
        rex = r"-|#|&|=|\+|@|%|\*|\/|\$"
        spec_chars = [i.span()[0] for i in re.finditer(rex, x)]
        val.append(values(x, numbers, spec_chars))
        
    return val

def get_valid_numbers(value, compare_value1, compare_value2 = None) -> List:
    
    # prYellow(compare_value1.string)
    # prGreen(value.string)
    # if compare_value2:
    #     prYellow(compare_value2.string)

    # print(value.numbers)
    # print(value.spec_chars)
    # print(compare_value1.spec_chars)
    # if compare_value2:
    #     print(compare_value2.spec_chars)

    spec_chars_pos = value.spec_chars + compare_value1.spec_chars
    spec_chars_pos += compare_value2.spec_chars if compare_value2 else []

    valid_numbers = []

    for start, end in value.numbers:
        if any([i in spec_chars_pos for i in range(start - 1, end + 1)]):
            valid_numbers.append(int(value.string[start:end]))

    # print("Valid Numbers", valid_numbers)
    # print()
    return valid_numbers



def part1(_data: None):
    data = test_data(_data)
    final_score = []

    for idx in range(len(data)):
        if idx == 0:
            final_score += get_valid_numbers(data[idx], data[idx + 1])
        elif idx == len(data) - 1:
            final_score += get_valid_numbers(data[idx], data[idx - 1])
        else:
            final_score += get_valid_numbers(data[idx], data[idx - 1], data[idx + 1])
            
    return sum(final_score)


"""
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..

In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
"""
def part2():
    file_path = f"{Path(__file__).parent.absolute()}/day3_input"
    grid = read_input_file(file_path)

    final_score = 0

    for r, row in enumerate(grid):

        for c, ch in enumerate(row):
            if ch != "*":
                continue
            
            cs = set()

            for cr in [r - 1, r, r + 1]:
                for cc in [c - 1, c, c + 1]:
                    if cr < 0 or cr >= len(grid) or cc < 0 or cc >= len(grid[cr]) or not grid[cr][cc].isdigit():
                        continue

                    while cc > 0 and grid[cr][cc - 1].isdigit():
                        cc -= 1
                    cs.add((cr, cc))
            
            if len(cs) != 2:
                continue

            ns = []

            for cr, cc in cs:
                s = ""
                while cc < len(grid[cr]) and grid[cr][cc].isdigit():
                    s += grid[cr][cc]
                    cc += 1
                ns.append(int(s))
            print(ns)
            score = ns[0] * ns[1]
            print(score)
            final_score += score
    return final_score


if __name__ == "__main__":
    x = part1(None)
    print(x)

    y = part2()
    print(y)
