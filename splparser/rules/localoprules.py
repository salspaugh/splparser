#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.localoplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_localop(p):
    """cmdexpr : localopcmd"""
    p[0] = p[1]

def p_cmdexpr_localop_debug(p):
    """localopcmd : LOCALOP"""
    p[0] = ParseTreeNode('COMMAND', raw='localop')

def p_error(p):
    raise SPLSyntaxError("Syntax error in localop parser input!") 
