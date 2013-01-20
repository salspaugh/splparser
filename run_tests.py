#!/usr/bin/env python

import os
import subprocess
import sys

TESTS_DIR='test'
TESTS_PREFIX = 'test_'
TESTS_SUFFIX = '.py'

def run_all_tests(tests_dir=TESTS_DIR):
    for test in find_tests("", descend=True):
        run_test(test)

def is_test(f):
    return (f[0:5] == TESTS_PREFIX and f[-3:] == TESTS_SUFFIX)

def run_test(test):
    print "Running test:"
    print "\t"+ test
    subprocess.call(test)
    print

def run_tests_in(module, descend=False):
    for test in find_tests(module, descend=descend):
        run_test(test)

def find_tests(module, descend=False):
    module_tests_dir = module.replace('.', '/')
    tests_dir = TESTS_DIR + '/' + module_tests_dir
    for (dirpath, dirnames, filenames) in os.walk(tests_dir):
        for filename in filenames:
            if is_test(filename):
                yield dirpath + '/' + filename
        if not descend:
            break

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-a", "--all", dest="all", 
                      action="store_true", default=False,
                      help="run all tests (this is the default)")
    parser.add_option("-m", "--module", dest="module", metavar="MODULE", 
                      help="run tests in module MODULE")
    parser.add_option("-d", "--descend", dest="descend",
                      action="store_true", default=False,
                      help="also run all tests below MODULE")
    (options, args) = parser.parse_args()
    
    if options.all:
        run_all_tests()
    elif not options.module is None:
        run_tests_in(options.module, descend=options.descend)
    else:
        run_all_tests()
