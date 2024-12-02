"""
The elves bought too much eggnog again - 150 liters this time. To fit it all into your refrigerator, you'll need to move it into smaller containers. You take an inventory of the capacities of the available containers.

For example, suppose you have containers of size 20, 15, 10, 5, and 5 liters. If you need to store 25 liters, there are four ways to do it:

    15 and 10
    20 and 5 (the first 5)
    20 and 5 (the second 5)
    15, 5, and 5

Filling all containers entirely, how many different combinations of containers can exactly fit all 150 liters of eggnog?
"""

from utils import read_input_file
from pathlib import Path
from itertools import combinations
from collections import defaultdict


def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day17_input"
    data = read_input_file(file_path)
    return list(map(int, data))


def part1():
    data = test_data()
    res = 0
    for i in range(len(data)):
        for x in combinations(data, i):
            if sum(x) == 150:
                res += 1
    
    return res


"""
--- Part Two ---

While playing with all the containers in the kitchen, another load of eggnog arrives! The shipping and receiving department is requesting as many containers as you can spare.

Find the minimum number of containers that can exactly fit all 150 liters of eggnog. How many different ways can you fill that number of containers and still hold exactly 150 litres?

In the example above, the minimum number of containers was two. There were three ways to use that many containers, and so the answer there would be 3.
"""
def part2():
    data = test_data()

    res = defaultdict(int)
    for i in range(len(data)):
        for x in combinations(data, i):
            if sum(x) == 150:
                res[len(x)] += 1
    
    return res[min(res)]


if __name__ == "__main__":
    x = part1()
    print(x)
    y = part2()
    print(y)
