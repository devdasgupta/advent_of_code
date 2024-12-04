from utils import read_input_file
from pathlib import Path

"""
This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?
"""

def get_data():
    _file = f"{Path(__file__).parent.absolute()}/day4_input"
    lst = read_input_file(_file, delimiter="\n")
    return lst


def transpose(lst):
    return [''.join(x) for x in zip(*lst)]

def diagonal(lst):
    for x in range(len(lst) - 3):
        for y in range(len(lst[x]) - 3):
            yield ''.join([lst[x + i][y + i] for i in range(4)])
            yield ''.join([lst[x + 3 - i][y + i] for i in range(4)])

def part1(lst):
    res = 0
    for s in lst:
        res += s.count("XMAS")
        res += s.count("SAMX")
    
    for s in transpose(lst):
        res += s.count("XMAS")
        res += s.count("SAMX")

    for s in diagonal(lst):
        res += s.count("XMAS")
        res += s.count("SAMX")
    
    return res


"""
Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
"""
def part2(lst):
    res = 0
    for y in range(len(lst) - 2):
        for x in range(len(lst[y]) - 2):
            if (lst[x][y] + lst[x + 1][y + 1] + lst[x + 2][y + 2] in ("MAS", "SAM")) \
            and (lst[x][y + 2] + lst[x + 1][y + 1] + lst[x + 2][y] in ("MAS", "SAM")):
                res += 1

    return res


if __name__ == "__main__":
    lst = get_data()
    # lst = [
    #     "MMMSXXMASM",
    #     "MSAMXMSMSA",
    #     "AMXSXMAAMM",
    #     "MSAMASMSMX",
    #     "XMASAMXAMM",
    #     "XXAMMXXAMA",
    #     "SMSMSASXSS",
    #     "SAXAMASAAA",
    #     "MAMMMXMMMM",
    #     "MXMXAXMASX"
    # ]
    
    res = part1(lst)
    print(res)

    res = part2(lst)
    print(res)
