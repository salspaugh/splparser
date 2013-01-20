#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes import *

tokens = [
    'MINUS',
    'WORD',
]

t_MINUS = r'-'
t_ignore = ' '

#@TOKEN(minus)
#def t_MINUS(t):
#    return t

@TOKEN(word)
def t_WORD(t):
    return t

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def tokenize(data, debug=False, debuglog=None):
    lexer = ply.lex.lex(debug=debug, debuglog=debuglog)
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: break
        tokens.append(tok)
    return tokens

if __name__ == "__main__":
    import sys
    print tokenize(' '.join(sys.argv[1:]))
