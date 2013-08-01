
from splparser.parsetree import *

from splparser.rules.common.uminusrules import *

def p_simplevalue_times(p):
    """simplevalue : simplefield"""
    p[0] = p[1]
    if p[0].type != 'SPL_FIELD':
        p[0].role = 'VALUE'

def p_simplevalue_ipv6addr(p):
    """simplevalue : IPV6ADDR"""
    p[0] = ParseTreeNode(role='VALUE', type='IPV6ADDR', raw=p[1], is_argument=True)

def p_simplevalue_ipv4addr(p):
    """simplevalue : IPV4ADDR"""
    p[0] = ParseTreeNode(role='VALUE', type='IPV4ADDR', raw=p[1], is_argument=True)
