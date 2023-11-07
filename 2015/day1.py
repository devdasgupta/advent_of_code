"""
Here's an easy puzzle to warm you up.

Santa is trying to deliver presents in a large apartment building, but he can't find the right floor - the directions he got are a little confusing. He starts on the ground floor (floor 0) and then follows the instructions one character at a time.

An opening parenthesis, (, means he should go up one floor, and a closing parenthesis, ), means he should go down one floor.

The apartment building is very tall, and the basement is very deep; he will never find the top or bottom floors.

For example:

    (()) and ()() both result in floor 0.
    ((( and (()(()( both result in floor 3.
    ))((((( also results in floor 3.
    ()) and ))( both result in floor -1 (the first basement level).
    ))) and )())()) both result in floor -3.

To what floor do the instructions take Santa?
"""
from pathlib import Path
from utils import read_regular_file
from collections import Counter


def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day1_input"
    return read_regular_file(_file)

def part1():
    data = [x for x in test_data()]
    count = Counter(data)
    return count.get('(') - count.get(')')

def part2():
    data = test_data()
    res = 0
    for idx, x in enumerate(data):
        res += 1 if x == '(' else -1

        if res == -1:
            break
    
    return idx + 1


if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)
