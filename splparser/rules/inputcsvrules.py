#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.inputcsvlexer import tokens

start = 'cmdexpr'

boolean_options = ["append", "events"]

def p_cmdexpr_inputcsv(p):
    """cmdexpr : inputcsvcmd"""
    p[0] = p[1]

def p_cmdexpr_inputcsv_field(p):
    """inputcsvcmd : INPUTCSV wc_stringlist value"""
    p[0] = ParseTreeNode('COMMAND', raw='inputcsv')
    p[0].add_children(p[2].children)
    p[3].role = 'FILENAME'
    p[0].add_child(p[3])

def p_inputcsvcmd_inputcsv(p):
    """inputcsvcmd : INPUTCSV wc_stringlist
                   | INPUTCSV value"""
    p[0] = ParseTreeNode('COMMAND', raw='inputcsv')
    p[0].add_child(p[2])
    if len(p[2].children) == 0:
        p[2].role = 'FILENAME'

def p_inputcsv_opt(p):
    """wc_string : INPUTCSV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_ainputcsv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_inputcsv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in inputcsv parser input!")
