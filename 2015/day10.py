"""
Today, the Elves are playing a game called look-and-say. They take turns making sequences by reading aloud the previous sequence and using that reading as the next sequence. For example, 211 is read as "one two, two ones", which becomes 1221 (1 2, 2 1s).

Look-and-say sequences are generated iteratively, using the previous value as input for the next step. For each step, take the previous value, and replace each run of digits (like 111) with the number of digits (3) followed by the digit itself (1).

For example:

    1 becomes 11 (1 copy of digit 1).
    11 becomes 21 (2 copies of digit 1).
    21 becomes 1211 (one 2 followed by one 1).
    1211 becomes 111221 (one 1, one 2, and two 1s).
    111221 becomes 312211 (three 1s, two 2s, and one 1).

Starting with the digits in your puzzle input, apply this process 40 times. What is the length of the result?

Your puzzle input is 1321131112.
"""

str_inp = "1321131112"

def solve_str(str_inp):
    length = len(str_inp)

    count = 1
    final_res = []
    previous = str_inp[0]

    for idx in range(1, length, 1):
        current = str_inp[idx]

        if current == previous:
            count += 1
        else:
            final_res.append(str(count))
            final_res.append(previous)
            previous = current
            count = 1
    final_res.append(str(count))
    final_res.append(previous)

    return ''.join(final_res)


def part1():
    x = str_inp
    for _ in range(40):
        x = solve_str(x)
        # print(_, x)

    return len(x)

"""
Neat, right? You might also enjoy hearing John Conway talking about this sequence (that's Conway of Conway's Game of Life fame).

Now, starting again with the digits in your puzzle input, apply this process 50 times. What is the length of the new result?
"""
def part2():
    x = str_inp
    for _ in range(50):
        x = solve_str(x)
        # print(_, x)

    return len(x)

if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)