
from splparser.parsetree import *

def p_field_word(p):
    """field : WORD"""
    p[0] = ParseTreeNode('FIELD', nodetype='WORD', raw=p[1], is_argument=True)

def p_field_id(p):
    """field : ID"""
    p[0] = ParseTreeNode('FIELD', nodetype='ID', raw=p[1], is_argument=True)

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('FIELD', nodetype='LITERAL', raw=p[1], is_argument=True)

def p_field_hostname(p):
    """field : HOSTNAME"""
    p[0] = ParseTreeNode('FIELD', nodetype='HOSTNAME', raw=p[1], is_argument=True)

def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('FIELD', nodetype='NBSTR', raw=p[1], is_argument=True)

def p_field_wildcard(p):
    """field : WILDCARD"""
    p[0] = ParseTreeNode('FIELD', nodetype='WILDCARD', raw=p[1], is_argument=True)

def p_field_num(p):
    """field : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('FIELD', nodetype='BIN', raw=p[1], is_argument=True)

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('FIELD', nodetype='OCT', raw=p[1], is_argument=True)

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('FIELD', nodetype='HEX', raw=p[1], is_argument=True)

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('FIELD', nodetype='INT', raw=p[1], is_argument=True)

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FIELD', nodetype='FLOAT', raw=p[1], is_argument=True)

def p_field_default_field(p):
    """field : DEFAULT_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)

def p_field_internal_field(p):
    """field : INTERNAL_FIELD"""
    p[0] = ParseTreeNode('INTERNAL_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)

def p_field_default_datetime_field(p):
    """field : DEFAULT_DATETIME_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_DATETIME_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)
