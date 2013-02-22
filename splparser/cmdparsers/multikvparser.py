#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *

from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.fieldlistrules import *
from splparser.cmdparsers.common.valuerules import *

from splparser.cmdparsers.multikvlexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_multikvs(p):
    """cmdexpr : multikvcmd"""
    p[0] = p[1]

def p_multikvcmd_multikv(p):
    """multikvcmd : MULTIKV"""
    p[0] = ParseTreeNode('MULTIKV')
    p[0].error = True

def p_multikv_multikvopt_fieldlist(p):
    """multikvcmd : MULTIKV multikvoptlist"""
    p[0] = ParseTreeNode('MULTIKV')
    p[0].add_children(p[2].children)

def p_conf_multikvoptlist(p):
    """multikvcmd : MULTIKV conf multikvoptlist"""
    p[0] = ParseTreeNode('MULTIKV')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)
    
def p_conf(p):
    """conf : CONF EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_multikvoptlist(p):
    """multikvoptlist : multikvopt"""
    p[0] = ParseTreeNode('_MULTIKV_OPT_LIST')
    p[0].add_child(p[1])

def p_multikvoptlist_multikvopt(p):
    """multikvoptlist : multikvopt multikvoptlist"""
    p[0] = ParseTreeNode('_MULTIKV_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children) 

def p_multikvopt(p):
    """multikvopt : MULTIKV_SINGLE_OPT EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_multipkopt_listopt(p):
    """multikvopt : MULTIKV_LIST_OPT fieldlist"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[2].children)

def p_multikvopt_equal(p):
    """multikvopt : MULTIKV_LIST_OPT EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in multikv parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "commandparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="multikv_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
