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
