#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.relevancylexer import tokens

start = 'cmdexpr'

def p_cmdexpr_relevancy(p):
    """cmdexpr : relevancycmd"""
    p[0] = p[1]

def p_cmdexpr_relevancy_debug(p):
    """relevancycmd : RELEVANCY"""
    p[0] = ParseTreeNode('COMMAND', raw='relevancy')

def p_error(p):
    raise SPLSyntaxError("Syntax error in relevancy parser input!") 
