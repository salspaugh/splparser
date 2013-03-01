
from splparser.parsetree import *

from splparser.rules.common.simplefieldrules import *

# WARNING: The order of the next two rules is important.
def p_simplefieldlist_simplefield(p):
    """simplefieldlist : simplefield"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])

def p_simplefieldlist_comma(p):
    """simplefieldlist : simplefield COMMA simplefieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_simplefieldlist_space(p):
    """simplefieldlist : simplefield simplefieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

