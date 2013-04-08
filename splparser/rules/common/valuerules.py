
from splparser.parsetree import *

def p_value_times(p):
    """value : field"""
    p[0] = p[1]

def p_value_ipv6addr(p):
    """value : IPV6ADDR"""
    p[0] = ParseTreeNode('IPV6ADDR', raw=p[1], arg=True)

def p_value_ipv4addr(p):
    """value : IPV4ADDR"""
    p[0] = ParseTreeNode('IPV4ADDR', raw=p[1], arg=True)

def p_value_email(p):
    """value : EMAIL"""
    p[0] = ParseTreeNode('EMAIL', raw=p[1], arg=True)

def p_value_url(p):
    """value : URL"""
    p[0] = ParseTreeNode('URL', raw=p[1], arg=True)

def p_value_path(p):
    """value : PATH"""
    p[0] = ParseTreeNode('PATH', raw=p[1], arg=True)

def p_value_us_phone(p):
    """value : US_PHONE"""
    p[0] = ParseTreeNode('US_PHONE', raw=p[1], arg=True)

