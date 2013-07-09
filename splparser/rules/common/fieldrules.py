
from splparser.parsetree import *

def p_field_word(p):
    """field : WORD"""
    p[0] = ParseTreeNode('FIELD', type='WORD', raw=p[1], is_argument=True)

def p_field_id(p):
    """field : ID"""
    p[0] = ParseTreeNode('FIELD', type='ID', raw=p[1], is_argument=True)

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('FIELD', type='LITERAL', raw=p[1], is_argument=True)

def p_field_hostname(p):
    """field : HOSTNAME"""
    p[0] = ParseTreeNode('FIELD', type='HOSTNAME', raw=p[1], is_argument=True)

def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('FIELD', type='NBSTR', raw=p[1], is_argument=True)

def p_field_wildcard(p):
    """field : WILDCARD"""
    p[0] = ParseTreeNode('FIELD', type='WILDCARD', raw=p[1], is_argument=True)

def p_field_num(p):
    """field : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('FIELD', type='BIN', raw=p[1], is_argument=True)

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('FIELD', type='OCT', raw=p[1], is_argument=True)

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('FIELD', type='HEX', raw=p[1], is_argument=True)

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('FIELD', type='INT', raw=p[1], is_argument=True)

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FIELD', type='FLOAT', raw=p[1], is_argument=True)
