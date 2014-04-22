#!/usr/bin/python

from argparse import ArgumentParser
from splparser import parse
from splparser.exceptions import *
from sqlite3 import connect
from sys import stdout, stderr

MONITOR = 'monitor.tmp'

def check_number_parseable(database):
    print "starting..."
    last_queries = []
    notimplemented = {}
    error = {}
    total = 0.
    success = 0.
    for query in read_queries(database):
        m = open(MONITOR, 'w')
        m.write(query.encode("utf8"))
        m.write('\n')
        m.flush()
        try:
            parse(query)
            success += 1.
        except NotImplementedError as e:
            cmd = e.args[0].split()[0]
            if not cmd in notimplemented:
                notimplemented[cmd] = 0.
            notimplemented[cmd] += 1.
        except SPLSyntaxError as e: # TODO: something different here
            args = e.args[0] # TODO: fix the args here to be consistent
            if type(args) == type(tuple()):
                args = args[0]
            args = args.split()
            if len(args) > 3:
                cmd = args[3]
                if not cmd in error:
                    error[cmd] = 0.
                error[cmd] += 1.
            stderr.write(str(e.args) + "\n")
            stderr.write(query.encode("utf8") + "\n")
        except TerminatingSPLSyntaxError as e: # TODO: something different here
            args = e.args[0]
            if type(args) == type(tuple()):
                args = args[0]
            args = args.split()
            if len(args) > 3:
                cmd = args[3]
                if not cmd in error:
                    error[cmd] = 0.
                error[cmd] += 1.
            stderr.write(str(e.args) + "\n")
            stderr.write(query.encode("utf8") + "\n")
        except Exception as e:
            stderr.write(str(e.args) + "\n")
            stderr.write(query.encode("utf8") + "\n")
        total += 1.
        if total % 100. == 0:
            stdout.write('.')
            stdout.flush()
        if total % 1000. == 0:
            stdout.write('\n')
            stdout.flush()
        if total % 100000. == 0.:
            print_status(success, total)

    print "DONE"
    print_status(success, total, notimplemented, error)

def read_queries(database):
    db = connect(database)
    cursor = db.execute("SELECT DISTINCT text FROM queries")
    for (text, ) in cursor.fetchall():
        yield text
    db.close()

def print_status(success, total, notimplemented, error):
    print "successes: ", success
    print "total: ", total
    print "percent: ", float(success) / float(total) * 100.
    notimplemented = sorted(notimplemented.iteritems(), key=lambda x: x[1], reverse=True)
    print "implementation priorities:"
    for (command, nqueries) in notimplemented:
        print "\t", command, nqueries
    error = sorted(error.iteritems(), key=lambda x: x[1], reverse=True)
    print "error priorities:"
    for (command, nqueries) in error:
        print "\t", command, nqueries

if __name__ == "__main__":
    parser = ArgumentParser("Checks how many queries are parseable and what commands need to be implemented.") 
    parser.add_argument("database", metavar="DATABASE", 
                        help="The database containing a queries table with a 'text' column to be parsed.")
    args = parser.parse_args()
    check_number_parseable(args.database)
