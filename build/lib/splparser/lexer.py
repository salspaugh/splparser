#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
import re

from splparser.regexes import *

class SPLSyntaxError(SyntaxError):
    
    def __init__(self, message, *args):
        self.message = message
        self.msg = message
        SyntaxError.__init__(self, args)

tokens = [
    'COMMA', 'PERIOD',
    'WHACK', 'SLASH',
    'PIPE',
    'MACRO',
    'AT',
    # TODO: considering eliminating some rules with 'COMPARISON',
    'EQ', 'LT', 'LE', 'GE', 'GT', 'NE', 'DEQ',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDES', 'MODULUS',
    'COLON', 'DCOLON',
    'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET',
    'IPV4ADDR', 'IPV6ADDR',
    'WORD',
    'INT', 'BIN', 'OCT', 'HEX', 'FLOAT',
    'ID',
    'EMAIL',
    'NBSTR', # non-breaking string
    'LITERAL', # in quotes
    'STATS_FN',
    'EVAL_FN',
    'SEARCH_KEY',
    'COMMON_OPT',
    'TOP_OPT',
    'HEAD_OPT',
    'STATS_OPT'
]

reserved = {
    'stats' : 'STATS', 
    'sparkline' : 'SPARKLINE',
    'as' : 'ASLC',
    'by' : 'BYLC',
    'AS' : 'ASUC',
    'BY' : 'BYUC',
    'search' : 'SEARCH', 
    'AND' : 'AND',
    'OR' : 'OR',
    'NOT' : 'NOT',
    'XOR' : 'XOR',
    'LIKE' : 'LIKE',
    'host' : 'HOST',
    'tag' : 'TAG',
    'eval' : 'EVAL', 
    'fields' : 'FIELDS', 
    'rename' : 'RENAME', 
    'table' : 'TABLE', 
    'top' : 'TOP', 
    'head' : 'HEAD', 
    'tail' : 'TAIL', 
    'reverse' : 'REVERSE', 
    'chart' : 'CHART',
}

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_PIPE = r'\|'
t_EQ = r'='
t_LT = r'<'
t_LE = r'<='
t_GE = r'>='
t_GT = r'>'
t_NE = r'!='
t_DEQ = r'=='
t_DCOLON = r'::'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

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
    if re.match(stats_fn, t.value):
        return 'STATS_FN'
    elif re.match(eval_fn, t.value):
        return 'EVAL_FN'
    elif re.match(search_key, t.value):
        return 'SEARCH_KEY'
    elif re.match(top_opt, t.value):
        return 'TOP_OPT'
    else:
        return reserved.get(t.value, default)

def t_COMMA(t):
    r'''(?:\,)|(?:"\,")|(?:'\,')'''
    t.lexer.begin('ipunchecked')
    return t

def t_AT(t):
    r'@'
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

def t_MACRO(t):
    r'`.+`'
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(common_opt)
def t_COMMON_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(head_opt)
def t_HEAD_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(top_opt)
def t_TOP_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(stats_opt)
def t_STATS_OPT(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(stats_fn)
def t_STATS_FN(t):
    t.lexer.begin('ipunchecked')
    return(t)

@TOKEN(eval_fn)
def t_EVAL_FN(t):
    t.lexer.begin('ipunchecked')
    return(t)

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

def t_SLASH(t):
    r'/'
    t.lexer.begin('ipunchecked')
    return t

def t_WHACK(t):
    r'\\'
    t.lexer.begin('ipunchecked')
    return t

# TODO: FIXME: Doesn't print out incorrect token
def t_error(t):
    #print "Illegal character '%s'" % t.value[0]
    #t.lexer.skip(1)
    #t.lexer.begin('ipunchecked')
    badchar = t.value[0]
    t.lexer.skip(1)
    t.lexer.begin('ipunchecked')
    raise SPLSyntaxError("Illegal character '%s'" % badchar)

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
