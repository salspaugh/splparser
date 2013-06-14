
#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.appendcolslexer import tokens

start = 'cmdexpr'

def p_cmdexpr_appendcols(p):
    """cmdexpr : appendcolscmd"""
    p[0] = p[1]

def p_appendcols(p):
    """appendcolscmd : APPENDCOLS"""
    p[0] = ParseTreeNode('APPENDCOLS')

def p_appendcols_optionlist(p):
    """appendcolscmd : APPENDCOLS optionlist"""
    p[0] = ParseTreeNode('APPENDCOLS')
    p[0].add_children(p[2])

def p_optionlist_single(p):
    """optionlist : APPENDCOLS_OPT EQ field"""
    opt = ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt]

def p_optionlist(p):
    """optionlist : APPENDCOLS_OPT EQ field optionlist"""
    opt= ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in appendcols parser input!")
