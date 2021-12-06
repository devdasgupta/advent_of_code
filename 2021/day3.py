from pathlib import Path
from utils import read_input_file
from collections import Counter
from functools import partial

file_path = Path(__file__).parent.absolute()
INPUT_DATA_FILE = f'{file_path}/day3_input'
MAX = partial(max)
MIN = partial(min)

def flip(x: str):
    return '1' if x == '0' else '0'

def puzzle1(inp_items):
    """
    You need to use the binary numbers in the diagnostic report to generate two
    new binary numbers (called the gamma rate and the epsilon rate). The power
    consumption can then be found by multiplying the gamma rate by the epsilon rate.

    Each bit in the gamma rate can be determined by finding the most common bit
    in the corresponding position of all numbers in the diagnostic report.
    For example, given the following diagnostic report:

    00100
    11110
    10110
    10111
    10101
    01111
    00111
    11100
    10000
    11001
    00010
    01010

    Considering only the first bit of each number, there are five 0 bits and
    seven 1 bits. Since the most common bit is 1, the first bit of the
    gamma rate is 1.

    The most common second bit of the numbers in the diagnostic report is 0,
    so the second bit of the gamma rate is 0.

    The most common value of the third, fourth, and fifth bits are 1, 1, and 0,
    respectively, and so the final three bits of the gamma rate are 110.

    So, the gamma rate is the binary number 10110, or 22 in decimal.

    The epsilon rate is calculated in a similar way; rather than use the most
    common bit, the least common bit from each position is used. So, the epsilon
    rate is 01001, or 9 in decimal. Multiplying the gamma rate (22) by the
    epsilon rate (9) produces the power consumption, 198.

    Use the binary numbers in your diagnostic report to calculate the gamma rate
    and epsilon rate, then multiply them together. What is the power consumption
    of the submarine? (Be sure to represent your answer in decimal, not binary.)
    """
    inp_items = [list(x) for x in inp_items]

    # Transpose the 2D list/array
    inp_items = list(map(list, zip(*inp_items)))

    # Get the max occurence from each cumulated_list to get gamma_rate
    gamma_rate = [Counter(x).most_common(1)[0][0] for x in inp_items]
    print(gamma_rate)

    # flip the gamma_rate to get the epsilon gamma_rate
    epsilon_rate = list(map(flip, gamma_rate))
    print(epsilon_rate)

    # Join the list and then convert binary to decimal
    gamma_int = int(''.join(gamma_rate), 2)
    epsilon_int = int(''.join(epsilon_rate), 2)

    print(gamma_int * epsilon_int)


def get_index_count(item_list, pos, fn_criteria):
    """
    This functions inputs a list, the position of that list
    and then returns the items which occurs most or least based on
    the input provided by fn_criteria
    """
    val = [x[pos] for x in item_list]
    counts = Counter(val)
    if counts['0'] == counts['1']:
        return '1' if fn_criteria == MAX else '0'

    return fn_criteria(counts, key=counts.get)


def get_ratings(generator_list, _len, fn_criteria):
    for i in range(_len):
        common = get_index_count(generator_list, i, fn_criteria)
        generator_list = [x for x in generator_list if x[i] == common]

        if len(generator_list) == 1:
            break

    return int(''.join(generator_list[0]), 2)

def puzzle2(inp_items):
    """
    Next, you should verify the life support rating, which can be determined by multiplying the oxygen generator rating by the CO2 scrubber rating.

    Both the oxygen generator rating and the CO2 scrubber rating are values that can be found in your diagnostic report - finding them is the tricky part. Both values are located using a similar process that involves filtering out values until only one remains. Before searching for either rating value, start with the full list of binary numbers from your diagnostic report and consider just the first bit of those numbers. Then:

        Keep only numbers selected by the bit criteria for the type of rating value for which you are searching. Discard numbers which do not match the bit criteria.
        If you only have one number left, stop; this is the rating value for which you are searching.
        Otherwise, repeat the process, considering the next bit to the right.

    The bit criteria depends on which type of rating value you want to find:

        To find oxygen generator rating, determine the most common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 1 in the position being considered.
        To find CO2 scrubber rating, determine the least common value (0 or 1) in the current bit position, and keep only numbers with that bit in that position. If 0 and 1 are equally common, keep values with a 0 in the position being considered.

    For example, to determine the oxygen generator rating value using the same example diagnostic report from above:

        Start with all 12 numbers and consider only the first bit of each number. There are more 1 bits (7) than 0 bits (5), so keep only the 7 numbers with a 1 in the first position: 11110, 10110, 10111, 10101, 11100, 10000, and 11001.
        Then, consider the second bit of the 7 remaining numbers: there are more 0 bits (4) than 1 bits (3), so keep only the 4 numbers with a 0 in the second position: 10110, 10111, 10101, and 10000.
        In the third position, three of the four numbers have a 1, so keep those three: 10110, 10111, and 10101.
        In the fourth position, two of the three numbers have a 1, so keep those two: 10110 and 10111.
        In the fifth position, there are an equal number of 0 bits and 1 bits (one each). So, to find the oxygen generator rating, keep the number with a 1 in that position: 10111.
        As there is only one number left, stop; the oxygen generator rating is 10111, or 23 in decimal.

    Then, to determine the CO2 scrubber rating value from the same example above:

        Start again with all 12 numbers and consider only the first bit of each number. There are fewer 0 bits (5) than 1 bits (7), so keep only the 5 numbers with a 0 in the first position: 00100, 01111, 00111, 00010, and 01010.
        Then, consider the second bit of the 5 remaining numbers: there are fewer 1 bits (2) than 0 bits (3), so keep only the 2 numbers with a 1 in the second position: 01111 and 01010.
        In the third position, there are an equal number of 0 bits and 1 bits (one each). So, to find the CO2 scrubber rating, keep the number with a 0 in that position: 01010.
        As there is only one number left, stop; the CO2 scrubber rating is 01010, or 10 in decimal.

    Finally, to find the life support rating, multiply the oxygen generator rating (23) by the CO2 scrubber rating (10) to get 230.

    Use the binary numbers in your diagnostic report to calculate the oxygen generator rating and CO2 scrubber rating, then multiply them together. What is the life support rating of the submarine? (Be sure to represent your answer in decimal, not binary.)
    """
    bin_len = len(inp_items[0])

    o2_gen = get_ratings(inp_items, bin_len, MAX)
    co2_gen = get_ratings(inp_items, bin_len, MIN)
    print(o2_gen * co2_gen)


if __name__ == "__main__":
    test_input = [
                    '00100', '11110', '10110', '10111', '10101',
                    '01111', '00111', '11100', '10000', '11001',
                    '00010', '01010'
                ]
    input_items = read_input_file(INPUT_DATA_FILE)
    # input_items = test_input
    puzzle1(input_items)
    puzzle2(input_items)
