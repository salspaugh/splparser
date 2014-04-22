#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.strcatlexer import precedence, tokens

start = 'cmdexpr'

def p_strcat(p):
    """cmdexpr : STRCAT fieldlist"""
    for field_node in p[2].children:
        if field_node.nodetype == 'LITERAL':
            field_node.role = 'VALUE'
    p[0] = ParseTreeNode('COMMAND', raw='strcat')
    p[0].add_children(p[2].children)

def p_strcat_opt(p):
    """cmdexpr : STRCAT STRCAT_OPT EQ value fieldlist"""
    p[4].value = 'BOOLEAN'
    for field_node in p[2].children:
        if field_node.nodetype == 'LITERAL':
            field_node.role = 'VALUE'
    p[0] = ParseTreeNode('COMMAND', raw='strcat')
    eq_node = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[2])
    opt_node.values.append(p[4])
    p[0].add_child(eq_node)
    eq_node.add_child(opt_node)
    eq_node.add_child(p[4])
    p[0].add_children(p[5].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in strcat parser input!") 
