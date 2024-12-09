from utils import read_input_file
from pathlib import Path


def get_data():
    _file = f"{Path(__file__).parent.absolute()}/day6_input"
    lst = read_input_file(_file, delimiter="\n")
    return lst

"""
You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.

Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?
"""

def get_start_pos(lst):
    for y, row in enumerate(lst):
        for x, col in enumerate(row):
            if col == "^":
                return x, y

def part1(lst):
    
    x, y = get_start_pos(lst)
    n, m = len(lst), len(lst[0])

    visited = set()
    dir_map = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0)
    }

    dir_index = 0
    while(0 <= x < m and 0 <= y < n):
        visited.add((x, y))

        i, j = dir_map[list(dir_map.keys())[dir_index % 4]]
        x += i
        y += j

        try:
            if lst[y][x] == "#":
                dir_index += 1
                x -= i
                y -= j
        except IndexError:
            break

    return len(visited)


"""
In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
"""

def check_loop(lst):
    x, y = get_start_pos(lst)
    n, m = len(lst), len(lst[0])

    visited = set()
    loop = False
    dir_map = {
        "up": (0, -1),
        "right": (1, 0),
        "down": (0, 1),
        "left": (-1, 0)
    }

    dir_index = 0
    while(0 <= x < m and 0 <= y < n):
        direction = list(dir_map.keys())[dir_index % 4]
        if (x, y, direction) in visited:
            loop = True
            break

        visited.add((x, y, direction))

        i, j = dir_map[direction]
        x += i
        y += j

        try:
            if lst[y][x] == "#":
                dir_index += 1
                x -= i
                y -= j
        except IndexError:
            break

    return loop


def part2(lst):
    x, y = get_start_pos(lst)

    n, m = len(lst), len(lst[0])
    loop_count = 0

    for i in range(n):
        for j in range(m):
            if (i, j) == (y, x):
                continue

            if lst[i][j] == ".":
                lst[i] = lst[i][:j] + "#" + lst[i][j+1:]
                loop_count += 1 if check_loop(lst) else 0

                lst[i] = lst[i][:j] + "." + lst[i][j+1:]

    return loop_count


if __name__ == "__main__":
    lst = get_data()
    # lst = [
    #     "....#.....",
    #     ".........#",
    #     "..........",
    #     "..#.......",
    #     ".......#..",
    #     "..........",
    #     ".#..^.....",
    #     "........#.",
    #     "#.........",
    #     "......#..."
    # ]
    
    res = part1(lst)
    print(res)

    res = part2(lst)
    print(res)
