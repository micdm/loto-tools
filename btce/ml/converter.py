#!/usr/bin/env python

import csv
from datetime import datetime
import json
import sys


class MainConverter:

    def __init__(self, source):
        self._source = source

    def convert(self):
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
        for line1, line2 in zip(self._source, self._source[1:]):
            data1 = json.loads(line1)
            data2 = json.loads(line2)
            writer.writerow(dict(
                down_amount=data2['amounts'][1],
                up_amount=data2['amounts'][0],
                down_bets=data2['bets'][1],
                up_bets=data2['bets'][0],
                day_of_week=self._get_day_of_week(data2['start_time']),
                minute_of_day=self._get_time_of_day(data2['start_time']),
                # is_increased=int(data2['start_price'] > data1['start_price']),
                result=int(data2['end_price'] > data2['start_price'])
            ))

    def _get_day_of_week(self, timestamp):
        return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ').weekday()

    def _get_time_of_day(self, timestamp):
        time = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
        return time.hour * 60 + time.minute


class IncreaseDecreaseSequenceConverter:

    def __init__(self, source, length):
        self._source = source
        self._length = length

    def convert(self):
        fields = tuple('value%s' % i for i in range(self._length))
        writer = csv.DictWriter(sys.stdout, fields)
        writer.writeheader()
        sources = tuple(map(json.loads, self._source[i:]) for i in range(self._length + 1))
        for values in zip(*sources):
            writer.writerow(dict(
                ('value%s' % i, self._get_price_direction(values[i]['start_price'], values[i]['end_price'])) for i in range(self._length)
            ))

    def _get_price_direction(self, a, b):
        if a == b:
            return 0
        if a > b:
            return 1
        return -1


source = list(open(sys.argv[2]))
if sys.argv[1] == 'main':
    MainConverter(source).convert()
elif sys.argv[1] == 'increase-decrease':
    IncreaseDecreaseSequenceConverter(source, 4).convert()
