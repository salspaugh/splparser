#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.collectlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_collect(p):
    """cmdexpr : collectcmd"""
    p[0] = p[1]

def p_collect(p):
    """collectcmd : COLLECT field EQ value"""
    p[0] = ParseTreeNode('COMMAND', raw='collect')
    eq_node = ParseTreeNode('EQ', raw='assign')
    eq_node.add_children([p[2], p[4]])
    p[0].add_child(eq_node)

def p_collect_comma_optionlist(p):
    """collectcmd : COLLECT field EQ value COMMA optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='collect')
    eq_node = ParseTreeNode('EQ', raw='assign')
    eq_node.add_children([p[2], p[4]])
    p[0].add_children([eq_node] + p[6])

def p_collect_optionlist(p):
    """collectcmd : COLLECT field EQ value optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='collect')
    eq_node = ParseTreeNode('EQ', raw='assign')
    eq_node.add_children([p[2], p[4]])
    p[0].add_children([eq_node] + p[5])

def p_optionlist(p):
    """optionlist : option optionlist"""
    p[0] = [p[1]] + p[2]

def p_optionlist_comma(p):
    """optionlist : option COMMA optionlist"""
    p[0] = [p[1]] + p[3]

def p_optionlist_one(p):
    """optionlist : option"""
    p[0] = [p[1]]

def p_option(p):
    """option : COLLECT_OPT EQ value"""
    eq_node = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    if p[1] in ["addtime", "spool", "testmode", "run-in-preview"]:
        opt_node.nodetype = 'BOOLEAN'
    opt_node.values.append(p[3])
    eq_node.add_children([opt_node, p[3]])
    p[0] = eq_node

def p_error(p):
    raise SPLSyntaxError("Syntax error in collect parser input!")
