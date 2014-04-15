#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.outputlookuplexer import tokens

start = 'cmdexpr'

boolean_options = ["append", "create_empty", "createinapp"]

def p_cmdexpr_outputlookup(p):
    """cmdexpr : outputlookupcmd"""
    p[0] = p[1]

def p_outputlookup_name(p):
    """outputlookupcmd : OUTPUTLOOKUP field"""
    p[0] = ParseTreeNode('COMMAND', raw='outputlookup')
    p[2].role = 'LOOKUP_TABLE'
    p[0].add_child(p[2])

def p_outputlookup_name_optionlist(p):
    """outputlookupcmd : OUTPUTLOOKUP field optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='outputlookup')
    p[2].role = 'LOOKUP_TABLE'
    p[0].add_children([p[2]] + p[3])

def p_outputlookup_optionlist_name(p):
    """outputlookupcmd : OUTPUTLOOKUP optionlist field"""
    p[0] = ParseTreeNode('COMMAND', raw='outputlookup')
    p[3].role = 'LOOKUP_TABLE'
    p[0].add_children(p[2] + [p[3]])

def p_optionlist_single(p):
    """optionlist : OUTPUTLOOKUP_OPT EQ field"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq]

def p_optionlist(p):
    """optionlist : OUTPUTLOOKUP_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in outputlookup parser input!")
