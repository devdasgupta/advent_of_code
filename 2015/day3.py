"""
Santa is delivering presents to an infinite two-dimensional grid of houses.

He begins by delivering a present to the house at his starting location, and then an elf at the North Pole calls him via radio and tells him where to move next. Moves are always exactly one house to the north (^), south (v), east (>), or west (<). After each move, he delivers another present to the house at his new location.

However, the elf back at the north pole has had a little too much eggnog, and so his directions are a little off, and Santa ends up visiting some houses more than once. How many houses receive at least one present?

For example:

    > delivers presents to 2 houses: one at the starting location, and one to the east.
    ^>v< delivers presents to 4 houses in a square, including twice to the house at his starting/ending location.
    ^v^v^v^v^v delivers a bunch of presents to some very lucky children at only 2 houses.

"""
import numpy as np
from typing import List
from pathlib import Path
from utils import read_regular_file

def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day3_input"
    return read_regular_file(_file)


def part1():
    data = test_data()
    # data = "^^>^^vv<"

    mat_len = 2 * len(data) - 1

    matx = np.zeros((mat_len, mat_len), dtype=int)

    x = y = len(data) - 1

    matx[x][y] += 1
    for d in data:
        # print(x, y, d)
        if d == ">":
            y += 1
        elif d == "<":
            y -= 1
        elif d == "^":
            x -= 1
        else:
            x += 1
        matx[x][y] += 1

    return np.count_nonzero(matx)


"""
The next year, to speed up the process, Santa creates a robot version of himself, Robo-Santa, to deliver presents with him.

Santa and Robo-Santa start at the same location (delivering two presents to the same starting house), then take turns moving based on instructions from the elf, who is eggnoggedly reading from the same script as the previous year.

This year, how many houses receive at least one present?

For example:

    ^v delivers presents to 3 houses, because Santa goes north, and then Robo-Santa goes south.
    ^>v< now delivers presents to 3 houses, and Santa and Robo-Santa end up back where they started.
    ^v^v^v^v^v now delivers presents to 11 houses, with Santa going one direction and Robo-Santa going the other.

"""
def part2():
    data = test_data()
    # data = "^^>^^vv<"

    mat_len = 2 * len(data) - 1

    matx = np.zeros((mat_len, mat_len), dtype=int)

    x = y = len(data) - 1
    rx = ry = len(data) - 1

    matx[x][y] += 1
    matx[rx][ry] += 1
    for i, d in enumerate(data):
        if i % 2 == 0:
            if d == ">":
                y += 1
            elif d == "<":
                y -= 1
            elif d == "^":
                x -= 1
            else:
                x += 1
            matx[x][y] += 1
        else:
            if d == ">":
                ry += 1
            elif d == "<":
                ry -= 1
            elif d == "^":
                rx -= 1
            else:
                rx += 1
            matx[rx][ry] += 1

    return np.count_nonzero(matx)


if __name__ == "__main__":
    c = part1()
    print(c)

    cc = part2()
    print(cc)