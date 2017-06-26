#!/usr/bin/env python3

import json
import sys

DELTA_THRESHOLD = 1.03
PRIZE_PART = 0.998

INPUT = sys.argv[1]
CURRENCIES = ("btc", "ltc", "eth", "dsh")


def get_datas():
    previous_timestamp = None
    for line in open(INPUT):
        data = json.loads(line)
        timestamp = next(iter(data.values()))['updated']
        if previous_timestamp and timestamp - previous_timestamp < 43200:
            continue
        previous_timestamp = timestamp
        yield dict((key, value['last']) for key, value in data.items())


def get_all_deltas(base, previous, current):
    for key in current.keys():
        if key.startswith(base):
            yield key, current[key] / previous[key]
        if key.endswith(base):
            yield key, previous[key] / current[key]


def get_preferred_deltas(base, deltas):
    return filter(lambda item: any(currency != base and currency in item[0] for currency in CURRENCIES), deltas)


def run():
    datas = tuple(get_datas())
    balance = {"btc": 0.1}
    previous = datas[0]
    for current in datas[1:]:
        base = tuple(balance.keys())[0]
        deltas = get_preferred_deltas(base, get_all_deltas(base, previous, current))
        pair, value = max(deltas, key=lambda item: item[1])
        print("The best pair is %s with delta %s" % (pair, value))
        if value < DELTA_THRESHOLD:
            print("Price has been changed too low, skipping")
            continue
        if pair.startswith(base):
            currency = pair.split("_")[1]
            amount = balance[base] * current[pair] * PRIZE_PART
            print("Selling %s for %s, amount is %s" % (base, currency, amount))
            balance = {currency: amount}
        elif pair.endswith(base):
            currency = pair.split("_")[0]
            amount = balance[base] / current[pair] * PRIZE_PART
            print("Buying %s for %s, amount is %s" % (currency, base, amount))
            balance = {currency: amount}
        else:
            raise Exception("not supposed to happen")
        previous = current
    print("Final balance is %s" % balance)


if __name__ == '__main__':
    run()
