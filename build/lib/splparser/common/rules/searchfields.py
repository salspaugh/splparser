
from splparser.parsetree import *

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('LITERAL', raw=p[1])

def p_field_email(p):
    """field : EMAIL"""
    p[0] = ParseTreeNode('EMAIL', raw=p[1])

def p_field_id(p):
    """field : ID"""
    p[0] = ParseTreeNode('ID', raw=p[1])

# TODO: Make sure keys can actually be nbstr or if they must be IDs.
def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('NBSTR', raw=p[1])

## TODO: Think about if other key values can be field names too ...
def p_field_host(p):
    """field : HOST"""
    p[0] = ParseTreeNode('HOST')

def p_value_times(p):
    """value : field"""
    p[0] = p[1]

#def p_value_email(p):
#    """value : email"""
#    p[0] = p[1]

def p_value_hostname(p):
    """value : hostname"""
    p[0] = p[1]

def p_value_ipv6addr(p):
    """value : IPV6ADDR"""
    p[0] = ParseTreeNode('IPV6ADDR', raw=p[1])

def p_value_ipv4addr(p):
    """value : IPV4ADDR"""
    p[0] = ParseTreeNode('IPV4ADDR', raw=p[1])

def p_field_num(p):
    """field : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('BIN', raw=p[1])

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('OCT', raw=p[1])

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('HEX', raw=p[1])

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1])

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FLOAT', raw=p[1])
