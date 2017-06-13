#!/usr/bin/env python

import json
import sys


def get_rounds_from_file(file_name):
    rounds = {}
    for line in open(file_name):
        round = json.loads(line)
        if round['number'] not in rounds or round['start_time'] < rounds[round['number']]['start_time']:
            rounds[round['number']] = round
    return rounds


rounds = get_rounds_from_file(sys.argv[1])

for key in sorted(rounds.keys(), key=int):
    print(json.dumps(rounds[key]))
