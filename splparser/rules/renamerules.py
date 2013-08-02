#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.simplevaluerules import *
from splparser.rules.common.statsfnrules import *
from splparser.rules.common.uminusrules import *
    
from splparser.lexers.renamelexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_rename(p):
    """cmdexpr : renamecmd"""
    p[0] = p[1]

def p_rename_renameexprlist(p):
    """renamecmd : RENAME renameexprlist"""
    p[0] = ParseTreeNode('COMMAND', raw='rename')
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

def p_renameexprlist_renameexprlist_nocomma(p):
    """renameexprlist : renameexpr renameexprlist"""
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_renameexpr_simplefield(p):
    """renameexpr : simplefield as simplevalue"""
    as_node = ParseTreeNode('FUNCTION', raw='rename')
    as_node.add_children([p[1], p[3]])
    p[3].role = 'FIELD'
    p[0] = as_node

def p_renameexpr_statsfnexpr(p):
    """renameexpr : statsfnexpr as simplevalue"""
    as_node = ParseTreeNode('FUNCTION', raw='rename')
    as_node.add_children(p[1].children)
    as_node.add_child(p[3])
    p[3].role = 'FIELD'
    p[0] = as_node
    p[3].values.append(p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in rename parser input!") 

