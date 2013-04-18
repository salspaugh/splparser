#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.gaugelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_gauge(p):
    """cmdexpr : gaugecmd"""
    p[0] = p[1]

def p_cmdexpr_gauge_single(p):
    """gaugecmd : GAUGE"""
    p[0] = ParseTreeNode('GAUGE')

def p_gaugecmd_gauge(p):
    """gaugecmd : GAUGE wc_stringlist"""
    p[0] = ParseTreeNode('GAUGE')
    p[0].add_children(p[2].children)

def p_gauge_opt_list(p):
    """wc_stringlist : field"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_gauge_optlist(p):
    """wc_stringlist : field wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in gauge parser input!")
