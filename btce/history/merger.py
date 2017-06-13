#!/usr/bin/env python

import json
import sys


def get_records_from_file(file_name):
    records = {}
    for line in open(file_name):
        record = json.loads(line)
        if record['id'] not in records:
            records[record['id']] = record
    return records


records = get_records_from_file(sys.argv[1])

for key in sorted(records.keys(), key=int):
    print(json.dumps(records[key]))
