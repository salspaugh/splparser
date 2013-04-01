#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN

from splparser.exceptions import SPLSyntaxError

tokens = [
    'OVERLAP'
]

t_ignore = ' '

def t_OVERLAP(t):
    r'overlap'
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in overlap lexer '%s'" % badchar)

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
