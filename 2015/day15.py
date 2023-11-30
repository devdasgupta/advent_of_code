"""
Today, you set out on the task of perfecting your milk-dunking cookie recipe. All you have to do is find the right balance of ingredients.

Your recipe leaves room for exactly 100 teaspoons of ingredients. You make a list of the remaining ingredients you could use to finish the recipe (your puzzle input) and their properties per teaspoon:

    capacity (how well it helps the cookie absorb milk)
    durability (how well it keeps the cookie intact when full of milk)
    flavor (how tasty it makes the cookie)
    texture (how it improves the feel of the cookie)
    calories (how many calories it adds to the cookie)

You can only measure ingredients in whole-teaspoon amounts accurately, and you have to be accurate so you can reproduce your results in the future. The total score of a cookie can be found by adding up each of the properties (negative totals become 0) and then multiplying together everything except calories.

For instance, suppose you have these two ingredients:

Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3

Then, choosing to use 44 teaspoons of butterscotch and 56 teaspoons of cinnamon (because the amounts of each ingredient must add up to 100) would result in a cookie with the following properties:

    A capacity of 44*-1 + 56*2 = 68
    A durability of 44*-2 + 56*3 = 80
    A flavor of 44*6 + 56*-2 = 152
    A texture of 44*3 + 56*-1 = 76

Multiplying these together (68 * 80 * 152 * 76, ignoring calories for now) results in a total score of 62842880, which happens to be the best score possible given these ingredients. If any properties had produced a negative total, it would have instead become zero, causing the whole score to multiply to zero.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make?
"""

from utils import read_input_file
from pathlib import Path
import re
import numpy as np
from itertools import product
from functools import reduce
from typing import List

from math import prod

def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day15_input"
    return read_input_file(filepath=file_path)


def list_prod(lst: List, num: int):
    return [num * x for x in lst]


def lst_add(lst1: List, lst2: List):
    res = []
    for i, j in zip(lst1, lst2):
        res.append(i + j)
    
    return res


def part1():
    data = test_data()
    data = [list(map(int, re.findall(r"-?\d+", x))) for x in data]

    # data = [
    #     [-1, -2, 6, 3, 8],
    #     [2, 3, -2, -1, 3]
    # ]

    n_ingrds = len(data)

    ingrds_q = list(range(1, 100 - n_ingrds + 2))

    all_comb = [ingrds_q] * n_ingrds

    proportions = [x for x in product(*all_comb) if sum(x) == 100]
    
    overall_score = []
    max_score = 0
    print(np.array(data))

    for proportion in proportions:
        
        score = [list_prod(i, j) for i, j in zip(data, proportion)]
        
        sum_score = reduce(lambda x, y: lst_add(x, y), score)
        sum_score = [max(x, 0) for x in sum_score]
        
        tot_score = reduce(lambda x, y: x * y, sum_score[:-1])
        

        # if tot_score > max_score:
        #     max_score = tot_score
        #     print(proportion)
        
        overall_score.append(tot_score)

    return max(overall_score)


# This is an alternate solution

def divide(number, buckets):
    if buckets == 1:
        yield (number,)
    else:
        for bucket in range(number + 1):
            for rest in divide(number - bucket, buckets - 1):
                yield (bucket,) + rest


def alt_sol():

    ingredients = [tuple(map(int, re.findall(r"-?\d+", line))) for line in test_data()]
    print(ingredients)
    s1 = s2 = 0

    # x = [buckets for buckets in divide(100, len(ingredients))]
    # print(len(x))

    for buckets in divide(100, len(ingredients)):
        *props, cals = (
            max(sum(b * s for b, s in zip(buckets, slice)), 0)
            for slice in zip(*ingredients)
        )

        if s1 < (total := prod(props)):
            # print(props)
            # print(buckets)
            s1 = total

    print(s1)
    return s1


"""
--- Part Two ---

Your cookie recipe becomes wildly popular! Someone asks if you can make another recipe that has exactly 500 calories per cookie (so they can use it as a meal replacement). Keep the rest of your award-winning process the same (100 teaspoons, same ingredients, same scoring system).

For example, given the ingredients above, if you had instead selected 40 teaspoons of butterscotch and 60 teaspoons of cinnamon (which still adds to 100), the total calorie count would be 40*8 + 60*3 = 500. The total score would go down, though: only 57600000, the best you can do in such trying circumstances.

Given the ingredients in your kitchen and their properties, what is the total score of the highest-scoring cookie you can make with a calorie total of 500?

"""

def part2():
    data = test_data()
    data = [list(map(int, re.findall(r"-?\d+", x))) for x in data]

    # data = [
    #     [-1, -2, 6, 3, 8],
    #     [2, 3, -2, -1, 3]
    # ]

    n_ingrds = len(data)

    ingrds_q = list(range(1, 100 - n_ingrds + 2))

    all_comb = [ingrds_q] * n_ingrds

    proportions = [x for x in product(*all_comb) if sum(x) == 100]
    
    overall_score = []
    max_score = 0
    print(np.array(data))

    for proportion in proportions:
        
        score = [list_prod(i, j) for i, j in zip(data, proportion)]
        
        sum_score = reduce(lambda x, y: lst_add(x, y), score)
        sum_score = [max(x, 0) for x in sum_score]
        
        if sum_score[-1] != 500:
            continue

        tot_score = reduce(lambda x, y: x * y, sum_score[:-1])
        

        # if tot_score > max_score:
        #     max_score = tot_score
        #     print(proportion)
        
        overall_score.append(tot_score)

    return max(overall_score)


if __name__ == "__main__":
    x = part1()
    print(x)
    # alt_sol()
    y = part2()
    print(y)