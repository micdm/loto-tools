#!/usr/bin/env python

from decimal import Decimal
import re
import sys
from lxml import etree

tree = etree.parse(sys.argv[1], etree.HTMLParser())
for row in tree.xpath('//table[@id="last_periods"]//tr'):
    cells = row.xpath('./td')
    if not cells:
        continue
    is_ended = len(cells[6].xpath('.//span[text()="ended"]')) != 0
    if not is_ended:
        continue
    number = cells[0].text
    start_price = Decimal(cells[2].text)
    end_price = Decimal(cells[3].xpath('./b')[0].text.translate(str.maketrans({'↓': '', '↑': ''})))
    match = re.search('↑(\d+) ↓(\d+)', cells[4].text)
    bets = (int(match.group(1)), int(match.group(2)))
    if end_price > start_price:
        if bets[0] > bets[1]:
            check = '+'
        if bets[0] < bets[1]:
            check = '-'
        if bets[0] == bets[1]:
            check = '?'
    else:
        if bets[0] > bets[1]:
            check = '-'
        if bets[0] < bets[1]:
            check = '+'
        if bets[0] == bets[1]:
            check = '?'
    print('{} {} {} {} {}'.format(number, start_price, end_price, bets, check))
