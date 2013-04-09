#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.transposelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_transpose(p):
    """cmdexpr : transposecmd"""
    p[0] = p[1]

def p_cmdexpr_transpose_debug(p):
    """transposecmd : TRANSPOSE"""
    p[0] = ParseTreeNode('TRANSPOSE')

def p_transpose_int(p):
	"""transposecmd : TRANSPOSE value"""
	p[0] = ParseTreeNode('TRANSPOSE')
	p[0].add_child(p[2])

def p_error(p):
    raise SPLSyntaxError("Syntax error in transpose parser input!") 
