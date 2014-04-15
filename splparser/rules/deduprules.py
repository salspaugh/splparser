#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.deduplexer import tokens

start = 'cmdexpr'

boolean_options = ["consecutive", "keepempty", "keepevents"]

def p_cmdexpr_dedup(p):
    """cmdexpr : dedupcmd"""
    p[0] = p[1]

def p_dedup(p):
    """dedupcmd : DEDUP args"""
    p[0] = ParseTreeNode('COMMAND', raw='dedup')
    p[0].add_children(p[2])

def p_dedup_args(p):
    """args : fieldlist"""
    p[0] = p[1].children

def p_dedup_args_field(p):
    """args : INT fieldlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='n')
    int = ParseTreeNode('VALUE', nodetype='INT', raw=p[1], is_argument=True)
    eq.add_children([opt, int])
    p[0] = [eq] + p[2].children

def p_dedup_args_option(p):
    """args : fieldlist optionlist"""
    p[0] = p[1].children + p[2]

def p_dedup_args_sort(p):
    """args : fieldlist sort"""
    p[0] = p[1].children + [p[2]]

def p_dedup_args_field_option(p):
    """args : INT fieldlist optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='n')
    int = ParseTreeNode('VALUE', nodetype='INT', raw=p[1], is_argument=True)
    eq.add_children([opt, int])
    p[0] = [eq] + p[2].children + p[3]

def p_dedup_args_field_sort(p):
    """args : INT fieldlist sort"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='n')
    int = ParseTreeNode('VALUE', nodetype='INT', raw=p[1], is_argument=True)
    eq.add_children([opt, int])
    p[0] = [eq] + p[2].children + [p[3]]

def p_dedup_args_option_sort(p):
    """args : fieldlist optionlist sort"""
    p[0] = p[1].children + p[2] + [p[3]]

def p_dedup_args_field_option_sort(p):
    """args : INT fieldlist optionlist sort"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='n')
    int = ParseTreeNode('VALUE', nodetype='INT', raw=p[1], is_argument=True)
    eq.add_children([opt, int])
    p[0] = [eq] + p[2].children + p[3] + [p[4]]

def p_optionlist(p):
    """optionlist : DEDUP_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[4]

def p_optionlist_comma(p):
    """optionlist : DEDUP_OPT EQ field COMMA optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[5]

def p_optionlist_one(p):
    """optionlist : DEDUP_OPT EQ field"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq]

def p_sort(p):
    """sort : SORTBY sortfields"""
    p[0] = ParseTreeNode('FUNCTION', raw='sortby')
    p[0].add_children(p[2])

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
    """sortfunc : WORD LPAREN field RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in dedup parser input!")
