#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.fieldlistrules import *
from splparser.cmdparsers.common.typerules import *

from splparser.cmdparsers.tablelexer import lexer, precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_table(p):
    """cmdexpr : tablecmd"""
    p[0] = p[1]

def p_cmdexpr_table_debug(p):
    """tablecmd : TABLE"""
    p[0] = ParseTreeNode('TABLE')

def p_table_fieldlist(p):
    """tablecmd : TABLE fieldlist"""
    p[0] = ParseTreeNode('TABLE')
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in table parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "tableparser.log",
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
