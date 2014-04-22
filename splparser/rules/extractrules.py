#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *
from splparser.rules.common.regexrules import *

from splparser.lexers.extractlexer import tokens

start = 'cmdexpr'

boolean_options = ["auto", "clean_keys", "mv_add", "reload", "segment"]

def p_cmdexpr_extractkv(p):
    """cmdexpr : extractkvcmd"""
    p[0] = p[1]

def p_cmdexpr_extractkv_single(p):
    """extractkvcmd : EXTRACT
                    | KV"""
    p[0] = ParseTreeNode('COMMAND', raw="extract")

def p_cmdexpr_extractkv_both(p):
    """extractkvcmd : EXTRACT wc_stringlist field
                    | KV wc_stringlist field"""
    p[0] = ParseTreeNode('COMMAND', raw="extract")
    p[0].add_children(p[2].children)
    p[3].role = 'EXTRACTOR_NAME'
    p[0].add_child(p[3])

def p_extractkvcmd_extractkv_field(p):
    """extractkvcmd : EXTRACT field
                    | KV field"""
    p[0] = ParseTreeNode('COMMAND', raw="extract")
    p[2].role = 'EXTRACTOR_NAME'
    p[0].add_child(p[2])

def p_extractkvcmd_extractkv_opts(p):
    """extractkvcmd : EXTRACT wc_stringlist
                    | KV wc_stringlist"""
    p[0] = ParseTreeNode('COMMAND', raw="extract")
    p[0].add_children(p[2].children)

def p_extractkv_opt(p):
    """wc_string : EXTRACTKV_OPT EQ value COMMA
                 | EXTRACTKV_OPT EQ value
                 | EXTRACTKV_OPT EQ regex"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    if p[1].raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_extractkv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_extractkv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in extract parser input!")
