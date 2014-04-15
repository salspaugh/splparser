
#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.appendcolslexer import tokens

start = 'cmdexpr'

boolean_options = ["override"]

def p_cmdexpr_appendcols(p):
    """cmdexpr : appendcolscmd"""
    p[0] = p[1]

def p_appendcols(p):
    """appendcolscmd : APPENDCOLS"""
    p[0] = ParseTreeNode('COMMAND', raw='appendcols')

def p_appendcols_optionlist(p):
    """appendcolscmd : APPENDCOLS optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='appendcols')
    p[0].add_children(p[2])

def p_optionlist_single(p):
    """optionlist : APPENDCOLS_OPT EQ field"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq]

def p_optionlist(p):
    """optionlist : APPENDCOLS_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in appendcols parser input!")
