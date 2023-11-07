"""
Santa needs help mining some AdventCoins (very similar to bitcoins) to use as gifts for all the economically forward-thinking little girls and boys.

To do this, he needs to find MD5 hashes which, in hexadecimal, start with at least five zeroes. The input to the MD5 hash is some secret key (your puzzle input, given below) followed by a number in decimal. To mine AdventCoins, you must find Santa the lowest positive number (no leading zeroes: 1, 2, 3, ...) that produces such a hash.

For example:

    If your secret key is abcdef, the answer is 609043, because the MD5 hash of abcdef609043 starts with five zeroes (000001dbbfa...), and it is the lowest such number to do so.
    If your secret key is pqrstuv, the lowest number it combines with to make an MD5 hash starting with five zeroes is 1048970; that is, the MD5 hash of pqrstuv1048970 looks like 000006136ef....

Your puzzle input is iwrupvqb.
"""

import hashlib
from itertools import count

def get_hash(val: str) -> str:
    res = hashlib.md5(val.encode())
    return str(res.hexdigest())


def part1(pattern: str):
    input = "iwrupvqb"
    # input = "pqrstuv"

    for i in count(1):
        data = f"{input}{i}"
        val = get_hash(data)

        if val.startswith(pattern):
            print(data, val, i)
            break

    return i

if __name__ == "__main__":
    x = part1("00000")
    print(x)

    x = part1("000000")
    print(x)
