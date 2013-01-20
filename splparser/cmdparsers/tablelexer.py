#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.cmdparsers.fieldsregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA',
    'WILDCARD',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'ID',
    'EMAIL',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
]

reserved = {
    'table' : 'TABLE', 
}

tokens = tokens + list(reserved.values())

precedence = (
    ('left', 'COMMA'),
)

t_ignore = ' '

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    return t

@TOKEN(wildcard)
def t_WILDCARD(t):
    return t

def t_LITERAL(t):
    r'"(?:[^"]+(?:(\s|-|_)+[^"]+)+\s*)"'
    return(t)

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

@TOKEN(word)
def t_WORD(t):
    t.type = reserved.get(t.value, 'WORD')
    return t

@TOKEN(int)
def t_INT(t):
    return t

@TOKEN(id)
def t_ID(t):
    t.type = reserved.get(t.value, 'ID')
    return t

@TOKEN(email)
def t_EMAIL(t):
    t.type = reserved.get(t.value, 'EMAIL')
    return t

@TOKEN(nbstr)
def t_NBSTR(t): # non-breaking string
    t.type = reserved.get(t.value, 'NBSTR')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in search lexer '%s'" % badchar)

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
