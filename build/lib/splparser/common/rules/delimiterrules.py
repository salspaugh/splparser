
from splparser.parsetree import *

def p_delimiter_comma(p):
    """delimiter : COMMA"""
    p[0] = ParseTreeNode('COMMA')

# TODO: Make other delimiters like tabs work.
