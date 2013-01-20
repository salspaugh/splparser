#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.typerules import *

from splparser.common.lexers.mainlexer import lexer, tokens
from splparser.common.precedence.mainprecedence import *

start = 'cmdexpr'

def p_error(p):
    raise SPLSyntaxError("Syntax error in command parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "commandparser.log",
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
