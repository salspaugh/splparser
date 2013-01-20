#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_rename(p):
    """cmdexpr : renamecmd"""
    p[0] = p[1]

#def p_cmdexpr_rename_debug(p):
#    """renamecmd : RENAME"""
#    p[0] = ParseTreeNode('RENAME')

def p_rename_renameexprlist(p):
    """renamecmd : RENAME renameexprlist"""
    p[0] = ParseTreeNode('RENAME')
    p[0].add_children(p[2].children)

# WARNING: The order of the next two rules is important.
def p_renameexprlist_renameexpr(p):
    """renameexprlist : renameexpr"""    
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])

def p_renameexprlist_renameexprlist(p):
    """renameexprlist : renameexpr COMMA renameexprlist"""
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_renameexpr_field(p):
    """renameexpr : field as value"""
    as_node = ParseTreeNode('AS')
    as_node.add_children([p[1], p[3]])
    p[0] = as_node

def p_renameexpr_statsfnexpr(p):
    """renameexpr : statsfnexpr as value"""
    as_node = ParseTreeNode('AS')
    as_node.add_children(p[1].children)
    as_node.add_child(p[3])
    p[0] = as_node
