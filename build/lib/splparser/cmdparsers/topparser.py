#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *

from splparser.cmdparsers.common.byrules import *
from splparser.cmdparsers.common.hostnamerules import *
from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.fieldlistrules import *
from splparser.cmdparsers.common.idrules import *
from splparser.cmdparsers.common.typerules import *
from splparser.cmdparsers.common.valuerules import *

from splparser.cmdparsers.toplexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_top(p):
    """cmdexpr : topcmd"""
    p[0] = p[1]

def p_top_fieldlist(p):
    """topcmd : TOP fieldlist"""
    p[0] = ParseTreeNode('TOP')
    p[0].add_children(p[2].children)

def p_top_fieldlist_by(p):
    """topcmd : TOP fieldlist by fieldlist"""
    by_node = ParseTreeNode('BY')
    by_node.add_children(p[4].children)
    p[0] = ParseTreeNode('TOP')
    p[0].add_children(p[2].children)
    p[0].add_child(by_node)

def p_top_topopt_fieldlist(p):
    """topcmd : TOP topoptlist fieldlist"""
    p[0] = ParseTreeNode('TOP')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_top_topopt_fieldlist_by(p):
    """topcmd : TOP topoptlist fieldlist by fieldlist"""
    by_node = ParseTreeNode('BY')
    by_node.add_children(p[5].children)
    p[0] = ParseTreeNode('TOP')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)
    p[0].add_child(by_node)

def p_topoptlist(p):
    """topoptlist : topopt"""
    p[0] = ParseTreeNode('_TOP_OPT_LIST')
    p[0].add_child(p[1])

def p_topoptlist_topopt(p):
    """topoptlist : topopt topoptlist"""
    p[0] = ParseTreeNode('_TOP_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children) 

def p_topopt(p):
    """topopt : TOP_OPT EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_topopt_commonopt(p):
    """topopt : COMMON_OPT EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

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
