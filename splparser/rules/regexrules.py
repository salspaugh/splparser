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
    """regexcmd : REGEX regex_req
                | REGEX regex"""
    p[0] = ParseTreeNode('REGEX')
    p[0].add_child(p[2])

def p_regex_eq(p):
    """regex_req : field EQ regex"""
    p[0] = ParseTreeNode('EQ')
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_regex_neq(p):
    """regex_req : field NEQ regex"""
    p[0] = ParseTreeNode('NEQ')
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_error(p):
    raise SPLSyntaxError("Syntax error in regex parser input!") 

