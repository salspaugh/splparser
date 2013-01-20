
from splparser.parsetree import *

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('LITERAL', raw=p[1])

#def p_field_timestamp(p):
#    """field : timestamp"""
#    p[0] = p[1]

def p_field_word(p):
    """field : wordid"""
    p[0] = p[1]

def p_field_email(p):
    """field : EMAIL"""
    p[0] = ParseTreeNode('EMAIL', raw=p[1])

# TODO: Make sure keys can actually be nbstr or if they must be IDs.
def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('NBSTR', raw=p[1])

def p_field_wildcard(p):
    """field : WILDCARD"""
    p[0] = ParseTreeNode('WILDCARD', raw=p[1])

# TODO: Think about if other key values can be field names too ...
# TODO: EVAL_FN can probably be field names too.
#def p_field_stats_fn(p):
#    """field : STATS_FN""" # HACK 
#    p[0] = ParseTreeNode('WORD', raw=p[1])

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

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1])

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FLOAT', raw=p[1])
