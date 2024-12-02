"""
Every year, Santa manages to deliver all of his presents in a single night.

This year, however, he has some new locations to visit; his elves have provided him the distances between every pair of locations. He can start and end at any two (different) locations he wants, but he must visit each location exactly once. What is the shortest distance he can travel to achieve this?

For example, given the following distances:

London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141

The possible routes are therefore:

Dublin -> London -> Belfast = 982
London -> Dublin -> Belfast = 605
London -> Belfast -> Dublin = 659
Dublin -> Belfast -> London = 659
Belfast -> Dublin -> London = 605
Belfast -> London -> Dublin = 982

The shortest of these is London -> Dublin -> Belfast = 605, and so the answer is 605 in this example.

What is the distance of the shortest route?
"""

"""
--- Part Two ---

The next year, just to show off, Santa decides to take the route with the longest distance instead.

He can still start and end at any two (different) locations he wants, and he still must visit each location exactly once.

For example, given the distances above, the longest route would be 982 via (for example) Dublin -> London -> Belfast.

What is the distance of the longest route?

"""

from utils import read_input_file
from pathlib import Path
import re
from collections import defaultdict
from itertools import permutations
import json

def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day9_input"
    return read_input_file(_file)

def get_cities():
    data = test_data()
    cities = defaultdict(dict)

    for x in data:
        v = re.split(" to | = ", x)
        cities[v[0]][v[1]] = int(v[2])
        cities[v[1]][v[0]] = int(v[2])
    # print(json.dumps(cities, indent=4))

    return cities

def part1():
    cities = get_cities()
    # print(json.dumps(cities, indent=4))

    tot_distance_list = []
    minimal = 10000000
    for locations in permutations(cities):
        
        dist = 0
        try:
            for city_from, city_to in zip(locations, locations[1:]):
                dist += cities[city_from][city_to]
            minimal = min(minimal, dist)
            if dist == minimal:
                print(locations)

            tot_distance_list.append(dist)
        except KeyError:
            continue

    return tot_distance_list

if __name__ == "__main__":
    x = part1()
    print(min(x))
    print(max(x))