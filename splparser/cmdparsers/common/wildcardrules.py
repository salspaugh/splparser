
from splparser.parsetree import *

def p_field_wildcard(p):
    """field : WILDCARD"""
    p[0] = ParseTreeNode('WILDCARD', raw=p[1])

