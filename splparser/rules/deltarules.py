#!/usr/bin/env python

from splparser.parsetree import *

from splparser.rules.common.asrules import *
from splparser.rules.common.fieldrules import *

from splparser.lexers.deltalexer import tokens

start = 'cmdexpr'

def p_cmdexpr_delta(p):
    """cmdexpr : deltacmd"""
    p[0] = p[1]

def p_delta_arg(p):
    """deltacmd : DELTA deltaarg"""
    p[0] = ParseTreeNode('COMMAND', raw='delta')
    p[0].add_child(p[2])

def p_delta_arg_opt(p):
    """deltacmd : DELTA deltaarg deltaopt"""
    p[0] = ParseTreeNode('COMMAND', raw='delta')
    p[0].add_child(p[2])
    p[0].add_child(p[3])

def p_delta_opt_arg(p):
    """deltacmd : DELTA deltaopt deltaarg"""
    p[0] = ParseTreeNode('COMMAND', raw='delta')
    p[0].add_child(p[2])
    p[0].add_child(p[3])

def p_deltaarg_as(p):
    """deltaarg : field as field"""
    p[0] = ParseTreeNode('FUNCTION', raw='as')
    p[0].add_children([p[1], p[3]])

def p_deltaarg(p):
    """deltaarg : field"""
    p[0] = p[1]

def p_deltaopt(p):
    """deltaopt : DELTA_OPT EQ INT"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    int_node = ParseTreeNode('VALUE', nodetype='INT', raw=p[3], is_argument=True)
    p[0].add_child(int_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in delta parser input!") 
