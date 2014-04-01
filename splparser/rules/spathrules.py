#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.spathlexer import tokens

start = 'cmdexpr'

def p_cmdexpr(p):
    """cmdexpr : spathcmd"""
    p[0] = p[1]

def p_cmdexpr_spath(p):
    """spathcmd : SPATH
                | SPATH spatharglist"""
    p[0] = ParseTreeNode('COMMAND', raw='spath')
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_spatharglist_spathargs(p):
    """spatharglist : spatharg
                    | spatharg spatharglist"""
    p[0] = ParseTreeNode('_SPATHARGLIST')
    p[0].add_child(p[1])
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_spatharg_opt(p):
    """spatharg : SPATH_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    if opt.raw in ["input", "output"]:
        p[3].role = 'FIELD'
    opt.values.append(p[3])
    p[0].add_children([opt, p[3]])

def p_spatharg_path(p):
    """spatharg : value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='path')
    opt.values.append(p[1])
    p[0].add_children([opt, p[1]])

def p_error(p):
    raise SPLSyntaxError("Syntax error in spath parser input!")
