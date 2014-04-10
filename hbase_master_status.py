#!/usr/bin/python

# Gets the Hmaster status page, parses it and extracts tables.
import httplib, sys, re
from lxml import etree

conn = httplib.HTTPConnection("localhost:60010")
conn.request("GET", "/master-status?filter=all") # filter used to always have the same number of tables
res = conn.getresponse()

if res.status == 200:
    data = res.read()
    parser = etree.HTMLParser()
    root  = etree.fromstring(data, parser)

    i = 0
    current = ""
    table_names = []
    table_values = []
    for entry in root.xpath('(//table)[4]/tr/td[position() = 2 or position() = 3]/text()'):
        if i % 2 == 0:
            current = entry.strip()
        else:
            name = entry.strip().split(',')[0][1:-1]
            if name.startswith("NAME"):
                name = name[9:] #for some versions...
            table_names.append(name)
            table_values.append(name + ".value " + current)
            current = ""
        i = i + 1

    if sys.argv[-1] == 'config':
        print "graph_title Hbase tables"
        print "graph_args -l 0"
        print "graph_category hbase"
        print "graph_vlabel size"
        for entry in table_names:
            print entry + ".label " + entry
            print entry + ".draw LINE1"
    else:
        for entry in table_values:
            print entry

