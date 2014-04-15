#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.gaugelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_gauge(p):
    """cmdexpr : gaugecmd"""
    p[0] = p[1]

def p_cmdexpr_gauge_single(p):
    """gaugecmd : GAUGE"""
    p[0] = ParseTreeNode('COMMAND', raw='gauge')

def p_gaugecmd_gauge(p):
    """gaugecmd : GAUGE fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='gauge')
    for c in p[2].children:
        if c.nodetype == 'INT':
            c.role = 'VALUE'
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in gauge parser input!")
