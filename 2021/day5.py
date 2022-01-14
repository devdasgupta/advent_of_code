from pathlib import Path
import re
from collections import namedtuple, Counter
from utils import read_input_file
from dataclasses import dataclass


file_path = Path(__file__).parent.absolute()
INPUT_DATA_FILE = f'{file_path}/day5_input'

Point = namedtuple("Point", "x y")

TEST_DATA = """
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

@dataclass
class Coord:
    cord_start: Point
    cord_end: Point

    def get_points_bwtn(self):
        cord_list = []
        if self.cord_start.x == self.cord_end.x:
            y1, y2 = (self.cord_start.y, self.cord_end.y) if self.cord_start.y < self.cord_end.y else (self.cord_end.y, self.cord_start.y)

            cord_list = [(self.cord_start.x, y) for y in range(y1, y2 + 1, 1)]
        elif self.cord_start.y == self.cord_end.y:
            x1, x2 = (self.cord_start.x, self.cord_end.x) if self.cord_start.x < self.cord_end.x else (self.cord_end.x, self.cord_start.x)

            cord_list = [(x, self.cord_start.y) for x in range(x1, x2 + 1, 1)]
        else:
            slope = (self.cord_end.y - self.cord_start.y) / (self.cord_end.x - self.cord_start.x)
            x1, x2 = (min(self.cord_start.x, self.cord_end.x), max(self.cord_start.x, self.cord_end.x))
            y1, y2 = (min(self.cord_start.y, self.cord_end.y), max(self.cord_start.y, self.cord_end.y))

            # print(x1, y1, x2, y2, slope)
            if slope < 1:
                x1, x2 = x2, x1
                y1, y2 = y2, y1
            # print(x1, y1, x2, y2, slope)
            while x1 <= x2 or y1 <= y2:
                cord_list.append((int(x1), int(y1)))
                x1 += 1
                y1 += 1
        print(self.cord_start, self.cord_end, cord_list)
        return cord_list


def get_counts(coordinates):
    count_dict = {k: v for k, v in Counter(coordinates).items() if v > 1}

    return len(count_dict)


def puzzle1(input_items):
    """
    You come across a field of hydrothermal vents on the ocean floor! These
    vents constantly produce large, opaque clouds, so it would be best
    to avoid them if possible.

    They tend to form in lines; the submarine helpfully produces a list of
    nearby lines of vents (your puzzle input) for you to review. For example:

    0,9 -> 5,9
    8,0 -> 0,8
    9,4 -> 3,4
    2,2 -> 2,1
    7,0 -> 7,4
    6,4 -> 2,0
    0,9 -> 2,9
    3,4 -> 1,4
    0,0 -> 8,8
    5,5 -> 8,2

    Each line of vents is given as a line segment in the format x1,y1 -> x2,y2
    where x1,y1 are the coordinates of one end the line segment and x2,y2 are
    the coordinates of the other end. These line segments include the points
    at both ends. In other words:

        An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
        An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.

    For now, only consider horizontal and vertical lines: lines where
    either x1 = x2 or y1 = y2.

    In this diagram, the top left corner is 0,0 and the bottom right corner
    is 9,9. Each position is shown as the number of lines which cover that
    point or . if no line covers that point. The top-left pair of 1s, for
    example, comes from 2,2 -> 2,1; the very bottom row is formed by the
    overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

    To avoid the most dangerous areas, you need to determine the number of points
    where at least two lines overlap. In the above example, this is anywhere
    in the diagram with a 2 or larger - a total of 5 points.

    Consider only horizontal and vertical lines. At how many points do at
    least two lines overlap?
    """
    coordinates = []
    input_items = [(Point(int(x[0]), int(x[1])), Point(int(x[2]), int(x[3])))
                        for x in input_items if x[0] == x[2] or x[1] == x[3]]

    for x in input_items:
        coordinates.extend(x for x in Coord(*x).get_points_bwtn())

    count = get_counts(coordinates)

    print(count)


def puzzle2(input_items):
    _inp_item = []
    coordinates = []
    for x in input_items:
        if x[0] == x[2] or x[1] == x[3]:
            _inp_item.append((Point(int(x[0]), int(x[1])), Point(int(x[2]), int(x[3]))))
        elif abs((int(x[3]) - int(x[1])) / (int(x[2]) - int(x[0]))) == 1.0:
            _inp_item.append((Point(int(x[0]), int(x[1])), Point(int(x[2]), int(x[3]))))
            slope = (int(x[3]) - int(x[1])) / (int(x[2]) - int(x[0]))
            # print(f'y2 - y1 = {x[3]} - {x[1]} = {int(x[3]) - int(x[1])}\tx2 - x1 = {x[2]} - {x[0]} = {int(x[2]) - int(x[0])}\tslope = {slope}, {abs(slope)}')
            # print(f'{x[0]} {x[1]}, {x[2]}, {x[3]} slope = {slope}, {abs(slope)}')

    # for x in _inp_item:
    #     print(x)
    for x in _inp_item:
        coordinates.extend(x for x in Coord(*x).get_points_bwtn())

    count = get_counts(coordinates)

    print(count)


if __name__ == "__main__":
    # input_items = read_input_file(INPUT_DATA_FILE)
    input_items = TEST_DATA.strip().split('\n')
    input_items = [re.split(',| -> ', x) for x in input_items]


    # puzzle1(input_items)
    puzzle2(input_items)
