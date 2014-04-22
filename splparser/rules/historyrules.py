#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.historylexer import tokens

BOOLEAN_OPTIONS = ["events"]

start = 'cmdexpr'

def p_cmdexpr_history(p):
    """cmdexpr : historycmd"""
    p[0] = p[1]

def p_cmdexpr_history_single(p):
    """historycmd : HISTORY"""
    p[0] = ParseTreeNode('COMMAND', raw='history')

def p_cmdexpr_history_field(p):
    """historycmd : HISTORY wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='history')
    p[0].add_children(p[2].children)

def p_history_opt(p):
    """wc_string : INPUTCSV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw in BOOLEAN_OPTIONS:
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_history_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_history_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in history parser input!")
