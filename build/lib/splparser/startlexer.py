#!/usr/bin/env python

import ply.lex
from ply.lex import TOKEN
from splparser.exceptions import SPLSyntaxError

tokens = [
    'PIPE',
#    'LBRACKET', TODO: Add support for subsearches anad macros.
#    'RBRACKET',
#    'TIC',
    'ARGS'
    ]

reserved = {
    'search': 'SEARCH',
    'stats': 'STATS',
    'eval': 'EVAL',
    'fields': 'FIELDS',
    'rename': 'RENAME',
    'table': 'TABLE',
    'top': 'TOP',
    'head': 'HEAD',
    'tail': 'TAIL',
    'reverse': 'REVERSE',
    'chart': 'CHART'
    }

tokens = tokens + list(reserved.values())

t_ignore = ' '

t_PIPE = r'\|'
#t_LBRACKET = r'\['
#t_RBRACKET = r'\]'
#t_TIC = r'`'

def t_ARGS(t):
    r"""(\'[^\']*\')|("[^"]*")|([^|\[\]`\s]+)"""
    t.type = reserved.get(t.value, 'ARGS')
    return t

def t_error(t):
    badchar = t.value[0]
    t.lexer.skip(1)
    raise SPLSyntaxError("Illegal character '%s'" % badchar)

lexer = ply.lex.lex()

def tokenize(data, debug = False, debuglog = None):
    lexer = ply.lex.lex()
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

if __name__ == '__main__':
    import sys
    print tokenize(' '.join(sys.argv[1:])) 
