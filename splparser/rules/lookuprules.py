#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.lookuplexer import tokens

start = 'cmdexpr'

boolean_options = ["update", "local"]

def p_cmdexpr_lookup(p):
    """cmdexpr : lookupcmd"""
    p[0] = p[1]

def p_lookup_tablename(p):
    """lookupcmd : LOOKUP field table"""
    p[0] = ParseTreeNode('COMMAND', raw='lookup')
    lookup_node = ParseTreeNode('LOOKUP_TABLE', raw=p[2].raw)
    p[0].add_children([lookup_node] + p[3])

def p_lookup_options_tablename(p):
    """lookupcmd :  LOOKUP field EQ value field table"""
    p[0] = ParseTreeNode('COMMAND', raw='lookup')
    if p[2].raw in boolean_options:
        p[4].nodetype = 'BOOLEAN'
    lookup_node = ParseTreeNode('LOOKUP_TABLE', raw=p[5].raw)
    eq_node = ParseTreeNode('EQ', raw='assign')
    option = ParseTreeNode('OPTION', raw=p[2].raw)
    eq_node.add_children([option, p[4]])
    p[0].add_children([eq_node, lookup_node] + p[6])

def p_table_tablename(p):
    """table : fieldlist"""
    p[0] = p[1].children

def p_table_tablename_field_output(p):
    """table : fieldlist out"""
    table = p[1].children
    table.append(p[2])
    p[0] = table

def p_field_as(p):
    """field : field ASLC field
             | field ASUC field"""
    as_node = ParseTreeNode('AS')
    as_node.add_child(p[3])
    p[1].add_child(as_node)
    p[0] = p[1]

def p_out(p):
    """out : OUTPUT fieldlist
           | OUTPUTNEW fieldlist"""
    p[0] = ParseTreeNode(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in lookup parser input!")
