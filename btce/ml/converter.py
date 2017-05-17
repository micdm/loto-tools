#!/usr/bin/env python

import csv
from datetime import datetime
import json
import sys


def get_day_of_week(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').weekday()


def get_time_of_day(timestamp):
    time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    return time.hour * 60 + time.minute


writer = csv.DictWriter(sys.stdout, (
    'down_amount',
    'up_amount',
    'down_bets',
    'up_bets',
    'day_of_week',
    'minute_of_day',
    # 'is_increased',
    'result'
))
writer.writeheader()
lines = list(open(sys.argv[1]))
for line1, line2 in zip(lines, lines[1:]):
    data1 = json.loads(line1)
    data2 = json.loads(line2)
    writer.writerow(dict(
        down_amount=data2['amounts'][1],
        up_amount=data2['amounts'][0],
        down_bets=data2['bets'][1],
        up_bets=data2['bets'][0],
        day_of_week=get_day_of_week(data2['start_time']),
        minute_of_day=get_time_of_day(data2['start_time']),
        # is_increased=int(data2['start_price'] > data1['start_price']),
        result=int(data2['end_price'] > data2['start_price'])
    ))
