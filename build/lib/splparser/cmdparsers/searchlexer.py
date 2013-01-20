#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.cmdparsers.searchregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA', 'PERIOD',
    'WILDCARD',
    'EQ', 'LT', 'LE', 'GE', 'GT', 'NE',
    'PLUS', 'MINUS',
    'COLON', 'DCOLON',
    'LPAREN', 'RPAREN',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'ID',
    'EMAIL',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'SEARCH_KEY',
]

reserved = {
    'search' : 'SEARCH', 
    'AND' : 'AND',
    'OR' : 'OR',
    'NOT' : 'NOT',
    'host' : 'HOST',
    'tag' : 'TAG',
}

tokens = tokens + list(reserved.values())

precedence = (
    ('nonassoc', 'NE' ,'LT', 'LE', 'GE', 'GT'),
    ('left', 'OR'),
    ('left', 'AND', 'COMMA'),
    ('right', 'EQ', 'DCOLON'),
    ('left', 'PLUS', 'MINUS'), 
    ('right', 'NOT'),
    ('right', 'UMINUS'),
)

t_ignore = ' '

t_EQ = r'='
t_LT = r'<'
t_LE = r'<='
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_DCOLON = r'::'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# !!!   The order in which these functions are defined determine matchine. The 
#       first to match is used. Take CARE when reordering.

states = (
    ('ipunchecked', 'inclusive'),
)

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
    t.lexer.begin('ipunchecked')
    return t

def t_PERIOD(t):
    r'\.'
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(wildcard)
def t_WILDCARD(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(plus)
def t_PLUS(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(minus)
def t_MINUS(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(search_key)
def t_SEARCH_KEY(t):
    t.lexer.begin('ipunchecked')
    return(t)

def t_LITERAL(t):
    r'"(?:[^"]+(?:(\s|-|_)+[^"]+)+\s*)"'
    return(t)

@TOKEN(bin)
def t_BIN(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(oct)
def t_OCT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(hex)
def t_HEX(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(float)
def t_FLOAT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(ipv4_addr)
def t_ipunchecked_IPV4ADDR(t):
    if is_ipv4addr(t.value):
        return t
    t.lexer.lexpos -= len(t.value)
    t.lexer.begin('INITIAL')
    return

@TOKEN(ipv6_addr)
def t_ipunchecked_IPV6ADDR(t):
    if is_ipv6addr(t.value):
        return t
    t.lexer.lexpos -= len(t.value)
    t.lexer.begin('INITIAL')
    return

@TOKEN(word)
def t_WORD(t):
    t.type = type_if_reserved(t, 'WORD')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(int)
def t_INT(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(id)
def t_ID(t):
    t.type = type_if_reserved(t, 'ID')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(email)
def t_EMAIL(t):
    t.type = type_if_reserved(t, 'EMAIL')
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(nbstr)
def t_NBSTR(t): # non-breaking string
    t.type = type_if_reserved(t, 'NBSTR')
    t.lexer.begin('ipunchecked')
    return t

def t_COLON(t):
    r':'
    t.lexer.begin('ipunchecked')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    t.lexer.begin('ipunchecked')
    raise SPLSyntaxError("Illegal character in search lexer '%s'" % badchar)

lexer = ply.lex.lex()

def tokenize(data, debug=False, debuglog=None):
    lexer = ply.lex.lex(debug=debug, debuglog=debuglog)
    lexer.input(data)
    lexer.begin('ipunchecked')
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: break
        tokens.append(tok)
    return tokens

if __name__ == "__main__":
    import sys
    print tokenize(' '.join(sys.argv[1:]))
