#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes.evalregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA',
    'WILDCARD',
    'HOSTNAME',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'LPAREN', 'RPAREN',
    'ID',
    'PLUS', 'MINUS',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'SORT_FN',
    'DESC',
    'INTERNAL_FIELD',
    'DEFAULT_FIELD',
    'DEFAULT_DATETIME_FIELD'
]

reserved = {
    'sort' : 'SORT', 
}

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'\-'

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.

def type_if_reserved(t, default):
    if re.match(sort_fn, t.value):
        return 'SORT_FN'
    elif re.match(internal_field, t.value):
        return 'INTERNAL_FIELD'
    elif re.match(default_field, t.value):
        return 'DEFAULT_FIELD',
    elif re.match(default_datetime_field, t.value):
        return 'DEFAULT_DATETIME_FIELD'
    else:
        return reserved.get(t.value, default)

def t_DESC(t):
    r"""(d|desc)"""
    return t

def t_MACRO(t):
    r"""(`[^`]*`)"""
    return t

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    return t

def t_LITERAL(t):
    r'"(?:[^"]+(?:(\s|-|_)+[^"]+)+\s*)"'
    return(t)

@TOKEN(sort_fn)
def t_SORT_FN(t):
    return(t)

@TOKEN(internal_field)
def t_INTERNAL_FIELD(t):
    return(t)

@TOKEN(default_field)
def t_DEFAULT_FIELD(t):
    return(t)

@TOKEN(default_datetime_field)
def t_DEFAULT_DATETIME_FIELD(t):
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

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character in search lexer '%s'" % badchar)

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
