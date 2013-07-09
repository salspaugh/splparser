#!/usr/bin/python

import queryutils
from splparser import parse
from sys import stdout

BYTES_IN_MB = 1048576
MBS = 800

MONITOR = 'monitor.tmp'

def print_status(success, total):
    print "successes: ", success
    print "total: ", total
    print "percent: ", float(success) / float(total) * 100.

def main():
    print "starting..."
    last_queries = []
    seen = {}
    total = 0.
    success = 0.
    for queries in queryutils.get_queries(limit=MBS*BYTES_IN_MB):
        for query in queries:
            if not query.text in seen:
                m = open(MONITOR, 'w')
                m.write(query.text)
                m.write('\n')
                m.flush()
                try:
                    parse(query.text)
                    seen[query.text] = 1.
                except:
                    seen[query.text] = 0.
            total += 1.
            success += seen[query.text] # 1 if parseable, 0 otherwise
            if total % 100. == 0:
                stdout.write('.')
                stdout.flush()
            if total % 1000. == 0:
                stdout.write('\n')
                stdout.flush()
            if total % 100000. == 0.:
                print_status(success, total)

    print "DONE"
    print_status(success, total)

main()
