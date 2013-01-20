#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.reverselexer import lexer, tokens

start = 'cmdexpr'

# TODO: Delete this parser and integrate into the top-level parser.

def p_cmdexpr_reverse(p):
    """cmdexpr : reversecmd"""
    p[0] = p[1]

def p_cmdexpr_reverse_debug(p):
    """reversecmd : REVERSE"""
    p[0] = ParseTreeNode('REVERSE')

def p_error(p):
    raise SPLSyntaxError("Syntax error in reverse parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "reverseparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog)
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
