"""
This year, Santa brought little Bobby Tables a set of wires and bitwise logic gates! Unfortunately, little Bobby is a little under the recommended age range, and he needs help assembling the circuit.

Each wire has an identifier (some lowercase letters) and can carry a 16-bit signal (a number from 0 to 65535). A signal is provided to each wire by a gate, another wire, or some specific value. Each wire can only get a signal from one source, but can provide its signal to multiple destinations. A gate provides no signal until all of its inputs have a signal.

The included instructions booklet describes how to connect the parts together: x AND y -> z means to connect wires x and y to an AND gate, and then connect its output to wire z.

For example:

    123 -> x means that the signal 123 is provided to wire x.
    x AND y -> z means that the bitwise AND of wire x and wire y is provided to wire z.
    p LSHIFT 2 -> q means that the value from wire p is left-shifted by 2 and then provided to wire q.
    NOT e -> f means that the bitwise complement of the value from wire e is provided to wire f.

Other possible gates include OR (bitwise OR) and RSHIFT (right-shift). If, for some reason, you'd like to emulate the circuit instead, almost all programming languages (for example, C, JavaScript, or Python) provide operators for these gates.

For example, here is a simple circuit:

123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i

After it is run, these are the signals on the wires:

d: 72
e: 507
f: 492
g: 114
h: 65412
i: 65079
x: 123
y: 456

In little Bobby's kit's instructions booklet (provided as your puzzle input), what signal is ultimately provided to wire a?
"""
from typing import Dict
from pyparsing import Word, Literal, alphas, printables, Combine, OneOrMore, White, ZeroOrMore
from dataclasses import dataclass
from pathlib import Path
from functools import cache
from utils import read_input_file
import json
from operator import iand, ior, rshift, lshift


def test_data():
    _file = f"{Path(__file__).parent.absolute()}/day7_input"
    return read_input_file(_file)


ops = {"AND": iand, "OR": ior, "RSHIFT": rshift, "LSHIFT": lshift}
wires = {k: v.split() for line in test_data() for v, k in [line.strip().split(" -> ")]}

@dataclass
class Assembly:
    instruction: str

    def __post_init__(self):
        word = Word(alphas)
        operator = Literal("AND") | Literal("NOT") | Literal("RSHIFT") | Literal("OR") | Literal("LSHIFT")
        output = Literal("->")
        integer = Word("0123456789")
        white = White(" ", max=1)

        expression = (
            Combine(ZeroOrMore(integer | operator | word | white))
            + output
            + word
            )
        
        res = expression.parseString(self.instruction)
        self.key = res[2]
        self.value = res[0]

    def __repr__(self) -> str:
        return f"Rules: {self.rules}"
    

@cache
def evaluate(data_dict: Dict, search_element: str):
    if search_element.isdigit():
        return int(search_element)
    
    rule = data_dict.get(search_element).strip()
    print(f"{search_element} -> {rule}")
    
    if 'AND' in rule:
        vals = [x.strip() for x in rule.split()]
        x1 = evaluate(data_dict, vals[0])
        # print(f"Return value 1: {x1}")
        x2 = evaluate(data_dict, vals[2])
        # print(f"Return value 2: {x2}")
        return iand(x1, x2)
    elif 'NOT' in rule:
        vals = [x.strip() for x in rule.split()]
        x1 = evaluate(data_dict, vals[1])
        # print(f"Return value 1: {x1}")
        return ~x1 & 65535
    elif 'OR' in rule:
        vals = [x.strip() for x in rule.split()]
        x1 = evaluate(data_dict, vals[0])
        # print(f"Return value 1: {x1}")
        x2 = evaluate(data_dict, vals[2])
        # print(f"Return value 2: {x2}")
        return ior(x1, x2)
    elif 'RSHIFT' in rule:
        vals = [x.strip() for x in rule.split()]
        x1 = evaluate(data_dict, vals[0])
        # print(f"Return value 1: {x1}")
        x2 = evaluate(data_dict, vals[2])
        # print(f"Return value 2: {x2}")
        return irshift(x1, x2)
    elif 'LSHIFT' in rule:
        vals = [x.strip() for x in rule.split()]
        x1 = evaluate(data_dict, vals[0])
        # print(f"Return value 1: {x1}, x{type(vals[2])}x")
        x2 = evaluate(data_dict, vals[2])
        # print(f"Return value 2: {x2}")
        return ilshift(x1, x2)
    else:
        return evaluate(data_dict, rule)


@cache
def solve(wire):
    if wire.isdigit():
        return int(wire)
    
    ins = wires[wire]
    
    if len(ins) == 3:
        return ops[ins[1]](solve(ins[0]), solve(ins[2]))
    elif len(ins) == 2:
        return ~solve(ins[1]) & 65535
    else:
        return solve(ins[0])
    

def part1():
    data = test_data()

    process_data = {}
    for _ in data:
        val = Assembly(_)
        process_data[val.key] = val.value.strip()

    
    solve.cache_clear()
    return solve('a')
    

def part2():
    wires["b"] = wires["a"]

    solve.cache_clear()
    return solve('a')


if __name__ == "__main__":
    x = part1()
    print(x)

    y = part2()
    print(y)

    