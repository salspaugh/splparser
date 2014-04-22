#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.makemvlexer import tokens

start = 'cmdexpr'

boolean_options = ["allowempty", "setsv"]

def p_cmdexpr_makemv(p):
    """cmdexpr : makemvcmd"""
    p[0] = p[1]

def p_cmdexpr_makemv_single(p):
    """makemvcmd : MAKEMV"""
    p[0] = ParseTreeNode('COMMAND', raw='makemv')

def p_cmdexpr_makemv_field(p):
    """makemvcmd : MAKEMV wc_stringlist field"""
    p[0] = ParseTreeNode('COMMAND', raw='makemv')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_addtotalscmd_makemv(p):
    """makemvcmd : MAKEMV field"""
    p[0] = ParseTreeNode('COMMAND', raw='makemv')
    p[0].add_child(p[2])

def p_makemv_opt_comma(p):
    """wc_string : MAKEMV_OPT EQ COMMA"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    p[3] = ParseTreeNode('VALUE', nodetype='LITERAL', raw=p[3])
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_makemv_opt(p):
    """wc_string : MAKEMV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    p[1].values.append(p[3])
    if p[3].raw in boolean_options:
        p[3].nodetype = "BOOLEAN"
    p[0].add_children([p[1], p[3]])

def p_makemv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_makemv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in makemv parser input!")
