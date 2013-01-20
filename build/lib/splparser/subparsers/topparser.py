#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_top(p):
    """cmdexpr : topcmd"""
    p[0] = p[1]

def p_top_fieldlist(p):
    """topcmd : TOP fieldlist"""
    p[0] = ParseTreeNode('TOP')
    p[0].add_children(p[2].children)

def p_top_fieldlist_by(p):
    """topcmd : TOP fieldlist by fieldlist"""
    by_node = ParseTreeNode('BY')
    by_node.add_children(p[4].children)
    p[0] = ParseTreeNode('TOP')
    p[0].add_children(p[2].children)
    p[0].add_child(by_node)

def p_top_topopt_fieldlist(p):
    """topcmd : TOP topoptlist fieldlist"""
    p[0] = ParseTreeNode('TOP')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_top_topopt_fieldlist_by(p):
    """topcmd : TOP topoptlist fieldlist by fieldlist"""
    by_node = ParseTreeNode('BY')
    by_node.add_children(p[5].children)
    p[0] = ParseTreeNode('TOP')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)
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
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_topopt_commonopt(p):
    """topopt : COMMON_OPT EQ value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])
