#!/usr/bin/env python

import json
import sys

rounds = list(map(json.loads, open(sys.argv[1])))[-500:]
sums = [0, 0, 0, 0]
for a, b, c in zip(rounds, rounds[1:], rounds[2:]):
    if a['start_price'] < b['start_price'] and b['start_price'] < c['start_price']:
        sums[0] += 1
    if a['start_price'] < b['start_price'] and b['start_price'] > c['start_price']:
        sums[1] += 1
    if a['start_price'] > b['start_price'] and b['start_price'] > c['start_price']:
        sums[2] += 1
    if a['start_price'] > b['start_price'] and b['start_price'] < c['start_price']:
        sums[3] += 1
print(sums)
