#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.typeaheadlexer import tokens

BOOLEAN_OPTIONS = ["collapse"]

start = 'cmdexpr'

def p_cmdexpr(p):
    """cmdexpr : typeaheadcmd"""
    p[0] = p[1]

def p_cmdexpr_typeahead(p):
    """typeaheadcmd : TYPEAHEAD typeaheadarglist"""
    p[0] = ParseTreeNode('COMMAND', raw='typeahead')
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_typeaheadarglist_typeaheadargs(p):
    """typeaheadarglist : typeaheadarg
                        | typeaheadarg typeaheadarglist"""
    p[0] = ParseTreeNode('_TYPEAHEADARGLIST')
    p[0].add_child(p[1])
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_typeaheadarg_eq(p):
    """typeaheadarg : field EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    if p[1].raw in BOOLEAN_OPTIONS:
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_field_search_opt(p):
    """field : TYPEAHEAD_OPT"""
    p[0] = ParseTreeNode('OPTION', raw=p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in typeahead parser input!")
