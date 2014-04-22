
import re

from splparser.parsetree import *

from splparser.rules.common.evalfnexprrules import *
from splparser.rules.common.simplevaluerules import *

CANONICAL_FUNCTIONS ={
    "c": "count",
    "dc": "distinct_count",
    "avg": "mean"
    }

ANY_DOMAIN = ["c", "count", "dc", "distinct_count", "earliest", "estdc", "estdc_error", "first", "last", "latest", "list", "max", "min", "median", "mode", "per_day", "per_hour", "per_minute", "per_second", "values"]

ANY_RANGE = ["earliest", "first", "last", "latest", "list", "max", "median", "min", "mode", "values"]

def set_range_datatypes(field, fn):
    if field.role.find('FIELD') == -1:
        return
    if fn.raw not in CONDITIONAL_FUNCTIONS: 
        field.datatype = function_range_type(fn)

def function_range_type(fn):
    if fn.raw.lower() not in ANY_RANGE:
        return 'NUMERIC'

def set_domain_datatypes(fn, args):
    stack = []
    if type(args) == type([]):
        for a in args:
            stack.insert(0, a)
    else:
        stack = [args]
    while len(stack) > 0:
        node = stack.pop(0)
        if node.role == 'FUNCTION':
            continue
        if node.role.find('FIELD') > -1:
            node.datatype = function_domain_type(fn)
        stack = node.children + stack

def function_domain_type(fn):
    if fn.raw.lower() not in ANY_DOMAIN:
        return 'NUMERIC'

def canonicalize(function):
    if not type(function) == type("string"):
        return function
    f = CANONICAL_FUNCTIONS.get(function, function)
    if re.match('p[\d]+', f):
        f = 'perc' + f[1:]
    return f

def convert_eq(node):
    stack = []
    stack.insert(0, node)
    while len(stack) > 0:
        curr = stack.pop()
        if curr.role == 'EQ':
            curr.role = 'FUNCTION'
            curr.raw = 'eq'
        for c in curr.children:
            stack.insert(0, c)

def p_statsfnexpr_simplefield(p):
    """statsfnexpr : STATS_FN simplefield
                   | COMMON_FN simplefield"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    fn.add_child(p[2])
    p[0].add_child(fn)
    set_domain_datatypes(fn, p[2])

def p_statsfnexpr_parensimplefield(p):
    """statsfnexpr : STATS_FN LPAREN simplefield RPAREN
                   | COMMON_FN LPAREN simplefield RPAREN"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    fn.add_child(p[3])
    p[0].add_child(fn)
    set_domain_datatypes(fn, p[3])

def p_statsfnexpr_empty(p):
    """statsfnexpr : STATS_FN LPAREN RPAREN"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(fn)

def p_statsfnexpr_keqv(p):
    """statsfnexpr : STATS_FN LPAREN simplefield EQ simplevalue RPAREN
                   | COMMON_FN LPAREN simplefield EQ simplevalue RPAREN"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    eq = ParseTreeNode('FUNCTION', raw='eq')
    eq.add_children([p[3], p[5]])
    p[3].values.append(p[5])
    fn.add_child(eq)
    p[0].add_child(fn)
    set_domain_datatypes(fn, p[3])

def p_statsfnexpr_statsfnexpr_paren(p):
    """statsfnexpr : STATS_FN LPAREN statsfnexpr RPAREN
                   | COMMON_FN LPAREN statsfnexpr RPAREN"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    fn.add_children(p[3].children)
    p[0].add_child(fn)
    set_domain_datatypes(fn, p[3])

def p_statsfnexpr_statsfnexpr(p):
    """statsfnexpr : STATS_FN statsfnexpr
                   | COMMON_FN statsfnexpr"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    fn.add_children(p[2].children)
    p[0].add_child(fn)
    set_domain_datatypes(fn, p[2])

def p_statsfnexpr_sparkline(p):
    """statsfnexpr : SPARKLINE"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp = ParseTreeNode('FUNCTION', raw='sparkline')
    p[0].add_child(sp)

# NOTE: The documentation is ambiguous / wrong about the grammar of this command.
def p_statsfnexpr_sparkline_paren(p):
    """statsfnexpr : SPARKLINE LPAREN statsfnexpr COMMA simplefield RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp = ParseTreeNode('FUNCTION', raw='sparkline')
    sp.add_children(p[3].children)
    sp.add_child(p[5])
    p[0].add_child(sp)

# TODO: EVAL_FN can probably be simplefield names too.
def p_simplefield_stats_fn(p):
    """simplefield : STATS_FN
                   | COMMON_FN""" # HACK
    p[0] = ParseTreeNode('FIELD', nodetype='WORD', raw=p[1], is_argument=True)

#def p_statsfnexpr_eval_parens(p):
#    """statsfnexpr : EVAL LPAREN oplist RPAREN"""
#    p[0] = ParseTreeNode('_STATSFNEXPR')
#    eval = ParseTreeNode('EVAL')
#    eval.add_children(p[3].children)
#    p[0].add_child(eval)

def p_statsfnexpr_eval(p):
    """statsfnexpr : EVAL LPAREN oplist RPAREN"""
    convert_eq(p[3]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    eval = ParseTreeNode('FUNCTION', raw='eval')
    eval.add_children(p[3].children)
    p[0].add_child(eval)

def p_opexpr_statsfnexpr(p):
    """opexpr : statsfnexpr"""
    p[0] = p[1]
