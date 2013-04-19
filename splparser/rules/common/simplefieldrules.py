
from splparser.parsetree import *

def p_simplefield_word(p):
    """simplefield : WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1], arg=True, field=True)

def p_simplefield_id(p):
    """simplefield : ID"""
    p[0] = ParseTreeNode('ID', raw=p[1], arg=True, field=True)

def p_simplefield_literal(p):
    """simplefield : LITERAL"""
    p[0] = ParseTreeNode('LITERAL', raw=p[1], arg=True, field=True)

def p_simplefield_nbstr(p):
    """simplefield : NBSTR"""
    p[0] = ParseTreeNode('NBSTR', raw=p[1], arg=True, field=True)

def p_simplefield_eval_fn(p):
    """simplefield : EVAL_FN"""
    p[0] = ParseTreeNode('WORD', raw=p[1], arg=True, field=True)

def p_simplefield_num(p):
    """simplefield : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('BIN', raw=p[1], arg=True, field=True)

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('OCT', raw=p[1], arg=True, field=True)

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('HEX', raw=p[1], arg=True, field=True)

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1], arg=True, field=True)

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FLOAT', raw=p[1], arg=True, field=True)
