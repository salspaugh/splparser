#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.xmlkvlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_xmlkv(p):
    """cmdexpr : xmlkvcmd"""
    p[0] = p[1]

def p_cmdexpr_xmlkv_debug(p):
    """xmlkvcmd : XMLKV"""
    p[0] = ParseTreeNode('XMLKV')

def p_transpose_int(p):
	"""xmlkvcmd : XMLKV MAXINPUTS EQ value"""
	p[0] = ParseTreeNode('XMLKV')
	Node = ParseTreeNode('EQ')
	Node_2 = ParseTreeNode('MAXINPUTS')
	Node.add_children([Node_2, p[4]])
	p[0].add_child(Node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in xmlkv parser input!") 
