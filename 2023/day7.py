"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

    Five of a kind, where all five cards have the same label: AAAAA
    Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    High card, where all cards' labels are distinct: 23456

Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

    32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
    KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
    T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""

from utils import read_input_file
from pathlib import Path
from typing import List
from collections import Counter

def test_data():
    file_path = f"{Path(__file__).parent.absolute()}/day7_input"
    data = {}
    for x in read_input_file(file_path):
        hand, bet = x.split()
        data[hand] = int(bet)

    return data


def get_hand_type(hand: str, joker) -> int:
    """
    Returns whether the hand is five of a kind, four of a kind, full house etc.
    """
    hand_value = {
        "Five of a kind": 7,
        "Four of a kind": 6,
        "Full house": 5,
        "Three of a kind": 4,
        "Two pair": 3,
        "One pair": 2,
        "High card": 1
    }
    val = Counter(hand)

    if joker:
        if set(val.values()) == {5}:
            return hand_value["Five of a kind"]
        elif set(val.values()) == {4, 1}:
            if joker in val.keys() and val[joker] == 4:
                return hand_value["Four of a kind"]
            else:
                return hand_value["Five of a kind"]
        elif set(val.values()) == {2, 3}:
            if joker in val.keys():
                return hand_value["Five of a kind"]
            else:
                return hand_value["Full house"]
        elif set(val.values()) == {1, 3}:
            if joker in val.keys() and val[joker] == 3:
                return hand_value["Three of a kind"]
            else:
                return hand_value["Four of a kind"]
        elif set(val.values()) == {1, 2} and len(val) == 3:
            if joker in val.keys():
                if val[joker] == 2:
                    return hand_value["Four of a kind"]
                else:
                    return hand_value["Full house"]
            else:
                return hand_value["Two pair"]
        elif set(val.values()) == {1, 2} and len(val) == 4:
            if joker in val.keys():
                return hand_value["Three of a kind"]
            else:
                return hand_value["One pair"]
        else:
            if joker in val.keys():
                return hand_value["One pair"]
            else:
                return hand_value["High card"]
    else:
        if set(val.values()) == {5}:
            return hand_value["Five of a kind"]
        elif set(val.values()) == {4, 1}:
            return hand_value["Four of a kind"]
        elif set(val.values()) == {2, 3}:
            return hand_value["Full house"]
        elif set(val.values()) == {1, 3}:
            return hand_value["Three of a kind"]
        elif set(val.values()) == {1, 2} and len(val) == 3:
            return hand_value["Two pair"]
        elif set(val.values()) == {1, 2} and len(val) == 4:
            return hand_value["One pair"]
        else:
            return hand_value["High card"]


def is_greater(hand_1, hand_2, joker) -> bool:
    if joker:
        hand_value = {
            "A": 13, "K": 12, "Q": 11, "T": 10, "9": 9, "8": 8,
            "7": 7, "6": 6, "5": 5, "4": 4, "3": 3, "2": 2, "J": 1
            }
    else:
        hand_value = {
            "A": 13, "K": 12, "Q": 11, "J": 10, "T": 9, "9": 8,
            "8": 7, "7": 6, "6": 5, "5": 4, "4": 3, "3": 2, "2": 1
            }
    
    if get_hand_type(hand_1, joker) == get_hand_type(hand_2, joker):
        for h1, h2 in zip(hand_1, hand_2):
            if h1 == h2:
                continue
            else:
                return hand_value[h1] > hand_value[h2]
    else:
        return get_hand_type(hand_1, joker) > get_hand_type(hand_2, joker)
    

def sorted_hand(array: List, joker) -> List:
    """
    Implementing Bubble Sort algorith here
    """
    n = len(array)

    for i in range(n):
        # Create a flag that will allow the function to
        # terminate early if there's nothing left to sort
        already_sorted = True

        # Start looking at each item of the list one by one,
        # comparing it with its adjacent value. With each
        # iteration, the portion of the array that you look at
        # shrinks because the remaining items have already been
        # sorted.
        for j in range(n - i - 1):
            if is_greater(array[j], array[j + 1], joker):
                # If the item you're looking at is greater than its
                # adjacent value, then swap them
                array[j], array[j + 1] = array[j + 1], array[j]

                # Since you had to swap two elements,
                # set the `already_sorted` flag to `False` so the
                # algorithm doesn't finish prematurely
                already_sorted = False

        # If there were no swaps during the last iteration,
        # the array is already sorted, and you can terminate
        if already_sorted:
            break

    return array
        

def get_total_winning(joker = None):
    data = test_data()
    # data = {"32T3K": 765, "T55J5": 684, "KK677": 28, "KTJJT": 220, "QQQJA": 483}
    hands = list(data.keys())
    s_hand = sorted_hand(hands, joker)

    overall_score = 0
    for rank, h in enumerate(s_hand, start=1):
        overall_score += rank * data[h]

    for s in s_hand:
        print(s)

    return overall_score

def part1():
    return get_total_winning()

def alternate_part1():
    data = test_data()

    return sum(
        rank0 * bid
        for rank0, (*_, bid) in enumerate(
            sorted(
                (
                    max(Counter(hand).values()) - len(set(hand)),
                    *map("23456789TJQKA".index, hand),
                    int(str_bid), 
                )
                for hand, str_bid in data.items()
            ),
            start=1
        )
    )


"""
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483

    32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
    KK677 is now the only two pair, making it the second-weakest hand.
    T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.

With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?
"""
def alternate_part2():

    data = test_data()

    joker = "J"

    return sum(
        rank0 * bid
        for rank0, (*_, bid) in enumerate(
            sorted(
                (
                    max(0, 0, *map(hand.count, set(hand) - {joker})) + hand.count(joker),
                    -(max(1, len(set(hand) - {joker}))),
                    *map("J23456789TQKA".index, hand),
                    int(str_bid),
                )
                for hand, str_bid in data.items()
            ),
            start=1
        )
    )


if __name__ == "__main__":
    x = part1()
    print(x)
    print(alternate_part1())

    y = part2()
    print(y)
    
    print(alternate_part2())
