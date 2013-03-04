#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.fieldlistrules import *
from splparser.cmdparsers.common.valuerules import *

from splparser.cmdparsers.sortlexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_sort(p):
    """cmdexpr : sortcmd"""
    p[0] = p[1]

def p_sort_sortfields(p):
    """sortcmd : SORT sortfields"""
    p[0] = ParseTreeNode('SORT')
    p[0].add_children(p[2])

def p_sort_num_sortfields(p):
    """sortcmd : SORT INT sortfields"""
    p[0] = ParseTreeNode('SORT')
    num = ParseTreeNode('INT', raw=p[2])
    p[0].add_children([num] + p[3])

def p_sort_num_limit_sortfields(p):
    """sortcmd : SORT WORD EQ value sortfields"""
    print p[4]
    print p[5]
    p[0] = ParseTreeNode('SORT')
    p[0].add_children(p[5])

def p_sortfields_list(p):
    """sortfields : sortfield COMMA sortfields"""
    p[0] = [p[1]] + p[3]

def p_sortfields_single(p):
    """sortfields : sortfield"""
    p[0] = [p[1]]

def p_sortfield_asc_func(p):
    """sortfield : PLUS sortfunc
                 | PLUS field
                 | sortfunc
                 | field
                 """
    p[0] = ParseTreeNode('ASCENDING')
    i = 1 if len(p)==2 else 2
    p[0].add_child(p[i])

def p_sortfield_desc_func(p):
    """sortfield : MINUS sortfunc
                 | MINUS field
                 """
    p[0] = ParseTreeNode('DESCENDING')
    p[0].add_child(p[2])

def p_sortfunc(p):
    """sortfunc : WORD LPAREN field RPAREN"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])


def p_error(p):
    raise SPLSyntaxError("Syntax error in sort parser input!")

logging.basicConfig(
    level = logging.DEBUG,
    filename = "sortupparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="sort_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
