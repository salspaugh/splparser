
from splparser.parsetree import *

from splparser.rules.common.simplevaluerules import *

FIELD_TYPES = ['WORD', 'ID']
NUMBER_TYPES = ['INT', 'FLOAT', 'BIN', 'OCT', 'HEX', 'FUNCTION']
CANONICAL_FUNCTIONS = {"ceil": "ceiling"}

NUMERIC_DOMAIN = ["abs", "case", "ceil", "ceiling",  "exact", "exp", "floor", "len", "ln", "log", "mvrange", "pi", "pow", "random", "round", "sigfig", "sqrt", "tonumber", "validate", "modulus", "divides", "times", "plus", "minus", "lt", "le", "ge", "gt"]
STRING_DOMAIN = ["case", "commands", "len", "like", "lower", "ltrim", "match", "replace", "rtrim", "searchmatch", "spath", "split", "substr", "tostring", "trim", "upper", "concat"]
IPADDR_DOMAIN = ["cidrmatch"]
TIME_DOMAIN = ["now", "relative_time", "strftime", "strptime"]
MV_DOMAIN = ["mvindex", "mvfilter", "mvfind", "mvjoin", "mvzip"]
URL_DOMAIN = ["urldecode"]
BOOLEAN_DOMAIN = ["and", "or", "not", "xor"]

NUMERIC_RANGE = ["abs", "ceil", "ceiling", "exact", "exp", "floor", "len", "ln", "log", "mvcount", "mvfind", "pi", "pow", "random", "round", "sigfig", "sqrt", "tonumber", "validate", "modulus", "divides", "times", "plus", "minus", "lt", "le", "ge", "gt"]
STRING_RANGE = ["commands", "exact", "lower", "ltrim", "md5", "mvjoin", "replace", "rtrim", "spath", "split", "substr", "tostring", "typeof", "trim", "upper", "validate"]
TIME_RANGE = ["now", "relative_time", "strftime", "strptime", "time"]
MV_RANGE = ["mvappend", "mvindex", "mvfilter", "mvrange", "mvzip"]
URL_RANGE = ["urldecode"]
BOOLEAN_RANGE = ["cidrmatch", "exact", "isbool", "isint", "isnotnull", "isnull", "isnum", "isstr", "like", "searchmatch", "and", "or", "not", "xor"]

CONDITIONAL_FUNCTIONS = ["case", "if", "ifnull"]

def set_range_datatypes(field, fn):
    if field.role.find('FIELD') == -1:
        return
    if fn.raw not in CONDITIONAL_FUNCTIONS: 
        field.datatype = function_range_type(fn)
    else:
        pass
        #TODO: something smarter on case and if functions

def function_range_type(fn):
    if fn.raw.lower() in NUMERIC_RANGE:
        return 'NUMERIC'
    if fn.raw.lower() in URL_RANGE:
        return 'URL'
    if fn.raw.lower() in STRING_RANGE:
        return 'STRING'
    if fn.raw.lower() in TIME_RANGE:
        return 'TIME'
    if fn.raw.lower() in MV_RANGE:
        return 'MV'
    if fn.raw.lower() in BOOLEAN_RANGE:
        return 'BOOLEAN'

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
    if fn.raw.lower() in NUMERIC_DOMAIN:
        return 'NUMERIC'
    if fn.raw.lower() in URL_RANGE:
        return 'URL'
    if fn.raw.lower() in IPADDR_DOMAIN:
        return 'IPADDR'
    if fn.raw.lower() in STRING_DOMAIN:
        return 'STRING'
    if fn.raw.lower() in TIME_DOMAIN:
        return 'TIME'
    if fn.raw.lower() in MV_DOMAIN:
        return 'MV'
    if fn.raw.lower() in BOOLEAN_DOMAIN:
        return 'BOOLEAN'

def canonicalize(function):
    if not type(function) == type("string"):
        return function
    f = CANONICAL_FUNCTIONS.get(function, function)
    return f

def check_role(node):
    if node.nodetype in FIELD_TYPES and not node.role.find('FIELD') > -1:
        node.role = 'FIELD'

def match_role(tree, raw, role):
    stack = []
    stack.insert(0, tree)
    while len(stack) > 0:
        node = stack.pop(0)
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
    p[1] = canonicalize(p[1])
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])

def p_evalfnexpr_evalfn(p):
    """evalfnexpr : EVAL_FN LPAREN oplist RPAREN 
                  | COMMON_FN LPAREN oplist RPAREN"""
    p[1] = canonicalize(p[1])
    p[0] = ParseTreeNode('FUNCTION', raw=p[1])
    set_domain_datatypes(p[0], p[3])
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
    set_domain_datatypes(p[0], p[0].children)

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
    set_domain_datatypes(p[0], p[0].children)

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
    set_domain_datatypes(p[0], p[0].children)

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
    set_domain_datatypes(p[0], p[0].children)

# TODO: Figure out how to include these in the schema extraction.
def p_opexpr_comparator(p):
    """opexpr : opexpr comparator opexpr %prec EQ"""
    if p[2] != 'EQ':
        p[0] = ParseTreeNode('FUNCTION', raw=p[2].raw)
    check_role(p[1])
    check_role(p[3])
    if p[1].nodetype != 'SPL':
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
    set_domain_datatypes(p[0], p[0].children)
    if p[2].role == 'EQ' and p[1].role == 'FIELD':
        set_range_datatypes(p[1], p[3])

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
    set_domain_datatypes(p[0], p[0].children)

def p_opexpr_plus(p):
    """opexpr : opexpr PLUS opexpr"""
    check_role(p[1])
    check_role(p[3])
    p[0] = ParseTreeNode('FUNCTION', raw='plus', is_associative=True)
    if not (p[1].nodetype in NUMBER_TYPES or p[1].role == 'FIELD' or p[1].role == '_STATSFNEXPR') or \
        not (p[3].nodetype in NUMBER_TYPES or p[3].role == 'FIELD' or p[3].role == '_STATSFNEXPR'):
        p[0] = ParseTreeNode('FUNCTION', raw='concat', is_associative=True)
    if p[1].role[0] == '_':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    if p[3].role[0] == '_':
        p[0].add_children(p[3].children)
    else:
        p[0].add_child(p[3])
    set_domain_datatypes(p[0], p[0].children)

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
    set_domain_datatypes(p[0], p[0].children)

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
    set_domain_datatypes(p[0], p[0].children)

def p_boolean_op_and(p):
    """boolean_op : AND"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1], is_associative=True)

def p_boolean_op_or(p):
    """boolean_op : OR"""
    p[0] = ParseTreeNode('FUNCTION', raw=p[1], is_associative=True)

