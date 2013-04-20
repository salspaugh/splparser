#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.outputlookuplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_outputlookup(p):
    """cmdexpr : outputlookupcmd"""
    p[0] = p[1]

def p_outputlookup_name(p):
    """outputlookupcmd : OUTPUTLOOKUP field"""
    p[0] = ParseTreeNode('OUTPUTLOOKUP')
    p[0].add_child(p[2])

def p_outputlookup_name_optionlist(p):
    """outputlookupcmd : OUTPUTLOOKUP field optionlist"""
    p[0] = ParseTreeNode('OUTPUTLOOKUP')
    p[0].add_children([p[2]] + p[3])

def p_outputlookup_optionlist_name(p):
    """outputlookupcmd : OUTPUTLOOKUP optionlist field"""
    p[0] = ParseTreeNode('OUTPUTLOOKUP')
    p[0].add_children(p[2] + [p[3]])

def p_optionlist_single(p):
    """optionlist : OUTPUTLOOKUP_OPT EQ field"""
    opt = ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt]

def p_optionlist(p):
    """optionlist : OUTPUTLOOKUP_OPT EQ field optionlist"""
    opt= ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in outputlookup parser input!")
