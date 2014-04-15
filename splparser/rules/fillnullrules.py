#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.fillnulllexer import tokens

start = 'cmdexpr'

def p_cmdexpr_fillnull(p):
    """cmdexpr : fillnullcmd"""
    p[0] = p[1]

def p_fillnullcmd_fieldlist(p):
    """fillnullcmd : FILLNULL fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[0].add_children(p[2].children)

def p_fieldlist(p):
    """fillnullcmd : FILLNULL fillvalue fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_fillvalue(p):
    """fillnullcmd : FILLNULL fillvalue"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[0].add_child(p[2])

def p_fillnull_macro(p):
    """fillnullcmd : FILLNULL MACRO"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[1] = ParseTreeNode('MACRO', raw=p[1], is_argument=True)
    p[0].add_child(p[1])

def p_fillnull_value_macro(p):
    """fillnullcmd : FILLNULL fillvalue MACRO"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[3] = ParseTreeNode('MACRO', raw=p[3], is_argument=True)
    p[0].add_child(p[2])
    p[0].add_child(p[3])

def p_fillnullcmd_value_macro_field(p):
    """fillnullcmd : FILLNULL fillvalue MACRO fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[3] = ParseTreeNode('MACRO', raw=p[3], is_argument=True)
    p[0].add_child(p[2])
    p[0].add_child(p[3])
    p[0].add_children(p[4].children)

def p_fillnullcmd_value_macro_comma_field(p):
    """fillnullcmd : FILLNULL fillvalue MACRO COMMA fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw='fillnull')
    p[3] = ParseTreeNode('MACRO', raw=p[3], is_argument=True)
    p[0].add_child(p[2])
    p[0].add_child(p[3])
    p[0].add_children(p[5].children)

def p_value(p):
    """fillvalue : VALUE EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode('OPTION', raw=p[1])
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_error(p):
    raise SPLSyntaxError("Syntax error in fillnull parser input!") 
