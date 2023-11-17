"""
Santa's Accounting-Elves need help balancing the books after a recent order. Unfortunately, their accounting software uses a peculiar storage format. That's where you come in.

They have a JSON document which contains a variety of things: arrays ([1,2,3]), objects ({"a":1, "b":2}), numbers, and strings. Your first job is to simply find all of the numbers throughout the document and add them together.

For example:

    [1,2,3] and {"a":2,"b":4} both have a sum of 6.
    [[[3]]] and {"a":{"b":4},"c":-1} both have a sum of 3.
    {"a":[-1,1]} and [-1,{"a":1}] both have a sum of 0.
    [] and {} both have a sum of 0.

You will not encounter any strings containing numbers.

What is the sum of all numbers in the document?
"""

import re
from pathlib import Path
from utils import read_regular_file
import json
from typing import List


def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day12_input"
    return read_regular_file(file_path)

def part1():
    data = test_data()
    res = re.findall(r"-?\d+", data)
    
    return sum(map(int, res))


"""
--- Part Two ---

Uh oh - the Accounting-Elves have realized that they double-counted everything red.

Ignore any object (and all of its children) which has any property with the value "red". Do this only for objects ({...}), not arrays ([...]).

    [1,2,3] still has a sum of 6.
    [1,{"c":"red","b":2},3] now has a sum of 4, because the middle object is ignored.
    {"d":"red","e":[1,2,3,4],"f":5} now has a sum of 0, because the entire structure is ignored.
    [1,"red",5] has a sum of 6, because "red" in an array has no effect.
"""

def flatten(data: List, ignore = None):
    for x in data:
        if isinstance(x, int):
            yield x
        elif isinstance(x, list):
            yield from flatten(x, ignore)
        elif isinstance(x, dict) and ignore not in x.keys():
            yield from flatten(x.values(), ignore)
        else:
            yield 0


def part2():
    data = json.loads(test_data())
    res = [x for x in flatten(data, "red")]
    return sum(res)


if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)