#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.joinlexer import tokens

start = 'cmdexpr'

boolean_options = ["usetime", "earlier", "overwrite"]

def p_cmdexpr_join(p):
    """cmdexpr : joincmd"""
    p[0] = p[1]

def p_join(p):
    """joincmd : JOIN"""
    p[0] = ParseTreeNode('COMMAND', raw='join')

def p_join_optionlist(p):
    """joincmd : JOIN optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='join')
    p[0].add_children(p[2])

def p_join_optionlist_fieldlist(p):
    """joincmd : JOIN optionlist fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='join')
    p[0].add_children(p[2] + p[3].children)

def p_optionlist_single(p):
    """optionlist : JOIN_OPT EQ field"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq]

def p_optionlist(p):
    """optionlist : JOIN_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in join parser input!")
