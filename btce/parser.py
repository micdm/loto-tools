#!/usr/bin/env python

import json
import re
import sys
from lxml import etree

def get_bets(text):
    match = re.search('↑(\d+) ↓(\d+)', text)
    return int(match.group(1)), int(match.group(2))


def get_amounts(text):
    match = re.search('↑([\d\.]+) ↓([\d\.]+)', text)
    return match.group(1), match.group(2)


tree = etree.parse(sys.argv[1], etree.HTMLParser())
table = str.maketrans({'↓': '', '↑': ''})
for row in tree.xpath('//table[@id="last_periods"]//tr'):
    cells = row.xpath('./td')
    if not cells:
        continue
    is_ended = len(cells[6].xpath('.//span[text()="ended"]')) != 0
    if not is_ended:
        continue
    print(json.dumps({
        'number': cells[0].text,
        'start_price': cells[2].text,
        'end_price': cells[3].xpath('./b')[0].text.translate(table),
        'bets': get_bets(cells[4].text),
        'amounts': get_amounts(cells[5].text)
    }))
