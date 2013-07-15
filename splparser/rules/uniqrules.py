#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.uniqlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_uniq(p):
    """cmdexpr : uniqcmd"""
    p[0] = p[1]

def p_cmdexpr_uniq_debug(p):
    """uniqcmd : UNIQ"""
    p[0] = ParseTreeNode('COMMAND', raw='uniq')

def p_error(p):
    raise SPLSyntaxError("Syntax error in uniq parser input!") 
