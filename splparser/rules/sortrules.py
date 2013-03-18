#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.sortlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_sort(p):
    """cmdexpr : sortcmd"""
    p[0] = p[1]

def p_sort_sortfields(p):
    """sortcmd : SORT sortfields"""
    p[0] = ParseTreeNode('SORT')
    p[0].add_children(p[2])

def p_sort_num_sortfields(p):
    """sortcmd : SORT value sortfields"""
    p[0] = ParseTreeNode('SORT')
    p[0].add_children([p[2]] + p[3])

def p_sort_num_limit_sortfields(p):
    """sortcmd : SORT field EQ value sortfields"""
    p[0] = ParseTreeNode('SORT')
    p[0].add_children([p[4]] + p[5])

def p_sortfields_list(p):
    """sortfields : sortfield COMMA sortfields"""
    p[0] = [p[1]] + p[3]

def p_sortfields_single(p):
    """sortfields : sortfield"""
    p[0] = [p[1]]

def p_sortfield_asc_func(p):
    """sortfield : PLUS sortfunc
                 | PLUS field
                 | sortfunc
                 | field
                 """
    p[0] = ParseTreeNode('ASCENDING')
    i = 1 if len(p)==2 else 2
    p[0].add_child(p[i])

def p_sortfield_desc_func(p):
    """sortfield : MINUS sortfunc
                 | MINUS field
                 """
    p[0] = ParseTreeNode('DESCENDING')
    p[0].add_child(p[2])

def p_sortfunc(p):
    """sortfunc : WORD LPAREN field RPAREN"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in sort parser input!")
