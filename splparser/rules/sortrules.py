#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.sortlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_sort(p):
    """cmdexpr : sortcmd"""
    p[0] = p[1]

def p_sort_sortfields(p):
    """sortcmd : SORT sortfields"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2])

def p_sort_sortfields_desc(p):
    """sortcmd : SORT sortfields DESC"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    for c in p[2]:
        desc = ParseTreeNode('FUNCTION', raw='descending')
        if c.role == 'FUNCTION' and c.raw == 'ascending':
            c = c.children[0]
        desc.add_child(c)
        p[0].add_child(desc)

def p_sort_num_sortfields(p):
    """sortcmd : SORT int sortfields"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[2].role = 'VALUE'
    eq_node = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION')
    eq_node.add_children([opt_node, p[2]])
    p[0].add_children([eq_node] + p[3])

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
    p[0] = ParseTreeNode('FUNCTION', raw='ascending')
    i = 1 if len(p)==2 else 2
    p[0].add_child(p[i])

def p_sortfield_desc_func(p):
    """sortfield : MINUS sortfunc
                 | MINUS field
                 """
    p[0] = ParseTreeNode('FUNCTION', raw='descending')
    p[0].add_child(p[2])

def p_sortfunc(p):
    """sortfunc : SORT_FN LPAREN field RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(p[3])

def p_sortfunc_sortfunc(p):
    """sortfunc : SORT_FN LPAREN SORT_FN RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    field_node = ParseTreeNode('FIELD', nodetype='WORD', raw=p[3])
    p[0].add_child(field_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in sort parser input!")
