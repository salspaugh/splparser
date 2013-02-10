#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.cmdparsers.lookupregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA', 'PERIOD',
    'EQ',
    'PLUS', 'MINUS',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD',
    'ID',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'OUTPUT',
    'UPDATE',
]

reserved = {
    'lookup' : 'LOOKUP', 
    'as' : 'ASLC',
    'AS' : 'ASUC',
}

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_EQ = r'='

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.


def is_ipv4addr(addr):
    addr = addr.replace('*', '0')
    addr = addr.strip()
    addr = addr.strip('"')
    port = addr.find(':')
    if port > 0:
        addr = addr[:port]
    slash = addr.find('/')
    if slash > 0:
        addr = addr[:slash]
    addr = addr.strip()
    import socket
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        return False
    return True

def is_ipv6addr(addr):
    addr = addr.replace('*', '0')
    addr = addr.strip()
    addr = addr.strip('"')
    addr = addr.strip('[')
    port = addr.find(']')
    if port > 0:
        addr = addr[:port]
    slash = addr.find('/')
    if slash > 0:
        addr = addr[:slash]
    addr = addr.strip()
    import socket
    try:
        socket.inet_pton(socket.AF_INET6, addr)
    except socket.error:
        return False
    return True

def type_if_reserved(t, default):
    if re.match(search_key, t.value):
        return 'SEARCH_KEY'
    else:
        return reserved.get(t.value, default)

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    return t

def t_PERIOD(t):
    r'\.'
    return t

@TOKEN(plus)
def t_PLUS(t):
    return t

@TOKEN(minus)
def t_MINUS(t):
    return t

@TOKEN(search_key)
def t_SEARCH_KEY(t):
    return(t)

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
