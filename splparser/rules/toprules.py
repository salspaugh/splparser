#!/usr/bin/env python

from splparser.parsetree import *

from splparser.rules.common.byrules import *
from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.toplexer import tokens

start = 'cmdexpr'

def p_cmdexpr_top(p):
    """cmdexpr : topcmd"""
    p[0] = p[1]

def p_top_fieldlist(p):
    """topcmd : TOP fieldlist
              | SITOP fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2].children)

def p_top_fieldlist_by(p):
    """topcmd : TOP fieldlist by fieldlist
              | SITOP fieldlist by fieldlist"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    by_node = ParseTreeNode('FUNCTION', raw='groupby')
    by_node.add_children(p[2].children)
    for c in p[4].children:
        c.role = 'GROUPING_' + c.role
    by_node.add_children(p[4].children)
    p[0].add_child(by_node)

def p_top_topopt_fieldlist(p):
    """topcmd : TOP topoptlist fieldlist
              | SITOP topoptlist fieldlist
              | TOP fieldlist topoptlist
              | SITOP fieldlist topoptlist"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_top_topopt_fieldlist_by(p):
    """topcmd : TOP topoptlist fieldlist by fieldlist
              | SITOP topoptlist fieldlist by fieldlist"""
    by_node = ParseTreeNode('FUNCTION', raw='groupby')
    by_node.add_children(p[3].children)
    for c in p[5].children:
        c.role = 'GROUPING_' + c.role
    by_node.add_children(p[5].children)
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2].children)
    p[0].add_child(by_node)

def p_topoptlist(p):
    """topoptlist : topopt"""
    p[0] = ParseTreeNode('_TOP_OPT_LIST')
    p[0].add_child(p[1])

def p_topoptlist_topopt(p):
    """topoptlist : topopt topoptlist"""
    p[0] = ParseTreeNode('_TOP_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children) 

def p_topopt(p):
    """topopt : TOP_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    if p[1] in ['showcount', 'showperc', 'useother']:
        p[3].nodetype = 'BOOLEAN'
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_topopt_commonopt(p):
    """topopt : COMMON_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    if p[1] == 'limit':
        p[3].nodetype = 'INT'
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in top parser input!") 
