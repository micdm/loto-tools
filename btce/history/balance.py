#!/usr/bin/env python3

from decimal import Decimal
import json
import sys

amounts = {}
for line in open(sys.argv[1]):
    data = json.loads(line)
    if data['time'] < '2017-06-01T00:00:00Z' or 'betting' in data['description']:
        continue
    currency = data['currency']
    if currency not in amounts:
        amounts[currency] = Decimal(0)
    amounts[currency] += Decimal(data['amount'])
print(amounts)
