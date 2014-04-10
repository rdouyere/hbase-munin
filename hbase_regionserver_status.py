#!/usr/bin/python

# Gets the region status page, parses it and extracts metrics.

import httplib, sys, re
from lxml import etree
from io import StringIO, BytesIO

conn = httplib.HTTPConnection("localhost:60030")
conn.request("GET", "/rs-status")
res = conn.getresponse()

# current / max heap
# nb regions
# read & write request count derive
if res.status == 200:
    data = res.read()

    parser = etree.HTMLParser()
    root   = etree.fromstring(data, parser)
    metrics_str = root.xpath('(//table)[1]/tr[4]/td[2]/text()')[0]
    #print metrics_str

    values = dict()
    for entry in metrics_str.split(','):
        key,value=entry.split("=")
        values[key.strip()] = value.strip()

    # print values

    if sys.argv[-1] == 'config':
        print "graph_title Hbase rs status"
        print "graph_args -l 0"
        print "graph_category hbase"
        print "graph_vlabel size"
        print "current_heap.label Current Heap"
        print "current_heap.draw LINE1"
        print "max_heap.label Max Heap"
        print "max_heap.draw LINE1"
        print "nb_regions.label Nb regions"
        print "nb_regions.draw LINE1"
        print "read_requests.label Read requests"
        print "read_requests.draw LINE1"
        print "read_requests.type DERIVE"
        print "write_requests.label Write requests"
        print "write_requests.draw LINE1"
        print "write_requests.type DERIVE"
    else:
        print "current_heap.value " + values["usedHeapMB"]
        print "max_heap.value " + values["maxHeapMB"]
        print "nb_regions.value " + values["numberOfOnlineRegions"]
        print "read_requests.value " + values["readRequestsCount"]
        print "write_requests.value " + values["writeRequestsCount"]

