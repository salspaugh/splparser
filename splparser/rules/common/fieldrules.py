
from splparser.parsetree import *

def p_field_word(p):
    """field : WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1], arg=True, field=True)

def p_field_id(p):
    """field : ID"""
    p[0] = ParseTreeNode('ID', raw=p[1], arg=True, field=True)

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('LITERAL', raw=p[1], arg=True, field=True)

def p_field_hostname(p):
    """field : HOSTNAME"""
    p[0] = ParseTreeNode('HOSTNAME', raw=p[1], arg=True, field=True)

def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('NBSTR', raw=p[1], arg=True, field=True)

def p_field_wildcard(p):
    """field : WILDCARD"""
    p[0] = ParseTreeNode('WILDCARD', raw=p[1], arg=True, field=True)

def p_field_num(p):
    """field : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('BIN', raw=p[1], arg=True, option=True)

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('OCT', raw=p[1], arg=True, option=True)

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('HEX', raw=p[1], arg=True, option=True)

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1], arg=True, option=True)

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FLOAT', raw=p[1], arg=True, option=True)
