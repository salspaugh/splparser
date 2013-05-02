#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.appendlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_append(p):
    """cmdexpr : appendcmd"""
    p[0] = p[1]

def p_append(p):
    """appendcmd : APPEND"""
    p[0] = ParseTreeNode('APPEND')

def p_append_optionlist(p):
    """appendcmd : APPEND optionlist"""
    p[0] = ParseTreeNode('APPEND')
    p[0].add_children(p[2])

def p_optionlist_single(p):
    """optionlist : APPEND_OPT EQ field"""
    opt = ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt]

def p_optionlist(p):
    """optionlist : APPEND_OPT EQ field optionlist"""
    opt= ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in append parser input!")
