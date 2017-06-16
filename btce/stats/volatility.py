#!/usr/bin/env python3

import json
import sys

INPUT = sys.argv[1]
PAIR = sys.argv[2]
DELTA = float(sys.argv[3])

count = 0
last = None
for line in open(INPUT):
    try:
        price = json.loads(line)[PAIR]["last"]
    except:
        continue
    if last is None:
        last = price
    elif abs(price - last) / last >= DELTA:
        count += 1
        last = price
print(count)
