#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes.evalregexes import *
from splparser.exceptions import SPLSyntaxError

tokens = [
    'COMMA', 'PERIOD',
    'EQ', 'LT', 'LE', 'GE', 'GT', 'NE', 'DEQ',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDES', 'MODULUS',
    'LPAREN', 'RPAREN',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'ID',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'EVAL_FN',
    'COMMON_FN',
    'HEAD_OPT',
    'COMMON_OPT',
    'INTERNAL_FIELD',
    'DEFAULT_FIELD',
    'DEFAULT_DATETIME_FIELD'
]

reserved = {
    'head' : 'HEAD', 
    'AND' : 'AND',
    'OR' : 'OR',
    'NOT' : 'NOT',
    'XOR' : 'XOR',
    'LIKE' : 'LIKE',
}

tokens = tokens + list(reserved.values())

precedence = (
    ('left', 'COMMA', 'AND', 'OR', 'XOR'), 
    ('right', 'NOT', 'LIKE'),
    ('left', 'EQ', 'LT', 'LE', 'GE', 'GT', 'NE', 'DEQ'),
    ('left', 'PLUS', 'MINUS'), 
    ('left', 'TIMES', 'DIVIDES', 'MODULUS', 'PERIOD'), 
    ('right', 'UMINUS'),
)

t_ignore = ' '

t_EQ = r'='
t_LT = r'<'
t_LE = r'<='
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_DEQ = r'=='
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
    if re.match(eval_fn, t.value):
        return 'EVAL_FN'
    elif re.match(common_fn, t.value):
        return 'COMMON_FN'
    elif re.match(head_opt, t.value):
        return 'HEAD_OPT'
    elif re.match(common_opt, t.value):
        return 'COMMON_OPT'
    elif re.match(internal_field, t.value):
        return 'INTERNAL_FIELD'
    elif re.match(default_field, t.value):
        return 'DEFAULT_FIELD',
    elif re.match(default_datetime_field, t.value):
        return 'DEFAULT_DATETIME_FIELD'
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

@TOKEN(plus)
def t_PLUS(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(minus)
def t_MINUS(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(times)
def t_TIMES(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(divides)
def t_DIVIDES(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(modulus)
def t_MODULUS(t):
    t.lexer.begin('ipunchecked')
    return t

@TOKEN(common_fn)
def t_COMMON_FN(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(eval_fn)
def t_EVAL_FN(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(head_opt)
def t_HEAD_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(common_opt)
def t_COMMON_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(internal_field)
def t_INTERNAL_FIELD(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(default_field)
def t_DEFAULT_FIELD(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(default_datetime_field)
def t_DEFAULT_DATETIME_FIELD(t):
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
    raise SPLSyntaxError("Illegal character in head lexer '%s'" % badchar)

def lex():
    return ply.lex.lex()

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
