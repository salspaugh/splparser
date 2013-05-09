#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.collectlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_dedup(p):
    """cmdexpr : collectcmd"""
    p[0] = p[1]

def p_dedup(p):
    """collectcmd : COLLECT optionlist"""
    p[0] = ParseTreeNode('COLLECT')
    p[0].add_children(p[2])

def p_optionlist(p):
    """optionlist : COLLECT_OPT EQ field optionlist"""
    option = ParseTreeNode('EQ')
    opt_node = ParseTreeNode(p[1].upper(), option=True)
    opt_node.values.append(p[3])
    option.add_children([opt_node, p[3]])
    p[0] = [option] + p[4]

def p_optionlist_comma(p):
    """optionlist : COLLECT_OPT EQ field COMMA optionlist"""
    option = ParseTreeNode('EQ')
    opt_node = ParseTreeNode(p[1].upper(), option=True)
    opt_node.values.append(p[3])
    option.add_children([opt_node, p[3]])
    p[0] = [option] + p[5]

def p_optionlist_one(p):
    """optionlist : COLLECT_OPT EQ field"""
    option = ParseTreeNode('EQ')
    opt_node = ParseTreeNode(p[1].upper(), option=True)
    opt_node.values.append(p[3])
    option.add_children([opt_node, p[3]])
    p[0] = [option]

def p_error(p):
    raise SPLSyntaxError("Syntax error in collect parser input!")
