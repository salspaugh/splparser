#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.typerules import *

from splparser.common.lexers.mainlexer import lexer, tokens
from splparser.common.precedence.mainprecedence import *

start = 'cmdexpr'

def p_cmdexpr_dedup(p):
    """cmdexpr : dedupcmd"""
    p[0] = p[1]

def p_dedupcmd(p):
    """dedupcmd : DEDUP fieldlist dedupoptlist"""
    p[0] = ParseTreeNode('DEDUP')
    fields_node = ParseTreeNode('FIELDS')
    p[0].add_child(fields_node)
    fields_node.add_children(p[2].children)
    p[0].add_children(p[3].children)

#def p_dedupcmd_int(p):
#    """dedupcmd : DEDUP INT fieldlist dedupoptlist"""
#
#def p_dedupcmd(p):
#    """dedupcmd : DEDUP fieldlist dedupoptlist dedupsortby"""
#
#def p_dedupcmd_int(p):
#    """dedupcmd : DEDUP INT fieldlist dedupoptlist dedupsortby"""

def p_dedupoptlist_dedupopt(p):
    """dedupoptlist : dedupopt"""

def p_dedupoptlist(p):
    """dedupoptlist : dedupopt dedupoptlist"""

def p_dedupopt(p):
    """deduparg : DEDUP_OPT EQ value"""

def p_dedupsortby(p):
    """dedupsortby : SORTBY SORTBY_FN LPAREN field RPAREN"""

def p_dedupsortby(p):
    """dedupsortby : SORTBY PLUS SORTBY_FN LPAREN field RPAREN"""

def p_dedupsortby(p):
    """dedupsortby : SORTBY MINUS SORTBY_FN LPAREN field RPAREN"""

def p_error(p):
    raise SPLSyntaxError("Syntax error in dedup parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "dedupparser.log",
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
