
from splparser.parsetree import *

def p_statsfnexpr_field(p):
    """statsfnexpr : STATS_FN field
                   | COMMON_FN field
                   | EVAL field"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[2])
    p[0].add_child(fn_node)

def p_statsfnexpr_parenfield(p):
    """statsfnexpr : STATS_FN LPAREN field RPAREN
                   | COMMON_FN LPAREN field RPAREN
                   | EVAL LPAREN field RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[3])
    p[0].add_child(fn_node)

def p_statsfnexpr_keqv(p):
    """statsfnexpr : STATS_FN LPAREN key EQ value RPAREN
                   | COMMON_FN LPAREN key EQ value RPAREN
                   | EVAL LPAREN key EQ value RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    eq_node = ParseTreeNode('EQ')
    eq_node.add_children([p[3], p[5]])
    fn_node.add_child(eq_node)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr_paren(p):
    """statsfnexpr : STATS_FN LPAREN statsfnexpr RPAREN
                   | COMMON_FN LPAREN statsfnexpr RPAREN
                   | EVAL LPAREN statsfnexpr RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[3].children)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr(p):
    """statsfnexpr : STATS_FN statsfnexpr
                   | COMMON_FN statsfnexpr
                   | EVAL statsfnexpr"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[2].children)
    p[0].add_child(fn_node)

#def p_statsfnexpr_evalfnexpr(p):
#    """statsfnexpr : evalfnexpr"""
#    p[0] = p[1]

def p_statsfnexpr_sparkline(p):
    """statsfnexpr : SPARKLINE statsfnexpr"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp_node = ParseTreeNode('SPARKLINE')
    sp_node.add_children(p[2].children)
    p[0].add_child(sp_node)

# NOTE: The documentation is ambiguous / wrong about the grammar of this command.
def p_statsfnexpr_sparkline_paren(p):
    """statsfnexpr : SPARKLINE LPAREN statsfnexpr COMMA field RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    sp_node = ParseTreeNode('SPARKLINE')
    sp_node.add_children(p[3].children)
    sp_node.add_child(p[5])
    p[0].add_child(sp_node)

# TODO: EVAL_FN can probably be field names too.
def p_field_stats_fn(p):
    """field : STATS_FN
             | COMMON_FN""" # HACK
    p[0] = ParseTreeNode('WORD', raw=p[1])

