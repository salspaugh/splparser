#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *
from splparser.rules.common.regexrules import *

from splparser.lexers.extractlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_extractkv(p):
    """cmdexpr : extractkvcmd"""
    p[0] = p[1]

def p_cmdexpr_extractkv_single(p):
    """extractkvcmd : EXTRACT
                    | KV"""
    p[0] = ParseTreeNode(p[1])

def p_cmdexpr_extractkv_field(p):
    """extractkvcmd : EXTRACT wc_stringlist fieldlist
                    | KV wc_stringlist fieldlist"""
    p[0] = ParseTreeNode(p[1])
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_extractkvcmd_extractkv(p):
    """extractkvcmd : EXTRACT wc_stringlist
                    | EXTRACT fieldlist
                    | KV wc_stringlist
                    | KV fieldlist"""
    p[0] = ParseTreeNode(p[1])
    p[0].add_children(p[2].children)

def p_extractkv_opt(p):
    """wc_string : EXTRACTKV_OPT EQ value COMMA
                 | EXTRACTKV_OPT EQ value
                 | EXTRACTKV_OPT EQ regex"""
    p[0] = ParseTreeNode('EQ')
    p[1] = ParseTreeNode(p[1].upper())
    p[0].add_children([p[1],p[3]])

def p_extractkv_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])

def p_extractkv_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in extract parser input!")
