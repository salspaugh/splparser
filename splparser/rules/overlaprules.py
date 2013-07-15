#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.overlaplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_overlap(p):
    """cmdexpr : overlapcmd"""
    p[0] = p[1]

def p_cmdexpr_overlap_debug(p):
    """overlapcmd : OVERLAP"""
    p[0] = ParseTreeNode('COMMAND', raw='overlap')

def p_error(p):
    raise SPLSyntaxError("Syntax error in overlap parser input!") 
