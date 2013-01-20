#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

def p_cmdexpr_eval(p):
    """cmdexpr : evalcmd"""
    p[0] = p[1]

def p_eval_evalexpr(p):
    """evalcmd : EVAL evalexpr"""
    p[0] = ParseTreeNode('EVAL')
    p[0].add_child(p[2])

def p_evalexpr(p):
    """evalexpr : field eqevalfnexpr"""
    p[0] = ParseTreeNode('EVALEXPR')
    p[0].add_child(p[1])
    p[0].add_child(p[2])

def p_eqevalfnexpr(p):
    """eqevalfnexpr : EQ evalfnexpr"""
    p[0] = p[2]

def p_evalfnexpr_evalfn(p):
    """evalfnexpr : EVAL_FN LPAREN oplist RPAREN"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[3].children)

def p_evalfnexpr_oplist(p):
    """evalexpr : oplist"""
    p[0] = ParseTreeNode('EVALEXPR')
    p[0].add_children(p[1].children)

def p_oplist_parens(p):
    """oplist : LPAREN oplist RPAREN"""
    p[0] = p[2]

def p_oplist(p):
    """oplist : opexpr"""
    p[0] = ParseTreeNode('_OPERATORLSIT')
    p[0].add_child(p[1])

def p_opexpr_evalfnexpr(p):
    """opexpr : evalfnexpr"""
    p[0] = p[1]

def p_opexpr_value(p):
    """opexpr : value"""
    p[0] = p[1]

def p_oplist_op(p):
    """oplist : opexpr COMMA oplist"""
    p[0] = ParseTreeNode('_OPERATORLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_opexpr_binary_parens(p):
    """opexpr : LPAREN opexpr RPAREN"""
    p[0] = p[2]

def p_opexpr_not(p):
    """opexpr : NOT opexpr"""
    p[0] = ParseTreeNode('NOT')
    p[0].add_child(p[2])

def p_opexpr_nonassociative_op(p):
    """opexpr : value nonassociative_op value"""
    p[0] = p[2]
    p[0].add_children([p[1], p[3]])

def p_opexpr_minus(p):
    """opexpr : value MINUS value"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children([p[1], p[3]])

#def p_nonassociative_op_minus(p):
#    """nonassociative_op : MINUS"""
#    p[0] = ParseTreeNode(p[1].upper())

def p_nonassociative_op_divides(p):
    """nonassociative_op : DIVIDES"""
    p[0] = ParseTreeNode(p[1].upper())

def p_nonassociative_op_modulus(p):
    """nonassociative_op : MODULUS"""
    p[0] = ParseTreeNode(p[1].upper())

def p_nonassociative_op_xor(p):
    """nonassociative_op : XOR"""
    p[0] = ParseTreeNode(p[1].upper())

def p_nonassociative_op_like(p):
    """nonassociative_op : LIKE"""
    p[0] = ParseTreeNode(p[1].upper())

# TODO: Maybe use this instead of the individual comparison rules or delete it.
#def p_nonassociative_op_comparison(p):
#    """nonassociative_op : COMPARISON"""
#    p[0] = ParseTreeNode(p[1].upper())

# TODO: Make these one rule for readability.
def p_nonassociative_op_lt(p):
    """nonassociative_op : LT"""
    p[0] = ParseTreeNode('LT')

def p_nonassociative_op_gt(p):
    """nonassociative_op : GT"""
    p[0] = ParseTreeNode('GT')

def p_nonassociative_op_le(p):
    """nonassociative_op : LE"""
    p[0] = ParseTreeNode('LE')

def p_nonassociative_op_ge(p):
    """nonassociative_op : GE"""
    p[0] = ParseTreeNode('GE')

def p_nonassociative_op_ne(p):
    """nonassociative_op : NE"""
    p[0] = ParseTreeNode('NE')

def p_nonassociative_op_eq(p):
    """nonassociative_op : EQ"""
    p[0] = ParseTreeNode('EQ')

def p_nonassociative_op_deq(p):
    """nonassociative_op : DEQ"""
    p[0] = ParseTreeNode('DEQ')

def p_opexpr_concat(p):
    """opexpr : opexpr PERIOD opexpr"""
    p[0] = ParseTreeNode('CONCAT', associative=True)
    p[0].add_children([p[1], p[3]])

def p_opexpr_associative_op(p):
    """opexpr : opexpr associative_op opexpr"""
    p[0] = p[2]
    p[0].add_children([p[1], p[3]])

def p_opexpr_plus(p):
    """opexpr : opexpr PLUS opexpr"""
    p[0] = ParseTreeNode('PLUS', associative=True)
    p[0].add_children([p[1], p[3]])

#def p_associative_op_plus(p):
#    """associative_op : PLUS"""
#    p[0] = ParseTreeNode('PLUS', associative=True)

def p_associative_op_times(p):
    """associative_op : TIMES"""
    p[0] = ParseTreeNode('TIMES', associative=True)

def p_associative_op_and(p):
    """associative_op : AND"""
    p[0] = ParseTreeNode('AND', associative=True)

def p_associative_op_or(p):
    """associative_op : OR"""
    p[0] = ParseTreeNode('OR', associative=True)
