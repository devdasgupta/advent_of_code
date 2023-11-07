"""
Because your neighbors keep defeating you in the holiday house decorating contest year after year, you've decided to deploy one million lights in a 1000x1000 grid.

Furthermore, because you've been especially nice this year, Santa has mailed you instructions on how to display the ideal lighting configuration.

Lights in your grid are numbered from 0 to 999 in each direction; the lights at each corner are at 0,0, 0,999, 999,999, and 999,0. The instructions include whether to turn on, turn off, or toggle various inclusive ranges given as coordinate pairs. Each coordinate pair represents opposite corners of a rectangle, inclusive; a coordinate pair like 0,0 through 2,2 therefore refers to 9 lights in a 3x3 square. The lights all start turned off.

To defeat your neighbors this year, all you have to do is set up your lights by doing the instructions Santa sent you in order.

For example:

    turn on 0,0 through 999,999 would turn on (or leave on) every light.
    toggle 0,0 through 999,0 would toggle the first line of 1000 lights, turning off the ones that were on, and turning on the ones that were off.
    turn off 499,499 through 500,500 would turn off (or leave off) the middle four lights.

After following the instructions, how many lights are lit?
"""

from pyparsing import Word, Literal, alphas, Combine, OneOrMore, White
from dataclasses import dataclass
from pathlib import Path
from utils import read_input_file
import numpy as np


@dataclass
class Point:
    x: int
    y: int

    def __post_init__(self):
        if not isinstance(self.x, int):
            self.x = int(self.x)
        if not isinstance(self.y, int):
            self.y = int(self.y)


@dataclass
class Instructions:
    instruction: str

    def __post_init__(self):
        word = Word(alphas)
        operator = Combine(OneOrMore(Word(alphas) | White(' ',max=1) ))
        integer = Word("0123456789")
        comma = Literal(",")

        expression = (
            operator + integer + comma + integer + word + integer + comma + integer
            )
        
        res = expression.parseString(self.instruction)
        self.operator = res[0].strip()
        self.start_pos = Point(res[1], res[3])
        self.end_pos = Point(res[5], res[7])

    def __repr__(self) -> str:
        return f"Operator: {self.operator}, Start Pos: {self.start_pos}, End Pos: {self.end_pos}"
    

    def follow_instructions(self, matrx):
        for x in range(self.start_pos.x, self.end_pos.x + 1, 1):
            for y in range(self.start_pos.y, self.end_pos.y + 1):
                if self.operator.startswith('turn on'):
                    matrx[x][y] = 1
                elif self.operator.startswith('turn off'):
                    matrx[x][y] = 0
                else:
                    matrx[x][y] = 1 if matrx[x][y] == 0 else 0

        return matrx
    
    def follow_instructions_2(self, matrx):
        for x in range(self.start_pos.x, self.end_pos.x + 1, 1):
            for y in range(self.start_pos.y, self.end_pos.y + 1):
                if self.operator.startswith('turn on'):
                    matrx[x][y] += 1
                elif self.operator.startswith('turn off'):
                    matrx[x][y] = max(0, matrx[x][y] - 1)
                else:
                    matrx[x][y] += 2

        return matrx
            


def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day6_input"
    return read_input_file(_file)


def part1():
    data = test_data()

    process_data = [Instructions(x) for x in data]
    
    grid = np.zeros([1000, 1000], dtype=int)

    for item in process_data:
        grid = item.follow_instructions(grid)

    return np.count_nonzero(grid)


"""
You just finish implementing your winning light pattern when you realize you mistranslated Santa's message from Ancient Nordic Elvish.

The light grid you bought actually has individual brightness controls; each light can have a brightness of zero or more. The lights all start at zero.

The phrase turn on actually means that you should increase the brightness of those lights by 1.

The phrase turn off actually means that you should decrease the brightness of those lights by 1, to a minimum of zero.

The phrase toggle actually means that you should increase the brightness of those lights by 2.

What is the total brightness of all lights combined after following Santa's instructions?

For example:

    turn on 0,0 through 0,0 would increase the total brightness by 1.
    toggle 0,0 through 999,999 would increase the total brightness by 2000000.
"""
def part2():
    data = test_data()

    process_data = [Instructions(x) for x in data]
    
    grid = np.zeros([1000, 1000], dtype=int)

    for item in process_data:
        grid = item.follow_instructions_2(grid)

    return np.sum(grid)


if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)
