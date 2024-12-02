"""
Santa's previous password expired, and he needs help choosing a new one.

To help him remember his new password after the old one expires, Santa has devised a method of coming up with a password based on the previous one. Corporate policy dictates that passwords must be exactly eight lowercase letters (for security reasons), so he finds his new password by incrementing his old password string repeatedly until it is valid.

Incrementing is just like counting with numbers: xx, xy, xz, ya, yb, and so on. Increase the rightmost letter one step; if it was z, it wraps around to a, and repeat with the next letter to the left until one doesn't wrap around.

Unfortunately for Santa, a new Security-Elf recently started, and he has imposed some additional password requirements:

    Passwords must include one increasing straight of at least three letters, like abc, bcd, cde, and so on, up to xyz. They cannot skip letters; abd doesn't count.
    Passwords may not contain the letters i, o, or l, as these letters can be mistaken for other characters and are therefore confusing.
    Passwords must contain at least two different, non-overlapping pairs of letters, like aa, bb, or zz.

For example:

    hijklmmn meets the first requirement (because it contains the straight hij) but fails the second requirement requirement (because it contains i and l).
    abbceffg meets the third requirement (because it repeats bb and ff) but fails the first requirement.
    abbcegjk fails the third requirement, because it only has one double letter (bb).
    The next password after abcdefgh is abcdffaa.
    The next password after ghijklmn is ghjaabcc, because you eventually skip all the passwords that start with ghi..., since i is not allowed.

Given Santa's current password (your puzzle input), what should his next password be?

Your puzzle input is hepxcrrq.
"""

import re
from itertools import product

def increment_char(_char: str, value: int = 1):
    if value == 0:
        return _char, value
    try:
        res = ord(_char) + value
        res, carry = ((res - ord("z") - 1 + ord("a") ), 1 ) \
            if res > ord("z") else (res, 0)
    except TypeError as e:
        raise e
    
    return chr(res), carry


def increment_str(_str: str, value: int = 1):
    new_password = []
    carry = value

    for char in _str[::-1]:
        res, carry = increment_char(char, carry)
        new_password.append(res)

    return ''.join(new_password[::-1])


def series3(pwd: str) -> bool:
    ascii = list(map(ord, list(pwd)))
    val = [(ascii[i - 2], ascii[i - 1], ascii[i]) for i in range(2, len(ascii), 1)]
    res = list(map(lambda x: x[2] - x[1] == 1 and x[1] - x[0] == 1, val))

    return any(res)


def non_overlapping_pairs(pwd: str) -> bool:
    res = re.findall(r"([a-z])\1", pwd)
    
    return len(set(res)) > 1
    # return True


def is_valid_pwd(pwd: str) -> bool:
    try:
        assert len(pwd) == 8 # Check 1

        assert series3(pwd) # Check 2

        invalid_chars = set('iol')
        assert len(set(pwd).intersection(invalid_chars)) == 0 # Check 3

        assert non_overlapping_pairs(pwd) # Check 4

        return True
    except AssertionError as e:
        return False


def part1(old_pwd):
    
    flag = False

    new_pwd = increment_str(old_pwd)

    while not flag:
        # print(new_pwd)
        flag = is_valid_pwd(new_pwd)
        new_pwd = new_pwd if flag else increment_str(new_pwd)

    return new_pwd

"""
--- Part Two ---

Santa's password expired again. What's the next one?

"""


"""
Different Solution
"""
letters = "abcdefghjkmnpqrstuvwxyz"
triplets = set("".join(triplet) for triplet in zip(letters, letters[1:], letters[2:]))
r = re.compile(r"([a-z])\1.*([a-z])\2")
# r = re.compile(rf"([{letters}])\1.*([{letters}])\2")

def solve(password):
    found = None

    for i in range(1, len(password) + 1):
        if password[-i] == letters[-1]:
            next # No idea what this is doing

        prefix = password[:-i]
        print(i, letters[letters.index(password[-i]) + 1 :])
        for suffix in product(letters[letters.index(password[-i]) + 1 :], *([letters] * (i - 1))):
            # print(suffix)
            candidate = prefix + "".join(suffix)
            if r.search(candidate) and any(candidate[j : j + 3] in triplets for j in range(len(candidate) - 2)):
                found = candidate
                break

        if found is not None:
            break

    return found

if __name__=="__main__":
    old_pwd = "hepxcrrq"
    # x = part1(old_pwd)
    # print(x)
    # y = part1(x)
    # print(y)
    z = solve(old_pwd)
    print(z)