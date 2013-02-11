#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.cmdparsers.lookupregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'EQ',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD', 'ID',
    'PLUS', 'MINUS',
    'COLON',
]

reserved = {
    'lookup' : 'LOOKUP', 
    'as' : 'ASLC',
    'AS' : 'ASUC',
    'OUTPUT' : 'OUTPUT',
    'OUTPUTNEW' : 'OUTPUTNEW',
}

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_EQ = r'='

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.

def type_if_reserved(t, default):
    return reserved.get(t.value, default)

@TOKEN(word)
def t_WORD(t):
    t.type = type_if_reserved(t, 'WORD')
    return t

@TOKEN(id)
def t_ID(t):
    t.type = type_if_reserved(t, 'ID')
    return t

@TOKEN(plus)
def t_PLUS(t):
    return t

def t_COLON(t):
    r':'
    return t


@TOKEN(minus)
def t_MINUS(t):
    t.lexer.begin('ipunchecked')
    return t


def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in lookup lexer '%s'" % badchar)

lexer = ply.lex.lex()

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
