
from splparser.parsetree import *

def p_simplefield_word(p):
    """simplefield : WORD"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='WORD', raw=p[1], is_argument=True)

def p_simplefield_id(p):
    """simplefield : ID"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='ID', raw=p[1], is_argument=True)

def p_simplefield_literal(p):
    """simplefield : LITERAL"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='LITERAL', raw=p[1], is_argument=True)

def p_simplefield_nbstr(p):
    """simplefield : NBSTR"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='NBSTR', raw=p[1], is_argument=True)

def p_simplefield_eval_fn(p):
    """simplefield : EVAL_FN"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='WORD', raw=p[1], is_argument=True)

def p_simplefield_num(p):
    """simplefield : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='BIN', raw=p[1], is_argument=True)

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='OCT', raw=p[1], is_argument=True)

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='HEX', raw=p[1], is_argument=True)

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='INT', raw=p[1], is_argument=True)

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode(role='FIELD', nodetype='FLOAT', raw=p[1], is_argument=True)

def p_simplefield_default_simplefield(p):
    """simplefield : DEFAULT_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)

def p_simplefield_internal_simplefield(p):
    """simplefield : INTERNAL_FIELD"""
    p[0] = ParseTreeNode('INTERNAL_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)

def p_simplefield_default_datetime_simplefield(p):
    """simplefield : DEFAULT_DATETIME_FIELD"""
    p[0] = ParseTreeNode('DEFAULT_DATETIME_FIELD', nodetype='SPL_FIELD', raw=p[1], is_argument=True)
