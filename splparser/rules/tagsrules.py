#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.tagslexer import tokens

start = 'cmdexpr'

def p_cmdexpr_tags(p):
    """cmdexpr : tagscmd"""
    p[0] = p[1]

def p_cmdexpr_tags_single(p):
    """tagscmd : TAGS"""
    p[0] = ParseTreeNode('TAGS')

def p_cmdexpr_TAGS_field(p):
    """tagscmd : TAGS wc_stringlist fieldlist"""
    p[0] = ParseTreeNode('TAGS')
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_tagscmd_tags(p):
    """tagscmd : TAGS fieldlist
               | TAGS wc_stringlist"""
    p[0] = ParseTreeNode('TAGS')
    p[0].add_children(p[2].children)

def p_tags_opt(p):
    """wc_string : TAGS_OPT EQ value"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper())
    p[0].add_children([p[1], p[3]])

def p_tags_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_tags_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in tags parser input!")
