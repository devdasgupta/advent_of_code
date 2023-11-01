"""Santa needs help figuring out which strings in his text file are naughty or nice.

A nice string is one with all of the following properties:

    It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.

For example:

    ugknbfddgicrmopn is nice because it has at least three vowels (u...i...o...), a double letter (...dd...), and none of the disallowed substrings.
    aaa is nice because it has at least three vowels and a double letter, even though the letters used by different rules overlap.
    jchzalrnumimnmhp is naughty because it has no double letter.
    haegwjzuvuyypxyu is naughty because it contains the string xy.
    dvszwmarrgswjxmb is naughty because it contains only one vowel.

How many strings are nice?
"""
import re
from pathlib import Path
from utils import read_regular_file

def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day5_input"
    data = read_regular_file(_file)
    return data.strip().split("\n")

def validate_string(data_str: str):
    check1 = len(re.findall('[aeiou]', data_str)) >= 3
    if not check1:
        return check1
    
    check2 = any([data_str[x] == data_str[x + 1] for x in range(len(data_str) - 1)])
    if not check2:
        return check2

    check3 = len(re.findall("ab|cd|pq|xy", data_str)) == 0
    if not check3:
        return check3
    
    return True


def validate_string_regex(data_str: str):
    """
    Note: In regex term anything define in P is called as a placeholder
    """
    regex = re.compile(
        r"^"
        r"(?=(.*[aeiou]){3})"           # check 1
        r"(?=.*(?P<twin>.)(?P=twin))"   # check 2
        r"(?!.*(ab|cd|pq|xy))"          # check 3
    )

    return bool(regex.search(data_str))


def part1():
    data = test_data()
    res = [1 for x in data if validate_string(x)]

    return sum(res)


"""
Realizing the error of his ways, Santa has switched to a better model of determining whether a string is naughty or nice. None of the old rules apply, as they are all clearly ridiculous.

Now, a nice string is one with all of the following properties:

    It contains a pair of any two letters that appears at least twice in the string without overlapping, like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.

For example:

    qjhvhtzxzqqjkmpb is nice because is has a pair that appears twice (qj) and a letter that repeats with exactly one letter between them (zxz).
    xxyxx is nice because it has a pair that appears twice and a letter that repeats with one between, even though the letters used by each rule overlap.
    uurcxstgmygtbstg is naughty because it has a pair (tg) but no repeat with a single letter between them.
    ieodomkazucvgmuy is naughty because it has a repeating letter with one between (odo), but no pair that appears twice.

How many strings are nice under these new rules?
"""

def validate_string_2(data_str: str):

    check1 = len(re.findall(".*(?P<twins>..).*(?P=twins)", data_str)) > 0
    if not check1:
        return check1
    
    check2 = any([data_str[x] == data_str[x + 2] for x in range(len(data_str) - 2)])
    if not check2:
        return check2
    
    return True


def validate_string_regex_2(data_str: str):
    """
    Note: In regex term anything define in P is called as a placeholder
    """
    regex = re.compile(
        r"^"
        r"(?=.*(?P<twins>..).*(?P=twins))"  # check 1
        r"(?=.*(?P<repeat>.).(?P=repeat))"  # check 2
    )

    return bool(regex.search(data_str))


def part2():
    data = test_data()
    res = [1 for x in data if validate_string_2(x)]

    return sum(res)


if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)
    