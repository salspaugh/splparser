#!/usr/bin/env python

from cProfile import run

run('import splparser', "import.profile")

from time import time

start = time()

from splparser import parse

elapsed = time() - start
print "\tTime to import: %d seconds" % elapsed

run('parse("stats count(foo) by bar")', "parse.profile")
