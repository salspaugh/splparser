#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_reverse(p):
    """cmdexpr : reversecmd"""
    p[0] = p[1]

def p_cmdexpr_reverse_debug(p):
    """reversecmd : REVERSE"""
    p[0] = ParseTreeNode('REVERSE')
