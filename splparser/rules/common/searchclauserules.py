
from splparser.parsetree import *

def p_searchexpr_parentheses(p):
    """searchexpr : LPAREN searchexpr RPAREN"""
    p[0] = p[2]

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
