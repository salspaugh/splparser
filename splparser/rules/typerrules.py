#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.typerlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_typer(p):
    """cmdexpr : typercmd"""
    p[0] = p[1]

def p_cmdexpr_typer_debug(p):
    """typercmd : TYPER"""
    p[0] = ParseTreeNode('COMMAND', raw='typer')

def p_error(p):
    raise SPLSyntaxError("Syntax error in typer parser input!") 
