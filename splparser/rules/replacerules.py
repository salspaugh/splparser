#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.replacelexer import tokens

start = 'cmdexpr'

def p_cmdexpr_replace(p):
    """cmdexpr : replacecmd"""
    p[0] = p[1]

def p_replacecmd_replace(p):
    """replacecmd : REPLACE wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw='replace')
    p[0].add_children(p[2].children)

def p_replace_wc(p):
    """wc_string : value WITH value"""
    p[0] = ParseTreeNode('WITH')
    p[0].add_children([p[1],p[3]])

def p_replace_wc_empty(p):
    """wc_string : value WITH EMPTY"""
    p[0] = ParseTreeNode('WITH')
    p[3] = ParseTreeNode('VALUE', nodetype='LITERAL', raw=p[3])
    p[0].add_children([p[1],p[3]])
    
def p_replace_wc_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('WITH')
    p[0].add_child(p[1])
    
def p_replace_comma_wclist(p):
    """wc_stringlist : wc_string COMMA wc_stringlist"""
    p[0] = ParseTreeNode('WITH')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_replace_wclist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('WITH')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_replace_in(p):
    """replacecmd : REPLACE wc_stringlist in_field"""
    p[0] = ParseTreeNode('COMMAND', raw='replace')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_replace_in_field(p):
    """in_field : IN fieldlist"""
    p[0] = ParseTreeNode('IN')
    p[0].add_children(p[2].children)
    
def p_error(p):
    raise SPLSyntaxError("Syntax error in replace parser input!") 

