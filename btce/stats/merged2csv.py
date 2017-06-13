#!/usr/bin/env python3

import csv
import json
import sys


writer = csv.DictWriter(sys.stdout, (
    'number',
    'start_time',
    'start_price',
    'end_price',
    'down_bets',
    'down_amount',
    'up_bets',
    'up_amount'
))
writer.writeheader()
for line in open(sys.argv[1]):
    data = json.loads(line)
    writer.writerow(dict(
        number=data['number'],
        start_time=data['start_time'],
        start_price=data['start_price'],
        end_price=data['end_price'],
        down_bets=data['bets'][1],
        down_amount=data['amounts'][1],
        up_bets=data['bets'][0],
        up_amount=data['amounts'][0]
    ))
