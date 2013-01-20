#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_head(p):
    """cmdexpr : headcmd"""
    p[0] = p[1]

def p_headcmd_head(p):
    """headcmd : HEAD"""
    p[0] = ParseTreeNode('HEAD')

def p_headcmd_head_int(p):
    """headcmd : HEAD int"""
    p[0] = ParseTreeNode('HEAD')
    p[0].add_child(p[2])

#def p_headcmd_head_eval(p):
#    """headcmd : HEAD evalfnexpr"""
#    p[0] = ParseTreeNode('HEAD')
#    p[0].add_child(p[2])
#
#def p_headcmd_head_headopt(p):
#    """headcmd : HEAD headoptlist"""
#    p[0] = ParseTreeNode('HEAD') 
#    p[0].add_children(p[2].children)
#
#def p_headcmd_head_int_headopt(p):
#    """headcmd : HEAD int headoptlist"""
#    p[0] = ParseTreeNode('HEAD')
#    p[0].add_child(p[2])
#    p[0].add_children(p[3].children)
#
#def p_headcmd_head_eval_headopt(p):
#    """headcmd : HEAD evalfnexpr headoptlist"""
#    p[0] = ParseTreeNode('HEAD')
#    p[0].add_child(p[2])
#    p[0].add_children(p[3].children)
#
#def p_headoptlist(p):
#    """headoptlist : headopt"""
#    p[0] = ParseTreeNode('_HEAD_OPT_LIST')
#    p[0].add_child(p[1])
#
#def p_headoptlist_headopt(p):
#    """headoptlist : headopt headoptlist"""
#    p[0] = ParseTreeNode('_HEAD_OPT_LIST')
#    p[0].add_child(p[1])
#    p[0].add_children(p[2].children) 
#
#def p_headopt(p):
#    """headopt : HEAD_OPT EQ value"""
#    p[0] = ParseTreeNode(p[1].upper())
#    p[0].add_child(p[3])
#
#def p_headopt_commonopt(p):
#    """headopt : COMMON_OPT EQ value"""
#    p[0] = ParseTreeNode(p[1].upper())
#    p[0].add_child(p[3])
