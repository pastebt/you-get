#! /usr/bin/python3

import re
import sys
from urllib.parse import unquote

from db import add_one_url


html = open(sys.argv[1]).read()
m = re.search('''url_list="([^;]+)"''', html)
dat = m.group(1)
ss = unquote(dat).split("$$$")
sect = 0
for s in ss:
    sect += 1
    part = 0
    ps = s.split("+++")
    for p in ps:
        part += 1
        title = "Nashville_s%02dp%02d" % (sect, part)
        url = p.split("++")[1]
        print("%s %s" % (title, url))
        add_one_url(url, title)
