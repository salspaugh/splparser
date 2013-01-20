#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *

from splparser.cmdparsers.common.asrules import *
from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.hostnamerules import *
from splparser.cmdparsers.common.idrules import *
from splparser.cmdparsers.common.keyrules import *
from splparser.cmdparsers.common.statsfnrules import *
from splparser.cmdparsers.common.typerules import *
from splparser.cmdparsers.common.valuerules import *
    
from splparser.cmdparsers.renamelexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_rename(p):
    """cmdexpr : renamecmd"""
    p[0] = p[1]

def p_rename_renameexprlist(p):
    """renamecmd : RENAME renameexprlist"""
    p[0] = ParseTreeNode('RENAME')
    p[0].add_children(p[2].children)

# WARNING: The order of the next two rules is important.
def p_renameexprlist_renameexpr(p):
    """renameexprlist : renameexpr"""    
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])

def p_renameexprlist_renameexprlist(p):
    """renameexprlist : renameexpr COMMA renameexprlist"""
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_renameexpr_field(p):
    """renameexpr : field as value"""
    as_node = ParseTreeNode('AS')
    as_node.add_children([p[1], p[3]])
    p[0] = as_node

def p_renameexpr_statsfnexpr(p):
    """renameexpr : statsfnexpr as value"""
    as_node = ParseTreeNode('AS')
    as_node.add_children(p[1].children)
    as_node.add_child(p[3])
    p[0] = as_node

def p_error(p):
    raise SPLSyntaxError("Syntax error in rename parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "renameparser.log",
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
