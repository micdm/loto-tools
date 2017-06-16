#!/usr/bin/env python3

import json
import sys

DELTA_THRESHOLD = 1.05
PRIZE_PART = 0.998

INPUT = sys.argv[1]
CURRENCIES = ("btc", "ltc", "eth", "dsh")


def get_pairs_as_first(first):
    for currency in CURRENCIES:
        key = "%s_%s" % (first, currency)
        if key in current:
            yield key


def get_pairs_as_second(second):
    for currency in CURRENCIES:
        key = "%s_%s" % (currency, second)
        if key in current:
            yield key


balance = {"btc": 0.1}
datas = tuple(map(lambda item: dict((key, value["last"]) for key, value in item.items()), (json.loads(line) for line in open(INPUT))))
for previous, current in zip(datas, datas[1:]):
    base = tuple(balance.keys())[0]
    pairs_as_first = tuple(get_pairs_as_first(base))
    pairs_as_second = tuple(get_pairs_as_second(base))
    if pairs_as_first:
        pair = max(pairs_as_first, key=lambda key: current[key] / previous[key])
        if current[pair] < previous[pair]:
            print("Price has been decreased, skipping")
        elif current[pair] / previous[pair] < DELTA_THRESHOLD:
            print("Price has been increased too low (%s), skipping" % (current[pair] / previous[pair]))
        else:
            currency = pair.split("_")[1]
            amount = (balance[base] * current[pair]) * PRIZE_PART
            print("Selling %s for %s, amount is %s, delta is %s" % (base, currency, amount, current[pair] / previous[pair]))
            balance = {currency: amount}
    elif pairs_as_second:
        pair = max(pairs_as_second, key=lambda key: previous[key] / current[key])
        if current[pair] > previous[pair]:
            print("Price has been increased, skipping")
        elif previous[pair] / current[pair] < DELTA_THRESHOLD:
            print("Price has been decreased too low (%s), skipping" % (previous[pair] / current[pair]))
        else:
            currency = pair.split("_")[0]
            amount = (balance[base] / current[pair]) * PRIZE_PART
            print("Buying %s for %s, amount is %s, delta is %s" % (currency, base, amount, previous[pair] / current[pair]))
            balance = {currency: amount}
print("Final balance is %s" % balance)
