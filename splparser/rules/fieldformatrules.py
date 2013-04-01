#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.evalfnexprrules import *
from splparser.rules.common.simplefieldrules import *

from splparser.lexers.fieldformatlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_fieldformat(p):
    """cmdexpr : fieldformatcmd"""
    p[0] = p[1]

def p_fieldformat_fieldformatexpr(p):
    """fieldformatcmd : FIELDFORMAT oplist"""
    p[0] = ParseTreeNode('FIELDFORMAT')
    p[0].add_children(p[2].children)

#def p_fieldformat_fieldformatexpr(p):
#    """fieldformatcmd : FIELDFORMAT simplefield EQ evalfnexpr"""
#    p[0] = ParseTreeNode('FIELDFORMAT')
#    eq_node = ParseTreeNode('EQ')
#    p[0].add_child(eq_node)
#    eq_node.add_child(p[2])
#    eq_node.add_child(p[4])

def p_error(p):
    raise SPLSyntaxError("Syntax error in fieldformat parser input!") 
