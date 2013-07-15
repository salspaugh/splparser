#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.deletelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_delete(p):
    """cmdexpr : deletecmd"""
    p[0] = p[1]

def p_cmdexpr_delete_debug(p):
    """deletecmd : DELETE"""
    p[0] = ParseTreeNode('COMMAND', raw='delete')

def p_error(p):
    raise SPLSyntaxError("Syntax error in delete parser input!") 
