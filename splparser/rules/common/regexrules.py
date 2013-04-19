
from splparser.parsetree import *

def p_regex_regular_expression(p):
    """regex : REGULAR_EXPRESSION"""
    p[0] = ParseTreeNode('REGULAR_EXPRESSION', raw=p[1], arg=True)




