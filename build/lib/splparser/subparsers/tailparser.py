#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_tail(p):
    """cmdexpr : tailcmd"""
    p[0] = p[1]

def p_tailcmd_tail(p):
    """tailcmd : TAIL"""
    p[0] = ParseTreeNode('TAIL')

def p_tailcmd_tail_int(p):
    """tailcmd : TAIL INT"""
    p[0] = ParseTreeNode('TAIL')
    int_node = ParseTreeNode('INT', raw=p[2])
    p[0].add_child(int_node)
