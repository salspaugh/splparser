#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.searchlexer import precedence, tokens

start = 'cmdexpr'

def p_search_search(p):
    """cmdexpr : SEARCH searchexpr"""
    p[0] = ParseTreeNode('COMMAND', raw='search')
    p[0].add_child(p[2])

def p_searchexpr_parentheses(p):
    """searchexpr : LPAREN searchexpr RPAREN"""
    p[0] = p[2]
    
def p_searchexpr_macro(p):
    """searchexpr : MACRO"""
    p[0] = ParseTreeNode('MACRO', raw=p[1], arg=True)

#def p_searchexpr_subsearch(p):
#    """searchexpr : subsearch"""
#    p[0] = ('SUBSEARCH', p[1])

def p_searchexpr_space(p):
    """searchexpr : searchexpr searchexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw='AND', is_associative=True)
    p[0].add_children([p[1], p[2]])

def p_searchexpr_comma(p):
    """searchexpr : searchexpr COMMA searchexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw='AND', is_associative=True)
    p[0].add_children([p[1], p[3]])

def p_searchexpr_and(p):
    """searchexpr : searchexpr AND searchexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw='AND', is_associative=True)
    p[0].add_children([p[1], p[3]])
    
def p_searchexpr_or(p):
    """searchexpr : searchexpr OR searchexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw='OR', is_associative=True)
    p[0].add_children([p[1], p[3]])

def p_searchexpr_not(p):
    """searchexpr : NOT searchexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw='NOT')
    p[0].add_child(p[2])

def p_searchexpr_value(p):
    """searchexpr : value"""
    p[1].value = True
    p[0] = p[1]

def p_searchexpr_tag(p):
    """searchexpr : TAG EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[3].role = 'TAG'
    tag_node = ParseTreeNode('KEYWORD', raw=p[1])
    p[0].add_children([tag_node, p[3]])

def p_searchexpr_tag_value(p):
    """searchexpr : TAG DCOLON field EQ value"""
    tag_node = ParseTreeNode('KEYWORD', raw=p[1])
    dcolon_node = ParseTreeNode('DCOLON')
    eq_node = ParseTreeNode('EQ', raw='assign')
    p[5].role = 'TAG'
    eq_node.add_children([p[3], p[5]])
    dcolon_node.add_children([tag_node, eq_node])

# NOTE: '==' is not a valid comparator -- will parse out to SEARCH_KEY EQ =val, where
#       the second '=' is included as a part of the value.

def p_searchexpr_eq(p):
    """searchexpr : field EQ value
                  | field DCOLON value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_ne(p):
    """searchexpr : field NE value"""
    p[0] = ParseTreeNode('FUNCTION', raw='ne')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_lt(p):
    """searchexpr : field LT value"""
    p[0] = ParseTreeNode('FUNCTION', raw='lt')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_le(p):
    """searchexpr : field LE value"""
    p[0] = ParseTreeNode('FUNCTION', raw='le')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_ge(p):
    """searchexpr : field GE value"""
    p[0] = ParseTreeNode('FUNCTION', raw='ge')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_gt(p):
    """searchexpr : field GT value"""
    p[0] = ParseTreeNode('FUNCTION', raw='gt')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])    

def p_field_default_field(p):
    """field : DEFAULT_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_FIELD', raw=p[1])

def p_field_internal_field(p):
    """field : INTERNAL_FIELD"""
    p[0] = ParseTreeNode('INTERNAL_FIELD', raw=p[1])

def p_field_default_datetime_field(p):
    """field : DEFAULT_DATETIME_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_DATETIME_FIELD', raw=p[1])

def p_field_search_opt(p):
    """field : SEARCH_OPT"""
    p[0] = ParseTreeNode('OPTION', raw=p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in search parser input!") 
