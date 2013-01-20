
from splparser.parsetree import *

# WARNING: The order of the next two rules is important.
def p_fieldlist_field(p):
    """fieldlist : field"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])

def p_fieldlist_comma(p):
    """fieldlist : field COMMA fieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_fieldlist_space(p):
    """fieldlist : field fieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

