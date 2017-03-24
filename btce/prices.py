#!/usr/bin/env python
# curl https://btc-e.nz/api/3/ticker/ltc_rur-eth_rur-eth_btc-dsh_btc-nmc_usd-ppc_usd-nmc_btc-dsh_usd-eur_usd-eth_eur-ltc_usd-nvc_btc-dsh_eur-usd_rur-ltc_eur-btc_usd-ltc_btc-eth_ltc-ppc_btc-btc_eur-dsh_rur-eth_usd-nvc_usd-dsh_ltc-eur_rur-btc_rur-dsh_eth > data/last.data 2> /dev/null && curl https://btc-e.nz/api/3/info > data/info.data 2> /dev/null && python3 prices.py data/last.data data/info.data

from decimal import Decimal, ROUND_DOWN
import json
import sys


QUANTIZE_VALUE = Decimal('0.0001')
START_CURRENCY = 'usd'
START_AMOUNT = Decimal('1')
PRICE_PART = Decimal('0.998')


def handle_tick(prices: dict, limits: dict):
    moves = {}
    for key, price in prices.items():
        currency1, currency2 = key.split('_')
        moves[(currency1, currency2)] = price
        moves[(currency2, currency1)] = 1 / price
    return max(get_profit_chains(moves, limits), key=lambda values: values[1] / len(values[0]))


def get_profit_chains(moves, limits):
    chains = [(START_CURRENCY,)]
    while chains:
        chain = chains.pop()
        for pair, price in moves.items():
            if chain[-1] == pair[0]:
                new_chain = chain + (pair[1],)
                if pair[1] == START_CURRENCY:
                    profit = get_chain_profit(new_chain, moves, limits)
                    if profit > 1:
                        yield new_chain, profit
                elif pair[1] not in chain:
                    chains.append(new_chain)


def get_chain_profit(chain, moves, limits):
    amount = START_AMOUNT
    for pair in zip(chain[:-1], chain[1:]):
        amount = (amount * moves[pair] * PRICE_PART).quantize(limits[pair], rounding=ROUND_DOWN)
    return (amount / START_AMOUNT).quantize(QUANTIZE_VALUE)


limits = {}
for key, info in json.load(open(sys.argv[2]))['pairs'].items():
    currency1, currency2 = key.split('_')
    value = Decimal('0.' + '0' * (info['decimal_places'] - 1) + '1')
    limits[(currency1, currency2)] = value
    limits[(currency2, currency1)] = value
for line in open(sys.argv[1]):
    data = json.loads(line)
    print(handle_tick(dict((key, Decimal(value['last'])) for key, value in data.items()), limits))
