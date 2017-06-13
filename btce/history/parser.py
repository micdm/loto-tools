#!/usr/bin/env python3

from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
import sys

from lxml import etree

tree = etree.parse(sys.argv[1], etree.HTMLParser())
for row in tree.xpath('//tr'):
    if not row.xpath('.//td'):
        continue
    cells = row.xpath('./td')
    print(json.dumps({
        'id': cells[0].text[1:],
        'amount': str(Decimal(cells[1].xpath('./b')[0].text)),
        'currency': cells[1].xpath('./b')[1].text,
        'time': datetime.strptime(cells[3].text + ' ' + cells[3].xpath('./span')[0].text, '%d.%m.%y %H:%M:%S').replace(tzinfo=timezone(timedelta(hours=4))).astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'description': cells[2].text
    }))
