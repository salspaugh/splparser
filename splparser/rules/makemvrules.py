#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.makemvlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_addtotals(p):
    """cmdexpr : makemvcmd"""
    p[0] = p[1]

def p_cmdexpr_addtotals_single(p):
    """makemvcmd : MAKEMV"""
    p[0] = ParseTreeNode('MAKEMV')

def p_cmdexpr_addtotals_field(p):
    """makemvcmd : MAKEMV wc_stringlist field"""
    p[0] = ParseTreeNode('MAKEMV')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_addtotalscmd_addtotals(p):
    """makemvcmd : MAKEMV wc_stringlist
                    | MAKEMV field"""
    p[0] = ParseTreeNode('MAKEMV')
    p[0].add_child(p[2])

def p_addtotals_opt_comma(p):
    """wc_string : MAKEMV_OPT EQ COMMA"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper())
    p[3] = ParseTreeNode(p[3])
    p[0].add_children([p[1],p[3]])

def p_addtotals_opt(p):
    """wc_string : MAKEMV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper())
    p[0].add_children([p[1],p[3]])

def p_addtotals_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_addtotals_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in makemv parser input!")
