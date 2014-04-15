#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.outlierlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_outlier(p):
    """cmdexpr : outliercmd"""
    p[0] = p[1]

def p_cmdexpr_outlier_field(p):
    """outliercmd : OUTLIER wc_stringlist fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='outlier')
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_outliercmd_outlier(p):
    """outliercmd : OUTLIER wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='outlier')
    p[0].add_children(p[2].children)

def p_outlier_opt(p):
    """wc_string : OUTLIER_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw == "uselower":
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_outlier_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_outlier_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in outlier parser input!")
