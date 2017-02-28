#!/usr/bin/env python

import sys
from lxml import etree

tree = etree.parse(sys.argv[1], etree.HTMLParser())
for row in tree.xpath('//div[@class="data_table"]//tbody/tr'):
    cells = row.xpath('./td')
    round, numbers = int(cells[0].text), map(lambda item: int(item.strip()), cells[1].text.split(','))
    for number in numbers:
        print("{} {}".format(number, round))
 
