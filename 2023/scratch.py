import sys
import re
from collections import defaultdict, Counter

D = open(sys.argv[1]).read().strip()
L = D.split("\n")

GO = {'L': {}, 'R': {}}
steps, rule = D.split("\n\n")

for line in rule.split("\n"):
    st, lr = line.split("=")
    st = st.strip()
    left, right = lr.split(",")

    left = left.strip()[1:].strip()
    right = right[:-1].strip()
    GO["L"][st] = left
    GO["R"][st] = right

print(GO)