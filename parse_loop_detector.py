#!/usr/bin/env python

MONITOR = 'monitor.tmp'

oldq = ""

while True:
    m = open('monitor.tmp', 'r')
    newq = m.readline()
    if newq == oldq:
        print same as before
        sameness += 1
        sleep(10)
    oldq = newq
