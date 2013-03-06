#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.deduplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_dedup(p):
    """cmdexpr : dedupcmd"""
    p[0] = p[1]

def p_dedup(p):
    """dedupcmd : DEDUP args"""
    p[0] = ParseTreeNode('DEDUP')
    p[0].add_children(p[2])


def p_dedup_args(p):
    """args : fieldlist"""
    p[0] = p[1].children

def p_dedup_args_field(p):
    """args : field fieldlist"""
    p[0] = [p[1]] + p[2].children

def p_dedup_args_option(p):
    """args : fieldlist optionlist"""
    p[0] = p[1].children + p[2]

def p_dedup_args_sort(p):
    """args : fieldlist sort"""
    p[0] = p[1].children + [p[2]]

def p_dedup_args_field_option(p):
    """args : field fieldlist optionlist"""
    p[0] = [p[1]] + p[2].children + p[3]

def p_dedup_args_field_sort(p):
    """args : field fieldlist sort"""
    p[0] = [p[1]] + p[2].children + [p[3]]

def p_dedup_args_option_sort(p):
    """args : fieldlist optionlist sort"""
    p[0] = p[1].children + p[2] + [p[3]]

def p_dedup_args_field_option_sort(p):
    """args : field fieldlist optionlist sort"""
    p[0] = [p[1]] + p[2].children + p[3] + [p[4]]

def p_optionlist(p):
    """optionlist : field EQ value optionlist"""
    option = ParseTreeNode('EQ')
    option.add_children([p[1], p[3]])
    p[0] = [option] + p[4]

def p_optionlist_one(p):
    """optionlist : field EQ value"""
    option = ParseTreeNode('EQ')
    option.add_children([p[1], p[3]])
    p[0] = [option]

def p_sort(p):
    """sort : SORTBY sortfields"""
    p[0] = ParseTreeNode('SORTBY')
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
    raise SPLSyntaxError("Syntax error in dedup parser input!")
