from utils import read_input_file
from pathlib import Path


def get_data():
    _file = f"{Path(__file__).parent.absolute()}/day7_input"
    lst = read_input_file(_file, delimiter="\n")
    return lst


"""
You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. 
In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?
"""

from operator import add, mul
from itertools import product


def part1(lst):
    total = 0
    for idx, line in enumerate(lst):
        _sum = int(line.split(":")[0])
        nums = list(map(int, line.split(":")[-1].split()))

        arguments = [["+", "*"] for _ in range(len(nums) - 1)]
        for perm in product(*arguments):
            
            _sum_ = nums[0] 
            for i, num in enumerate(nums[1:]):
                
                if perm[i] == "+":
                    _sum_ = add(_sum_, num)
                else:
                    _sum_ = mul(_sum_, num)

                # print(i, num, perm[i], _sum_)
            if _sum_ == _sum:
                print(idx,_sum, perm, nums)
                total += _sum
                break
        

    return total


"""
The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?
"""
def part2(lst):
    total = 0
    for idx, line in enumerate(lst):
        _sum = int(line.split(":")[0])
        nums = list(map(int, line.split(":")[-1].split()))

        arguments = [["+", "*", "||"] for _ in range(len(nums) - 1)]
        for perm in product(*arguments):
            
            _sum_ = nums[0] 
            for i, num in enumerate(nums[1:]):
                
                if perm[i] == "+":
                    _sum_ = add(_sum_, num)
                elif perm[i] == "*":
                    _sum_ = mul(_sum_, num)
                else:
                    _sum_ = int(str(_sum_) + str(num))

                # print(i, num, perm[i], _sum_)
            if _sum_ == _sum:
                print(idx,_sum, perm, nums)
                total += _sum
                break
        

    return total

if __name__ == "__main__":
    lst = get_data()
    # lst = [
    #     "190: 10 19",
    #     "3267: 81 40 27",
    #     "83: 17 5",
    #     "156: 15 6",
    #     "7290: 6 8 6 15",
    #     "161011: 16 10 13",
    #     "192: 17 8 14",
    #     "21037: 9 7 18 13",
    #     "292: 11 6 16 20"
    # ]
    
    res = part1(lst)
    print(res)

    res = part2(lst)
    print(res)