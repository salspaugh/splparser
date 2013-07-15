#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.addinfolexer import tokens

start = 'cmdexpr'

def p_cmdexpr_addinfo(p):
    """cmdexpr : addinfocmd"""
    p[0] = p[1]

def p_cmdexpr_addinfo_debug(p):
    """addinfocmd : ADDINFO"""
    p[0] = ParseTreeNode('COMMAND', raw='addinfo')

def p_error(p):
    raise SPLSyntaxError("Syntax error in addinfo parser input!") 
