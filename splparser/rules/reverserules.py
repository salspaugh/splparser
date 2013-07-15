#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.reverselexer import tokens

start = 'cmdexpr'

def p_cmdexpr_reverse(p):
    """cmdexpr : reversecmd"""
    p[0] = p[1]

def p_cmdexpr_reverse_debug(p):
    """reversecmd : REVERSE"""
    p[0] = ParseTreeNode('COMMAND', raw='reverse')

def p_error(p):
    raise SPLSyntaxError("Syntax error in reverse parser input!") 
