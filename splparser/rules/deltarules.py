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
    p[0] = ParseTreeNode('DELTA')
    p[0].add_child(p[2])

def p_delta_arg_opt(p):
    """deltacmd : DELTA deltaarg deltaopt"""
    p[0] = ParseTreeNode('DELTA')
    p[0].add_child(p[2])
    p[0].add_child(p[3])

def p_delta_opt_arg(p):
    """deltacmd : DELTA deltaopt deltaarg"""
    p[0] = ParseTreeNode('DELTA')
    p[0].add_child(p[2])
    p[0].add_child(p[3])

def p_deltaarg_as(p):
    """deltaarg : field as field"""
    p[0] = p[1]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    p[1].renamed = p[3]

def p_deltaarg(p):
    """deltaarg : field"""
    p[0] = p[1]

def p_deltaopt(p):
    """deltaopt : DELTA_OPT EQ INT"""
    p[0] = ParseTreeNode('EQ')
    opt_node = ParseTreeNode(p[1].upper(), option=True)
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    int_node = ParseTreeNode('INT', raw=p[3], arg=True)
    p[0].add_child(int_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in delta parser input!") 
