#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.xpathlexer import tokens

start = 'cmdexpr'

def p_cmdexpr(p):
    """cmdexpr : xpathcmd"""
    p[0] = p[1]

def p_cmdexpr_xpath(p):
    """xpathcmd : XPATH value"""
    p[0] = ParseTreeNode('COMMAND', raw='xpath')
    p[0].add_child(p[2])

def p_cmdexpr_xpath_opt_value_opt(p):
    """xpathcmd : XPATH wc_stringlist value wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='xpath')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])
    p[0].add_children(p[4].children)

def p_addtotalscmd_opt_value(p):
    """xpathcmd : XPATH wc_stringlist value"""
    p[0] = ParseTreeNode('COMMAND', raw='xpath')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_addtotalscmd_value_opt(p):
    """xpathcmd : XPATH value wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='xpath')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_xpath_opt(p):
    """wc_string : XPATH_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw in ["field", "outfield"]:
        p[3].role = 'FIELD'
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_xpath_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_xpath_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in xpath parser input!")
