#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.multikvlexer import tokens

start = 'cmdexpr'

boolean_options = ["copyattrs", "noheader", "rmorig", "multitable"]

def p_cmdexpr_multikvs(p):
    """cmdexpr : multikvcmd"""
    p[0] = p[1]

def p_multikv_multikvopt_fieldlist(p):
    """multikvcmd : MULTIKV multikvoptlist"""
    p[0] = ParseTreeNode('COMMAND', raw='multikv')
    p[0].add_children(p[2].children)

def p_conf_multikvoptlist(p):
    """multikvcmd : MULTIKV conf multikvoptlist"""
    p[0] = ParseTreeNode('COMMAND', raw='multikv')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)
    
def p_conf(p):
    """conf : CONF EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_multikvoptlist(p):
    """multikvoptlist : multikvopt"""
    p[0] = ParseTreeNode('_MULTIKV_OPT_LIST')
    p[0].add_child(p[1])

def p_multikvoptlist_multikvopt(p):
    """multikvoptlist : multikvopt multikvoptlist"""
    p[0] = ParseTreeNode('_MULTIKV_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children) 

def p_multikvopt(p):
    """multikvopt : MULTIKV_SINGLE_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    if opt_node.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_multipkopt_listopt(p):
    """multikvopt : MULTIKV_LIST_OPT fieldlist"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[2].children)

def p_multikvopt_equal(p):
    """multikvopt : MULTIKV_LIST_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in multikv parser input!") 
