
from splparser.parsetree import *

from splparser.cmdparsers.common.evalfnexprrules import *
from splparser.cmdparsers.common.simplevaluerules import *

def p_statsfnexpr_simplefield(p):
    """statsfnexpr : STATS_FN simplefield
                   | COMMON_FN simplefield"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[2])
    p[0].add_child(fn_node)

def p_statsfnexpr_parensimplefield(p):
    """statsfnexpr : STATS_FN LPAREN simplefield RPAREN
                   | COMMON_FN LPAREN simplefield RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[3])
    p[0].add_child(fn_node)

def p_statsfnexpr_keqv(p):
    """statsfnexpr : STATS_FN LPAREN simplefield EQ simplevalue RPAREN
                   | COMMON_FN LPAREN simplefield EQ simplevalue RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    eq_node = ParseTreeNode('EQ')
    eq_node.add_children([p[3], p[5]])
    fn_node.add_child(eq_node)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr_paren(p):
    """statsfnexpr : STATS_FN LPAREN statsfnexpr RPAREN
                   | COMMON_FN LPAREN statsfnexpr RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[3].children)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr(p):
    """statsfnexpr : STATS_FN statsfnexpr
                   | COMMON_FN statsfnexpr"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[2].children)
    p[0].add_child(fn_node)

def p_statsfnexpr_sparkline(p):
    """statsfnexpr : SPARKLINE statsfnexpr"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp_node = ParseTreeNode('SPARKLINE')
    sp_node.add_children(p[2].children)
    p[0].add_child(sp_node)

# NOTE: The documentation is ambiguous / wrong about the grammar of this command.
def p_statsfnexpr_sparkline_paren(p):
    """statsfnexpr : SPARKLINE LPAREN statsfnexpr COMMA simplefield RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp_node = ParseTreeNode('SPARKLINE')
    sp_node.add_children(p[3].children)
    sp_node.add_child(p[5])
    p[0].add_child(sp_node)

# TODO: EVAL_FN can probably be simplefield names too.
def p_simplefield_stats_fn(p):
    """simplefield : STATS_FN
                   | COMMON_FN""" # HACK
    p[0] = ParseTreeNode('WORD', raw=p[1])

#def p_statsfnexpr_eval_parens(p):
#    """statsfnexpr : EVAL LPAREN oplist RPAREN"""
#    p[0] = ParseTreeNode('_STATSFNEXPR')
#    eval_node = ParseTreeNode('EVAL')
#    eval_node.add_children(p[3].children)
#    p[0].add_child(eval_node)

def p_statsfnexpr_eval(p):
    """statsfnexpr : EVAL oplist"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    eval_node = ParseTreeNode('EVAL')
    eval_node.add_children(p[2].children)
    p[0].add_child(eval_node)

def p_opexpr_statsfnexpr(p):
    """opexpr : statsfnexpr"""
    p[0] = p[1]
