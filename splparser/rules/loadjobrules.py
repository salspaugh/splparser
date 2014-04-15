#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.loadjoblexer import tokens

start = 'cmdexpr'

boolean_options = ["result-event", "ignore_running"]

def p_cmdexpr_loadjob(p):
    """cmdexpr : loadjobcmd"""
    p[0] = p[1]

def p_loadjob_value(p):
    """loadjobcmd : LOADJOB value"""
    p[0] = ParseTreeNode('COMMAND', raw='loadjob')
    p[0].add_child(p[2])

def p_loadjob_value_wcstringlist(p):
    """loadjobcmd : LOADJOB value wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='loadjob')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_loadjob_wcstringlist(p):
    """loadjobcmd : LOADJOB wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='loadjob')
    p[0].add_children(p[2].children)

def p_wcstring(p):
    """wc_string : LOADJOB_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_wcstringlist(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_wcstring_wcstringlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in loadjob parser input!")
