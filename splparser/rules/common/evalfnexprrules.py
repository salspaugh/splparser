
from splparser.parsetree import *

from splparser.rules.common.simplevaluerules import *

FIELD_TYPES = ['WORD', 'ID']
NUMBER_TYPES = ['INT', 'FLOAT', 'BIN', 'OCT', 'HEX', 'FUNCTION']

def check_role(node):
    if node.type in FIELD_TYPES:
        node.role = 'FIELD'

def match_role(tree, raw, role):
    stack = []
    stack.insert(0, tree)
    while len(stack) > 0:
        node = stack.pop()
        if node.raw == raw:
            node.role = role
        if len(node.children) > 0:
            for c in node.children:
                stack.insert(0, c)

def p_oplist_parens(p):
    """oplist : LPAREN oplist RPAREN"""
    p[0] = p[2]

def p_oplist(p):
    """oplist : opexpr"""
    p[0] = ParseTreeNode('_OPERATORLIST')
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])

def p_opexpr_evalfnexpr(p):
    """opexpr : evalfnexpr"""
    p[0] = p[1]

def p_evalfnexpr_empty(p):
    """evalfnexpr : EVAL_FN LPAREN RPAREN 
                  | COMMON_FN LPAREN RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])

def p_evalfnexpr_evalfn(p):
    """evalfnexpr : EVAL_FN LPAREN oplist RPAREN 
                  | COMMON_FN LPAREN oplist RPAREN"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_children(p[3].children)

def p_opexpr_simplevalue(p):
    """opexpr : simplevalue"""
    check_role(p[1])
    p[0] = p[1]

def p_oplist_op(p):
    """oplist : opexpr COMMA oplist"""
    check_role(p[1])
    p[0] = ParseTreeNode('_OPERATORLIST')
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_opexpr_binary_parens(p):
    """opexpr : LPAREN opexpr RPAREN"""
    p[0] = p[2]

def p_opexpr_not(p):
    """opexpr : NOT opexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(p[2])

def p_opexpr_minus(p):
    """opexpr : opexpr MINUS opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='minus')
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_divides(p):
    """opexpr : opexpr DIVIDES opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='divides')
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_modulus(p):
    """opexpr : opexpr MODULUS opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='modulus')
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_xor(p):
    """opexpr : opexpr XOR opexpr"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[2])
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_like(p):
    """opexpr : opexpr LIKE opexpr"""
    p[1].role = 'FIELD'
    p[0] = ParseTreeNode('FUNCTION', raw=p[2])
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

# TODO: Figure out how to include these in the schema extraction.
def p_opexpr_comparator(p):
    """opexpr : opexpr comparator opexpr %prec EQ"""
    if p[2] != 'EQ':
        p[0] = ParseTreeNode('FUNCTION', raw=p[2])
    check_role(p[1])
    check_role(p[3])
    if p[1].type != 'SPL':
        p[1].role = 'FIELD'
        match_role(p[3], p[1].raw, 'FIELD') 
    p[0] = p[2]
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_comparator_lt(p):
    """comparator : LT"""
    p[0] = ParseTreeNode('FUNCTION', raw='lt')

def p_comparator_gt(p):
    """comparator : GT"""
    p[0] = ParseTreeNode('FUNCTION', raw='gt')

def p_comparator_le(p):
    """comparator : LE"""
    p[0] = ParseTreeNode('FUNCTION', raw='le')

def p_comparator_ge(p):
    """comparator : GE"""
    p[0] = ParseTreeNode('FUNCTION', raw='ge')

def p_comparator_ne(p):
    """comparator : NE"""
    p[0] = ParseTreeNode('FUNCTION', raw='ne')

def p_comparator_eq(p):
    """comparator : EQ"""
    p[0] = ParseTreeNode('EQ', raw='assign')

def p_comparator_deq(p):
    """comparator : DEQ"""
    p[0] = ParseTreeNode('FUNCTION', raw='deq')

def p_opexpr_concat(p):
    """opexpr : opexpr PERIOD opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='concat', is_associative=True)
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_plus(p):
    """opexpr : opexpr PLUS opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='plus', is_associative=True)
    if not (p[1].type in NUMBER_TYPES or p[1].role == 'FIELD') or \
        not (p[3].type in NUMBER_TYPES or p[3].role == 'FIELD'):
        p[0] = ParseTreeNode('FUNCTION', raw='concat', is_associative=True)
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_times(p):
    """opexpr : opexpr TIMES opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='times', is_associative=True)
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_opexpr_boolean_op(p):
    """opexpr : opexpr boolean_op opexpr %prec COMMA"""
    p[0] = p[2]
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])

def p_boolean_op_and(p):
    """boolean_op : AND"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1], is_associative=True)

def p_boolean_op_or(p):
    """boolean_op : OR"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1], is_associative=True)

