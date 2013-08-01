#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes.searchregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'INT',
]

reserved = {
    'transpose' : 'TRANSPOSE'
}

t_ignore = ' '

tokens = tokens + list(reserved.values())

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.

@TOKEN(word)
def t_WORD(t):
    t.type = reserved.get(t.value, 'WORD')
    return t

@TOKEN(int)
def t_INT(t):
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in transpose lexer '%s'" % badchar)

def lex():
    return ply.lex.lex()

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
