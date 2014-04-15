#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.regexrules import *

from splparser.lexers.regexlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_regex(p):
    """cmdexpr : regexcmd"""
    p[0] = p[1]

def p_regexcmd_regex(p):
    """regexcmd : REGEX regex_field
                | REGEX regex_nofield"""
    p[0] = ParseTreeNode('COMMAND', raw='regex')
    p[0].add_children(p[2].children)

def p_regex(p):
    """regex_nofield : regex"""
    p[0] = ParseTreeNode('_REGEX_ARGS')
    match = ParseTreeNode('MATCH')
    field = ParseTreeNode('INTERNAL_FIELD', nodetype='ID', raw='_raw') 
    p[0].add_children([field, p[1], match])

def p_regex_eq(p):
    """regex_field : field EQ regex
                   | regex EQ regex"""
    if p[1].role == 'VALUE':
        p[1].role = 'FIELD'
    p[0] = ParseTreeNode('_REGEX_ARGS')
    match = ParseTreeNode('MATCH')
    p[0].add_children([p[1], p[3], match])

def p_regex_neq(p):
    """regex_field : field NEQ regex
                   | regex NEQ regex"""
    if p[1].role == 'VALUE':
        p[1].role = 'FIELD'
    p[0] = ParseTreeNode('_REGEX_ARGS')
    match = ParseTreeNode('NOT_MATCH')
    p[0].add_children([p[1], p[3], match])

def p_error(p):
    raise SPLSyntaxError("Syntax error in regex parser input!") 

