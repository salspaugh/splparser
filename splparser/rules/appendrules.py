#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.appendlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_append(p):
    """cmdexpr : appendcmd"""
    p[0] = p[1]

def p_append(p):
    """appendcmd : APPEND"""
    p[0] = ParseTreeNode('COMMAND', raw='append')

def p_append_optionlist(p):
    """appendcmd : APPEND optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='append')
    p[0].add_children(p[2])

def p_optionlist_single(p):
    """optionlist : APPEND_OPT EQ field"""
    p[3].role = 'VALUE'
    eq_node = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    eq_node.add_children([opt_node, p[3]])
    p[0] = [eq_node]

def p_optionlist(p):
    """optionlist : APPEND_OPT EQ field optionlist"""
    p[3].role = 'VALUE'
    eq_node = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    eq_node.add_children([opt_node, p[3]])
    p[0] = [eq_node] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in append parser input!")
