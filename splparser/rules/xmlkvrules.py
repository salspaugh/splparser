#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.xmlkvlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_xmlkv(p):
    """cmdexpr : xmlkvcmd"""
    p[0] = p[1]

def p_cmdexpr_xmlkv_single(p):
    """xmlkvcmd : XMLKV"""
    p[0] = ParseTreeNode('COMMAND', raw='xmlkv')

def p_cmdexpr_xmlkv_field(p):
    """xmlkvcmd : XMLKV wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='xmlkv')
    p[0].add_children(p[2].children)

def p_xmlkv_opt(p):
    """wc_string : XMLKV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_xmlkv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_xmlkv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in xmlkv parser input!")
