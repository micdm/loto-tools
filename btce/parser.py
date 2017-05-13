#!/usr/bin/env python

from datetime import datetime, timedelta
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

today = datetime.strptime(tree.xpath('(//div[@class="orderStats"]/strong)[last()]')[0].text, '%d.%m.%y %H:%M').date()
for row in tree.xpath('//table[@id="last_periods"]//tr'):
    cells = row.xpath('./td')
    if not cells:
        continue
    is_ended = len(cells[6].xpath('.//span[text()="ended"]')) != 0
    if not is_ended:
        continue
    start_time = datetime.strptime(cells[1].text[:5], "%H:%M").time()
    print(json.dumps({
        'number': cells[0].text,
        'start_time': str(datetime.combine(today, start_time).strftime('%s')),
        'start_price': cells[2].text,
        'end_price': cells[3].xpath('./b')[0].text.translate(table),
        'bets': get_bets(cells[4].text),
        'amounts': get_amounts(cells[5].text)
    }))
    if start_time.hour == 0 and start_time.minute == 0:
        today -= timedelta(days=1)
