'''
The automatic passport scanners are slow because they're having trouble detecting which passports have all required fields. The expected fields are as follows:

    byr (Birth Year)
    iyr (Issue Year)
    eyr (Expiration Year)
    hgt (Height)
    hcl (Hair Color)
    ecl (Eye Color)
    pid (Passport ID)
    cid (Country ID)

Passport data is validated in batch files (your puzzle input). Each passport is represented as a sequence of key:value pairs separated by spaces or newlines. Passports are separated by blank lines.

Here is an example batch file containing four passports:

ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in

The first passport is valid - all eight fields are present. The second passport is invalid - it is missing hgt (the Height field).

The third passport is interesting; the only missing field is cid, so it looks like data from North Pole Credentials, not a passport at all! Surely, nobody would mind if you made the system temporarily ignore missing cid fields. Treat this "passport" as valid.

The fourth passport is missing two fields, cid and byr. Missing cid is fine, but missing any other field is not, so this passport is invalid.

According to the above rules, your improved system would report 2 valid passports.

Count the number of valid passports - those that have all required fields. Treat cid as optional. In your batch file, how many passports are valid?
'''

'''
--- Part Two ---

The line is moving more quickly now, but you overhear airport security talking about how passports with invalid data are getting through. Better add some data validation, quick!

You can continue to ignore the cid field, but each other field has strict rules about what values are valid for automatic validation:

    byr (Birth Year) - four digits; at least 1920 and at most 2002.
    iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    hgt (Height) - a number followed by either cm or in:
        If cm, the number must be at least 150 and at most 193.
        If in, the number must be at least 59 and at most 76.
    hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    pid (Passport ID) - a nine-digit number, including leading zeroes.
    cid (Country ID) - ignored, missing or not.

Your job is to count the passports where all required fields are both present and valid according to the above rules.
'''

import os
import re
from itertools import compress

mandatory_fields = {
    'byr': r'^(19[2-9][0-9]|200[0-2])$',
    'iyr': r'^(201[0-9]|2020)$',
    'eyr': r'^(202[0-9]|2030)$',
    'hgt': r'^(1[5-8][0-9]cm|19[0-3]cm|59in|6[0-9]in|7[0-6]in)$',
    'hcl': r'^#([0-9a-f]{6})$',
    'ecl': r'(amb|blu|brn|gry|grn|hzl|oth)',
    'pid': r'^([0-9]{9})$'
}

def is_valid_passport(passport):
    return all(passport.get(x, False) for x in mandatory_fields.keys())

def is_valid_passport_data(passport):
    return all(re.match(val, passport[key]) for key, val in mandatory_fields.items())

def get_passport_list_from_batch(batch_items):
    return batch_items.strip().split('\n\n')

def get_passport_dict(passport):
    items = [x.split(':') for x in re.split(' |\\n', passport)]
    return {x[0]: x[1] for x in items}

def get_valid_passport_count(batch):
    passport_list = [get_passport_dict(passport) for passport in get_passport_list_from_batch(batch)]
    all_passport_status = [is_valid_passport(passport) for passport in passport_list]
    valid_passports = compress(passport_list, all_passport_status)
    # print(list(valid_passports))
    all_passport_data_status = [is_valid_passport_data(passport) for passport in valid_passports]

    return sum(all_passport_status), sum(all_passport_data_status)


def test_rule(rule, value):
    regex = mandatory_fields[rule]
    return all([re.match(regex, value)])

def test_part2():
    for x in range(1920, 2002):
        assert test_rule('byr', str(x))

    assert not test_rule('byr', '1919')
    assert not test_rule('byr', '2003')

    regex = mandatory_fields['iyr']
    for x in range(2010, 2020):
        assert all([re.match(regex, str(x))])

    assert re.match(regex, '1919') == None
    assert re.match(regex, '2023') == None

    regex = mandatory_fields['eyr']
    for x in range(2020, 2030):
        assert all([re.match(regex, str(x))])

    assert re.match(regex, '2019') == None
    assert re.match(regex, '2031') == None

    regex = mandatory_fields['hgt']
    for x in range(150, 193):
        assert all([re.match(regex, f'{x}cm')])

    for x in range(59, 76):
        assert all([re.match(regex, f'{x}in')])

    assert re.match(regex, '60') == None
    assert re.match(regex, '160') == None
    assert re.match(regex, '58in') == None
    assert re.match(regex, '77in') == None
    assert re.match(regex, '149cm') == None
    assert re.match(regex, '194cm') == None

    regex = mandatory_fields['ecl']
    assert all(re.match(regex, x) for x in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])
    assert re.match(regex, 'abc') == None



if __name__ == "__main__":

    file_path = f'{os.path.dirname(os.path.realpath(__file__))}/day4_puzzle_input'

    with open(file_path) as fr:
        batch = fr.read()

    part_1, part_2 = get_valid_passport_count(batch)
    print(part_1)
    print(part_2)

    test_part2()
