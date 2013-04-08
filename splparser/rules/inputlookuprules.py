#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.inputlookuplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_inputlookup(p):
    """cmdexpr : inputlookupcmd"""
    p[0] = p[1]

def p_inputlookup_name(p):
    """inputlookupcmd : INPUTLOOKUP field"""
    p[0] = ParseTreeNode('INPUTLOOKUP')
    p[0].add_child(p[2])

def p_inputlookup_name_optionlist(p):
    """inputlookupcmd : INPUTLOOKUP field optionlist"""
    p[0] = ParseTreeNode('INPUTLOOKUP')
    p[0].add_children([p[2]] + p[3])

def p_inputlookup_optionlist_name(p):
    """inputlookupcmd : INPUTLOOKUP optionlist field"""
    p[0] = ParseTreeNode('INPUTLOOKUP')
    p[0].add_children(p[2] + [p[3]])

def p_optionlist_single(p):
    """optionlist : INPUTLOOKUP_OPT EQ field"""
    eq = ParseTreeNode('EQ')
    eq.add_children([ParseTreeNode('WORD', raw=p[1], arg=True), p[3]])
    p[0] = [eq]

def p_optionlist(p):
    """optionlist : INPUTLOOKUP_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ')
    eq.add_children([ParseTreeNode('WORD', raw=p[1], arg=True), p[3]])
    p[0] = [eq] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in inputlookup parser input!")
