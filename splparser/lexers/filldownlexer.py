#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes.searchregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA',
    'WILDCARD',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'HOSTNAME', 
    'ID',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'INTERNAL_FIELD',
    'DEFAULT_FIELD',
    'DEFAULT_DATETIME_FIELD'
]

reserved = {
    'filldown' : 'FILLDOWN', 
}

tokens = tokens + list(reserved.values())

precedence = (
    ('left', 'COMMA'),
)

t_ignore = ' '

def type_if_reserved(t, default):
    if re.match(internal_field, t.value):
        return 'INTERNAL_FIELD'
    elif re.match(default_field, t.value):
        return 'DEFAULT_FIELD',
    elif re.match(default_datetime_field, t.value):
        return 'DEFAULT_DATETIME_FIELD'
    else:
        return reserved.get(t.value, default)

@TOKEN(internal_field)
def t_INTERNAL_FIELD(t):
    return(t)

@TOKEN(default_field)
def t_DEFAULT_FIELD(t):
    return(t)

@TOKEN(default_datetime_field)
def t_DEFAULT_DATETIME_FIELD(t):
    return(t)

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    return t

@TOKEN(wildcard)
def t_WILDCARD(t):
    return t

@TOKEN(literal)
def t_LITERAL(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(hostname)
def t_HOSTNAME(t):
    t.type = type_if_reserved(t, 'HOSTNAME')
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
    t.type = type_if_reserved(t, 'WORD')
    return t

@TOKEN(int)
def t_INT(t):
    return t

@TOKEN(id)
def t_ID(t):
    t.type = type_if_reserved(t, 'ID')
    return t

@TOKEN(nbstr)
def t_NBSTR(t): # non-breaking string
    t.type = type_if_reserved(t, 'NBSTR')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in filldown lexer '%s'" % badchar)

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
