from collections import Iterable, namedtuple
from pathlib import Path

from utils import read_input_file

file_path = Path(__file__).parent.absolute()
INPUT_DATA_FILE = f'{file_path}/day4_input_boards'
BINGO_INPUTS = [
    99,56,7,15,81,26,75,40,87,59,62,24,58,34,78,86,44,65,18,94,20,17,98,57,92,
    14,32,46,79,85,84,35,68,55,22,41,61,90,11,69,96,23,47,43,80,72,50,97,33,53,
    25,28,51,49,64,12,63,21,48,27,19,67,88,66,45,3,71,16,70,76,13,60,77,73,1,
    8,10,52,38,36,74,83,2,37,6,31,91,89,54,42,30,5,82,9,95,93,4,0,39
]

def transpose_matrix(list_item: list) -> list:
    return list(zip(*list_item))

def remove_items_from_list(list_item: list, removal_item: int) -> list:
    return list(filter(lambda val: val != removal_item, list_item))

def flatten(items):
    for x in items:
        if isinstance(x, Iterable):
            yield from flatten(x)
        else:
            yield x


def calculate_score(input_board, bing):
    sum_unmarked_num = int(sum([x for x in flatten(input_board)]) / 2)
    return bing * sum_unmarked_num

def get_ordered_bingo_board(input_board, bingo_inputs):
    """
    This function gets the input and the bingo number inputs and returns
    a list of bingo boards in order of winning occurrences
    """
    score = 0
    bingo_boards = []
    winner_boards = namedtuple('winner_boards', 'board, step')
    # 1. For each board matrix append another transposed matrix to track
    # all horizontal and vertical values
    input_board = [x + transpose_matrix(x) for x in input_board]

    # Iterate through each bingo input
    for bing in bingo_inputs:
        # First pop out all items that match the bingo card
        input_board = [[remove_items_from_list(x, bing) for x in y] for y in input_board]

        # Secondly, check if anyone can say BINGO!
        check_board = [[len(x) for x in y] for y in input_board]

        flat_board = [x for x in flatten(check_board)]

        # Thirdly when first Bingo is met calculate score
        if 0 in flat_board:
            # Find the board which has empty list as one item
            win_board = [x for x in input_board if [] in x]

            # Remove the winning board from the input_board list
            input_board = [x for x in input_board if [] not in x]

            # Append the winning board to bingo boards
            bingo_boards.append(winner_boards(win_board, bing))

    return bingo_boards


def puzzle1(input_board, bingo_inputs):
    """
    The submarine has a bingo subsystem to help passengers (currently, you and
    the giant squid) pass the time. It automatically generates a random order
    in which to draw numbers and a random set of boards (your puzzle input).
    For example:

    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7

    After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no
    winners, but the boards are marked as follows (shown here adjacent to
    each other to save space):

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    After the next six numbers are drawn (17, 23, 2, 0, 14, and 21),
    there are still no winners:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    Finally, 24 is drawn:

    22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
     8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
    21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
     6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
     1 12 20 15 19        14 21 16 12  6         2  0 12  3  7

    At this point, the third board wins because it has at least one complete
    row or column of marked numbers (in this case, the entire
    top row is marked: 14 21 17 24 4).

    The score of the winning board can now be calculated. Start by finding
    the sum of all unmarked numbers on that board; in this case, the sum is 188.
    Then, multiply that sum by the number that was just called when the
    board won, 24, to get the final score, 188 * 24 = 4512.

    To guarantee victory against the giant squid, figure out which board will
    win first. What will your final score be if you choose that board?
    """
    first_winner = get_ordered_bingo_board(input_board, bingo_inputs)[0]
    score = calculate_score(*first_winner)
    print(score)


def puzzle2(input_board, bingo_inputs):
    """
    On the other hand, it might be wise to try a different strategy: let
    the giant squid win.

    You aren't sure how many bingo boards a giant squid could play at once,
    so rather than waste time counting its arms, the safe thing to do is to
    figure out which board will win last and choose that one. That way, no
    matter which boards it picks, it will win for sure.

    In the above example, the second board is the last to win, which happens
    after 13 is eventually called and its middle column is completely marked.
    If you were to keep playing until this point, the second board would have
    a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

    Figure out which board will win last. Once it wins, what would its final score be?
    """
    last_winner = get_ordered_bingo_board(input_board, bingo_inputs)[-2]
    score = calculate_score(*last_winner)
    print(score)

if __name__ == "__main__":
    test_bingo_input = [7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,
                        6,15,25,12,22,18,20,8,19,3,26,1]

    test_boards = [
        [
            [22, 13, 17, 11, 0],
            [8, 2, 23, 4, 24],
            [21, 9, 14, 16, 7],
            [6, 10, 3, 18, 5],
            [1, 12, 20, 15, 19]
        ],
        [
            [3, 15, 0, 2, 22],
            [9, 18, 13, 17, 5],
            [19, 8,  7, 25, 23],
            [20, 11, 10, 24, 4],
            [14, 21, 16, 12, 6]
        ],
        [
            [14, 21, 17, 24, 4],
            [10, 16, 15, 9, 19],
            [18, 8, 23, 26, 20],
            [22, 11, 13, 6, 5],
            [2, 0, 12, 3, 7]
        ],
    ]

    input_board = read_input_file(filepath=INPUT_DATA_FILE, delimiter='\n\n')
    input_board = [x.strip().split('\n') for x in input_board]
    input_board = [[x.strip().split() for x in y] for y in input_board]
    input_board = [[[int(x) for x in y] for y in z] for z in input_board]
    bingo_inputs = BINGO_INPUTS
    # input_board = test_boards
    # bingo_inputs = test_bingo_input

    puzzle1(input_board, bingo_inputs)
    puzzle2(input_board, bingo_inputs)
