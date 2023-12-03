from typing import Optional

def read_input_file(filepath: Optional = None, delimiter: str = '\n', test_input: list = None) -> list:
    if test_input:
        return test_input
    else:
        with open(filepath, 'r') as fr:
            val = fr.read()

        val = [x for x in val.strip().split(delimiter)]

        return val

def read_regular_file(filepath: str):
    with open(filepath, 'r') as fr:
        data = fr.read()
    
    return data

def prRed(skk): 
    print("\033[91m {}\033[00m" .format(skk))
 
 
def prGreen(skk): 
    print("\033[92m {}\033[00m" .format(skk))
 
 
def prYellow(skk): 
    print("\033[93m {}\033[00m" .format(skk))
 
 
def prLightPurple(skk): 
    print("\033[94m {}\033[00m" .format(skk))
 
 
def prPurple(skk): 
    print("\033[95m {}\033[00m" .format(skk))
 
 
def prCyan(skk): 
    print("\033[96m {}\033[00m" .format(skk))
 
 
def prLightGray(skk): 
    print("\033[97m {}\033[00m" .format(skk))
 
 
def prBlack(skk): 
    print("\033[98m {}\033[00m" .format(skk))