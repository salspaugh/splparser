#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.taillexer import tokens

start = 'cmdexpr'

def p_cmdexpr_tail(p):
    """cmdexpr : tailcmd"""
    p[0] = p[1]

def p_tailcmd_tail(p):
    """tailcmd : TAIL"""
    p[0] = ParseTreeNode('TAIL')

def p_tailcmd_tail_int(p):
    """tailcmd : TAIL INT"""
    p[0] = ParseTreeNode('TAIL')
    int_node = ParseTreeNode('INT', raw=p[2], arg=True)
    p[0].add_child(int_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in tail parser input!") 
