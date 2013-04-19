
from splparser.parsetree import *

from splparser.rules.common.uminusrules import *

def p_simplevalue_times(p):
    """simplevalue : simplefield"""
    p[0] = p[1]
    p[0].field = False
    p[0].value = True

def p_simplevalue_ipv6addr(p):
    """simplevalue : IPV6ADDR"""
    p[0] = ParseTreeNode('IPV6ADDR', raw=p[1], arg=True, value=True)

def p_simplevalue_ipv4addr(p):
    """simplevalue : IPV4ADDR"""
    p[0] = ParseTreeNode('IPV4ADDR', raw=p[1], arg=True, value=True)
