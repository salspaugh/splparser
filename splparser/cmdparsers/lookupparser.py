#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.delimiterrules import *
from splparser.cmdparsers.common.typerules import *

from splparser.cmdparsers.lookuplexer import lexer, tokens

start = 'cmdexpr'

def p_cmdexpr_lookup(p):
    """cmdexpr : lookupcmd"""
    p[0] = p[1]

def p_lookup_tablename(p):
    """lookupcmd : LOOKUP table"""
    p[0] = ParseTreeNode('LOOKUP')
    p[0].add_children(p[2])

def p_lookup_options_tablename(p):
    """lookupcmd :  LOOKUP OPTION table"""
    p[0] = ParseTreeNode('LOOKUP')
    #opt = p[2].split("=")
    opt = ["LOCAL", "asdf"]
    option = ParseTreeNode(opt[0].upper())
    boolean = ParseTreeNode('WORD', raw=opt[1])
    option.add_child(boolean)
    p[0].add_children([option] + p[3])

def p_table_tablename(p):
    """table : tablename"""
    p[0] = [p[1]]

def p_table_tablename_field(p):
    """table : tablename field"""
    p[0] = [p[1], p[2]]

def p_tablename(p):
    """tablename : WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1])

def p_field(p):
    """field : WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1])

def p_field_as(p):
    """field : WORD ASLC WORD
             | WORD ASUC WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1])
    _as = ParseTreeNode('AS')
    _as.add_child(ParseTreeNode('WORD', raw=p[3]))
    p[0].add_child(_as)

#def p_optionlist(p):
#    """optionlist : option"""
#    p[0] = [p[1]]
#
#def p_optionlist_list(p):
#    """optionlist : option optionlist"""
#    p[0] = [p[1]] + p[2]
#
#def p_option_debug(p):
#    """option : OPTION"""
#    p[0] = [ParseTreeNode('LOCAL')]
#
#def p_option(p):
#    """option : LOCAL EQ WORD"""
#    p[0] = ParseTreeNode(p[1], raw=p[1])
#    boolean = ParseTreeNode('WORD', raw=p[3])
#    p[0].add_child(boolean)

def p_error(p):
    raise SPLSyntaxError("Syntax error in lookup parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "statsparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="lookup_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
