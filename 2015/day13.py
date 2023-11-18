"""
In years past, the holiday feast with your family hasn't gone so well. Not everyone gets along! This year, you resolve, will be different. You're going to find the optimal seating arrangement and avoid all those awkward conversations.

You start by writing up a list of everyone invited and the amount their happiness would increase or decrease if they were to find themselves sitting next to each other person. You have a circular table that will be just big enough to fit everyone comfortably, and so each person will have exactly two neighbors.

For example, suppose you have only four attendees planned, and you calculate their potential happiness as follows:

Alice would gain 54 happiness units by sitting next to Bob.
Alice would lose 79 happiness units by sitting next to Carol.
Alice would lose 2 happiness units by sitting next to David.
Bob would gain 83 happiness units by sitting next to Alice.
Bob would lose 7 happiness units by sitting next to Carol.
Bob would lose 63 happiness units by sitting next to David.
Carol would lose 62 happiness units by sitting next to Alice.
Carol would gain 60 happiness units by sitting next to Bob.
Carol would gain 55 happiness units by sitting next to David.
David would gain 46 happiness units by sitting next to Alice.
David would lose 7 happiness units by sitting next to Bob.
David would gain 41 happiness units by sitting next to Carol.

Then, if you seat Alice next to David, Alice would lose 2 happiness units (because David talks so much), but David would gain 46 happiness units (because Alice is such a good listener), for a total change of 44.

If you continue around the table, you could then seat Bob next to Alice (Bob gains 83, Alice gains 54). Finally, seat Carol, who sits next to Bob (Carol gains 60, Bob loses 7) and David (Carol gains 55, David gains 41). The arrangement looks like this:

     +41 +46
+55   David    -2
Carol       Alice
+60    Bob    +54
     -7  +83

After trying every other seating arrangement in this hypothetical scenario, you find that this one is the most optimal, with a total change in happiness of 330.

What is the total change in happiness for the optimal seating arrangement of the actual guest list?
"""

from utils import read_input_file
from pathlib import Path
from collections import defaultdict
import json
from itertools import permutations

input_data = defaultdict(dict)

def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day13_input"
    data = read_input_file(filepath=file_path)

    for i in data:
        val = i.replace(".", "").split()
        p1 = val[0]
        p2 = val[-1]
        happy = int(val[3]) if val[2] == "gain" else -1 * int(val[3])
        input_data[p1] = {**input_data[p1], **{p2: happy}}
        # input_data[val[0]] = {f"{val[-1]}": f"{-1 * int(val[3])}"} if val[2] == "lose" else {f"{val[-1]}": f"{int(val[3])}"}

    return input_data


def get_max_score(data):
    scores = []
    for x in permutations(data, len(data)):
        x = x + (x[0],) # Adding the first element of the tuple again to complete the cycle
        score_clockwise = [input_data[i][j] for i, j in zip(x, x[1:])]

        y = x[::-1]
        score_anticlockwise = [input_data[i][j] for i, j in zip(y, y[1:])]
        
        scores.append(sum(score_anticlockwise + score_clockwise))

    return max(scores)


def part1():
    data = test_data()

    return get_max_score(data)


"""
--- Part Two ---

In all the commotion, you realize that you forgot to seat yourself. At this point, you're pretty apathetic toward the whole thing, and your happiness wouldn't really go up or down regardless of who you sit next to. You assume everyone else would be just as ambivalent about sitting next to you, too.

So, add yourself to the list, and give all happiness relationships that involve you a score of 0.

What is the total change in happiness for the optimal seating arrangement that actually includes yourself?
"""
def part2():
    data = test_data()
    for k in data.keys():
        data[k] = {**data[k], **{"me": 0}}
    data["me"] = {k: 0 for k in data.keys()}
    
    return get_max_score(data)


"""
Alternate Solution
"""
from math import factorial
from itertools import permutations
from collections import defaultdict


def solve(first, people):
    limit = factorial(len(people)) // 2

    return max(
        sum(data[frozenset([a, b])] for a, b in zip(first + table, table + first))
        for i, table in enumerate(permutations(people))
        if i < limit  # avoid cyclic permutations and reversals
    )

def solution():
    inp_data = test_data()
    people, data = set(), defaultdict(int)

    for a, _, gain, n, *_, b in map(str.split, inp_data):
        people.add(a)
        data[frozenset([a, b[:-1]])] += int(n) * (-1) ** (gain != "gain")

    first = people.pop()
    print(solve(tuple([first]), people))

    people.add(first)
    print(solve(tuple("0"), people))

if __name__ == "__main__":
    x = part1()
    print(x)
    y = part2()
    print(y)