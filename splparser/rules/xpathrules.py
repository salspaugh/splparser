#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.xpathlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_xpath(p):
    """cmdexpr : xpathcmd"""
    p[0] = p[1]

def p_cmdexpr_xpath_single(p):
    """xpathcmd : XPATH"""
    p[0] = ParseTreeNode('XPATH')

def p_cmdexpr_xpath_field(p):
    """xpathcmd : XPATH wc_stringlist field"""
    p[0] = ParseTreeNode('XPATH')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_cmdexpr_xpath_field_list(p):
    """xpathcmd : XPATH wc_stringlist field wc_stringlist"""
    p[0] = ParseTreeNode('XPATH')
    p[0].add_children(p[2].children)
    p[0].add_child([p[3],p[4]])

def p_addtotalscmd_xpath(p):
    """xpathcmd : XPATH wc_stringlist
                | XPATH field"""
    p[0] = ParseTreeNode('XPATH')
    p[0].add_child(p[2])

def p_xpath_opt(p):
    """wc_string : XPATH_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode(p[1].upper(), option=True)
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

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
