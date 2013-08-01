#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.exportlexer import precedence , tokens

start = 'cmdexpr'

def p_cmdexpr_export(p):
    """cmdexpr : exportcmd"""
    p[0] = p[1]

def p_cmdexpr_export_debug(p):
    """exportcmd : EXPORT"""
    p[0] = ParseTreeNode('COMMAND', raw='export')

def p_export_fieldlist(p):
    """exportcmd : EXPORT FORMAT EQ field fieldlist"""
    p[4].role = 'VALUE'
    p[0] = ParseTreeNode('COMMAND', raw='export')
    eq_node = ParseTreeNode('EQ', raw='assign')
    format_node = ParseTreeNode('OPTION', raw=p[2])
    format_node.values.append(p[4])
    p[0].add_child(eq_node)
    eq_node.add_child(format_node)
    eq_node.add_child(p[4])
    p[0].add_children(p[5].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in export parser input!") 
