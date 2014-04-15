#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.transposelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_transpose(p):
    """cmdexpr : transposecmd"""
    p[0] = p[1]

def p_cmdexpr_transpose_debug(p):
    """transposecmd : TRANSPOSE"""
    p[0] = ParseTreeNode('COMMAND', raw='transpose')

def p_transpose_int(p):
    """transposecmd : TRANSPOSE INT"""
    p[0] = ParseTreeNode('COMMAND', raw='transpose')
    int_node = ParseTreeNode('VALUE', nodetype='INT', raw=p[2], is_argument=True)
    p[0].add_child(int_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in transpose parser input!") 
