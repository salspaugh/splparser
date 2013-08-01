#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.convertlexer import precedence, tokens

start = 'cmdexpr'

def p_convert_timeformat_exprlist(p):
    """cmdexpr : CONVERT TIMEFORMAT EQ value convertexprlist"""
    p[0] = ParseTreeNode('COMMAND', raw='convert')
    eq_node = ParseTreeNode('EQ', raw='assign')
    timeformat_node = ParseTreeNode('OPTION', raw='timeformat')
    timeformat_node.values.append(p[4])
    eq_node.add_child(timeformat_node)
    eq_node.add_child(p[4])
    p[0].add_child(eq_node)
    p[0].add_children(p[5].children)

def p_convert_exprlist(p):
    """cmdexpr : CONVERT convertexprlist"""
    p[0] = ParseTreeNode('COMMAND', raw='convert')
    p[0].add_children(p[2].children)

def p_convertexpr_convertexprlist(p):
    """convertexprlist : convertexpr convertexprlist"""
    p[0] = ParseTreeNode('_CONVERT_EXPR_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_convertexprlist(p):
    """convertexprlist : convertexpr"""
    p[0] = ParseTreeNode('_CONVERT_EXPR_LIST')
    p[0].add_child(p[1])

def p_convertexpr(p):
    """convertexpr : CONVERT_FN LPAREN field RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(p[3])

def p_convertexpr_as(p):
    """convertexpr : CONVERT_FN LPAREN field RPAREN as field"""
    fn_node = ParseTreeNode('FUNCTION', raw=p[1])
    fn_node.add_child(p[3])
    as_node = ParseTreeNode('FUNCTION', raw='as')
    as_node.add_children([fn_node, p[6]])
    p[6].values.append(fn_node)
    p[0] = as_node

def p_convertexpr_macro(p):
    """convertexpr : MACRO"""
    p[0] = ParseTreeNode('MACRO', raw=p[1], is_argument=True)

def p_error(p):
    raise SPLSyntaxError("Syntax error in convert parser input!") 
