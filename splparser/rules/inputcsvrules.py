#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.inputcsvlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_inputcsv(p):
    """cmdexpr : inputcsvcmd"""
    p[0] = p[1]

def p_cmdexpr_inputcsv_single(p):
    """inputcsvcmd : INPUTCSV"""
    p[0] = ParseTreeNode('INPUTCSV')

def p_cmdexpr_inputcsv_field(p):
    """inputcsvcmd : INPUTCSV wc_stringlist value"""
    p[0] = ParseTreeNode('INPUTCSV')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_inputcsvcmd_inputcsv(p):
    """inputcsvcmd : INPUTCSV wc_stringlist
                   | INPUTCSV value"""
    p[0] = ParseTreeNode('INPUTCSV')
    p[0].add_child(p[2])

def p_inputcsv_opt(p):
    """wc_string : INPUTCSV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper(), option=True)
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_ainputcsv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_inputcsv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in inputcsv parser input!")
