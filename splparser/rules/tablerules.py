#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.tablelexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_table(p):
    """cmdexpr : tablecmd"""
    p[0] = p[1]

def p_cmdexpr_table_debug(p):
    """tablecmd : TABLE"""
    p[0] = ParseTreeNode('COMMAND', raw='table')

def p_table_fieldlist(p):
    """tablecmd : TABLE fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='table')
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in table parser input!") 
