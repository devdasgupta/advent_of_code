from pathlib import Path
from utils import read_input_file
file_path = Path(__file__).parent.absolute()
INPUT_DATA_FILE = f'{file_path}/day1_input'


def get_increase_count(inp_items: list):
    first_measurement = inp_items[:-1]
    second_measurement = inp_items[1:]

    increase_count = 0

    for first, second in zip(first_measurement, second_measurement):
        if second > first:
            increase_count += 1

    return increase_count

def puzzle1(input_items: list):
    """
    This report indicates that, scanning outward from the submarine, the sonar sweep found depths of 199, 200, 208, 210, and so on.

    The first order of business is to figure out how quickly the depth increases, just so you know what you're dealing with - you never know if the keys will get carried into deeper water by an ocean current or a fish or something.

    To do this, count the number of times a depth measurement increases from the previous measurement. (There is no measurement before the first measurement.) In the example above, the changes are as follows:

        199 (N/A - no previous measurement)
        200 (increased)
        208 (increased)
        210 (increased)
        200 (decreased)
        207 (increased)
        240 (increased)
        269 (increased)
        260 (decreased)
        263 (increased)

        In this example, there are 7 measurements that are larger than the previous measurement.

        How many measurements are larger than the previous measurement?
    """
    increase_count = get_increase_count(input_items)
    print("Puzzle1: ", increase_count)

def puzzle2(input_items: list):
    """
    Start by comparing the first and second three-measurement windows. The measurements in the first window are marked A (199, 200, 208); their sum is 199 + 200 + 208 = 607. The second window is marked B (200, 208, 210); its sum is 618. The sum of measurements in the second window is larger than the sum of the first, so this first comparison increased.

    Your goal now is to count the number of times the sum of measurements in this sliding window increases from the previous sum. So, compare A with B, then compare B with C, then C with D, and so on. Stop when there aren't enough measurements left to create a new three-measurement sum.

    In the above example, the sum of each three-measurement window is as follows:

    A: 607 (N/A - no previous sum)
    B: 618 (increased)
    C: 618 (no change)
    D: 617 (decreased)
    E: 647 (increased)
    F: 716 (increased)
    G: 769 (increased)
    H: 792 (increased)

    In this example, there are 5 sums that are larger than the previous sum.

    Consider sums of a three-measurement sliding window. How many sums are larger than the previous sum?
    """
    cumulated_list = []
    for idx in range(0, len(input_items[:-2]), 1):
        cumulated_list.append(sum(input_items[idx:idx+3]))

    print(cumulated_list)
    increase_count = get_increase_count(cumulated_list)
    print("Puzzle2: ", increase_count)


if __name__ == "__main__":

    test_input = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    # input_items = read_input_file(test_input=test_input)
    input_items = read_input_file(INPUT_DATA_FILE)
    input_items = [int(x) for x in input_items]

    # puzzle1(input_items)
    puzzle2(input_items)
