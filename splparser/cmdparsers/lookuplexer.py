#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.cmdparsers.lookupregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA',
    'EQ',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD', 'ID',
    'PLUS', 'MINUS',
    'COLON',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'LITERAL',
    'EMAIL',
    'NBSTR'
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

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    return t

@TOKEN(int)
def t_INT(t):
    return t

@TOKEN(bin)
def t_BIN(t):
    return t

@TOKEN(oct)
def t_OCT(t):
    return t

@TOKEN(hex)
def t_HEX(t):
    return t

@TOKEN(float)
def t_FLOAT(t):
    return t

@TOKEN(plus)
def t_PLUS(t):
    return t

@TOKEN(minus)
def t_MINUS(t):
    return t

def t_COLON(t):
    r':'
    return t

@TOKEN(word)
def t_WORD(t):
    t.type = type_if_reserved(t, 'WORD')
    return t

@TOKEN(id)
def t_ID(t):
    t.type = type_if_reserved(t, 'ID')
    return t

def t_LITERAL(t):
    r'"(?:[^"]+(?:(\s|-|_)+[^"]+)+\s*)"'
    return(t)

@TOKEN(email)
def t_EMAIL(t):
    t.type = type_if_reserved(t, 'EMAIL')
    return t

@TOKEN(nbstr)
def t_NBSTR(t): # non-breaking string
    t.type = type_if_reserved(t, 'NBSTR')
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
