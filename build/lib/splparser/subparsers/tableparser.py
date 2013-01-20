#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_table(p):
    """cmdexpr : tablecmd"""
    p[0] = p[1]

def p_cmdexpr_table_debug(p):
    """tablecmd : TABLE"""
    p[0] = ParseTreeNode('TABLE')

def p_table_fieldlist(p):
    """tablecmd : TABLE fieldlist"""
    p[0] = ParseTreeNode('TABLE')
    p[0].add_children(p[2].children)
