#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.filldownlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_filldown(p):
    """cmdexpr : filldowncmd"""
    p[0] = p[1]

def p_cmdexpr_filldown_debug(p):
    """filldowncmd : FILLDOWN"""
    p[0] = ParseTreeNode('COMMAND', raw='filldown')

def p_filldown_fieldlist(p):
    """filldowncmd : FILLDOWN fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='filldown')
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in filldown parser input!") 
