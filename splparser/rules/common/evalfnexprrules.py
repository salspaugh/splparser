
from splparser.parsetree import *

from splparser.rules.common.simplevaluerules import *

def p_oplist_parens(p):
    """oplist : LPAREN oplist RPAREN"""
    p[0] = p[2]

def p_oplist(p):
    """oplist : opexpr"""
    p[0] = ParseTreeNode('_OPERATORLSIT')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])

def p_opexpr_evalfnexpr(p):
    """opexpr : evalfnexpr"""
    p[0] = p[1]

def p_evalfnexpr_empty(p):
    """evalfnexpr : EVAL_FN LPAREN RPAREN 
                  | COMMON_FN LPAREN RPAREN"""
    p[0] = ParseTreeNode(p[1].upper())

def p_evalfnexpr_evalfn(p):
    """evalfnexpr : EVAL_FN LPAREN oplist RPAREN 
                  | COMMON_FN LPAREN oplist RPAREN"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[3].children)

def p_opexpr_simplevalue(p):
    """opexpr : simplevalue"""
    p[0] = p[1]

def p_oplist_op(p):
    """oplist : opexpr COMMA oplist"""
    p[0] = ParseTreeNode('_OPERATORLIST')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_opexpr_binary_parens(p):
    """opexpr : LPAREN opexpr RPAREN"""
    p[0] = p[2]

def p_opexpr_not(p):
    """opexpr : NOT opexpr"""
    p[0] = ParseTreeNode('NOT')
    p[0].add_child(p[2])

def p_opexpr_minus(p):
    """opexpr : opexpr MINUS opexpr"""
    p[0] = ParseTreeNode('MINUS')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_divides(p):
    """opexpr : opexpr DIVIDES opexpr"""
    p[0] = ParseTreeNode('DIVIDES')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_modulus(p):
    """opexpr : opexpr MODULUS opexpr"""
    p[0] = ParseTreeNode('MODULUS')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_xor(p):
    """opexpr : opexpr XOR opexpr"""
    p[0] = ParseTreeNode('XOR')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_like(p):
    """opexpr : opexpr LIKE opexpr"""
    p[0] = ParseTreeNode('LIKE')
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_comparator(p):
    """opexpr : opexpr comparator opexpr %prec EQ"""
    p[0] = p[2]
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_comparator_lt(p):
    """comparator : LT"""
    p[0] = ParseTreeNode('LT')

def p_comparator_gt(p):
    """comparator : GT"""
    p[0] = ParseTreeNode('GT')

def p_comparator_le(p):
    """comparator : LE"""
    p[0] = ParseTreeNode('LE')

def p_comparator_ge(p):
    """comparator : GE"""
    p[0] = ParseTreeNode('GE')

def p_comparator_ne(p):
    """comparator : NE"""
    p[0] = ParseTreeNode('NE')

def p_comparator_eq(p):
    """comparator : EQ"""
    p[0] = ParseTreeNode('EQ')

def p_comparator_deq(p):
    """comparator : DEQ"""
    p[0] = ParseTreeNode('DEQ')

def p_opexpr_concat(p):
    """opexpr : opexpr PERIOD opexpr"""
    p[0] = ParseTreeNode('CONCAT', associative=True)
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_plus(p):
    """opexpr : opexpr PLUS opexpr"""
    p[0] = ParseTreeNode('PLUS', associative=True)
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_times(p):
    """opexpr : opexpr TIMES opexpr"""
    p[0] = ParseTreeNode('TIMES', associative=True)
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_boolean_op(p):
    """opexpr : opexpr boolean_op opexpr %prec COMMA"""
    p[0] = p[2]
    if p[1].type[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].type[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_boolean_op_and(p):
    """boolean_op : AND"""
    p[0] = ParseTreeNode('AND', associative=True)

def p_boolean_op_or(p):
    """boolean_op : OR"""
    p[0] = ParseTreeNode('OR', associative=True)

