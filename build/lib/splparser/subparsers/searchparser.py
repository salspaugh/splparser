#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_search(p): # search-like
    """cmdexpr : searchcmd"""
    p[0] = p[1]

def p_search_search(p):
    """searchcmd : SEARCH searchexpr"""
    p[0] = ParseTreeNode('SEARCH')
    p[0].add_child(p[2])

def p_searchexpr_parentheses(p):
    """searchexpr : LPAREN searchexpr RPAREN"""
    p[0] = p[2]
    
#def p_searchexpr_macro(p):
#    """searchexpr : MACRO"""
#    p[0] = ('MACRO', p[1])

#def p_searchexpr_subsearch(p):
#    """searchexpr : subsearch"""
#    p[0] = ('SUBSEARCH', p[1])

def p_searchexpr_space(p):
    """searchexpr : searchexpr searchexpr"""
    p[0] = ParseTreeNode('AND', associative=True)
    p[0].add_children([p[1], p[2]])

def p_searchexpr_comma(p):
    """searchexpr : searchexpr COMMA searchexpr"""
    p[0] = ParseTreeNode('AND', associative=True)
    p[0].add_children([p[1], p[3]])

def p_searchexpr_and(p):
    """searchexpr : searchexpr AND searchexpr"""
    p[0] = ParseTreeNode('AND', associative=True)
    p[0].add_children([p[1], p[3]])
    
def p_searchexpr_or(p):
    """searchexpr : searchexpr OR searchexpr"""
    p[0] = ParseTreeNode('OR', associative=True)
    p[0].add_children([p[1], p[3]])

def p_searchexpr_not(p):
    """searchexpr : NOT searchexpr"""
    p[0] = ParseTreeNode('NOT')
    p[0].add_child(p[2])

def p_searchexpr_value(p):
    """searchexpr : value"""
    p[0] = p[1]

# TODO: Ask Carrasso about this rule, I don't really understand it.
def p_searchexpr_tag(p):
    """searchexpr : TAG EQ SEARCH_KEY DCOLON value"""
    p[0] = ParseTreeNode('TAG')
    p[0].add_children([p[3], p[5]])

# NOTE: '==' is not a valid comparator -- will parse out to SEARCH_KEY EQ =val, where
#       the second '=' is included as a part of the value.

def p_searchexpr_eq(p):
    """searchexpr : key EQ value
                  | key DCOLON value"""
    p[0] = ParseTreeNode('EQ')
    p[0].add_children([p[1], p[3]])

# TODO: eliminate numerical comparison rules with the following rule
#def p_searchexpr_comparison(p):
#    """searchexpr : key COMPARISON value"""
#    p[0] = ParseTreeNode(p[2].upper())
#    p[0].add_children([p[1], p[3]])

def p_searchexpr_ne(p):
    """searchexpr : key NE value"""
    p[0] = ParseTreeNode('NE')
    p[0].add_children([p[1], p[3]])

def p_searchexpr_lt(p):
    """searchexpr : key LT value"""
    p[0] = ParseTreeNode('LT')
    p[0].add_children([p[1], p[3]])

def p_searchexpr_le(p):
    """searchexpr : key LE value"""
    p[0] = ParseTreeNode('LE')
    p[0].add_children([p[1], p[3]])

def p_searchexpr_ge(p):
    """searchexpr : key GE value"""
    p[0] = ParseTreeNode('GE')
    p[0].add_children([p[1], p[3]])

def p_searchexpr_gt(p):
    """searchexpr : key GT value"""
    p[0] = ParseTreeNode('GT')
    p[0].add_children([p[1], p[3]])    

def p_key_field(p):
    """key : field"""
    p[0] = p[1]

def p_key(p):
    """key : SEARCH_KEY""" 
    p[0] = ParseTreeNode(p[1].upper()) 
