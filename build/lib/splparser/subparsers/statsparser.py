#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

# TODO: Add support for sparklines.

# NOTE: The strange structure of these rules is because we need to always
#       associate STATS_FN with another token on the RHS of rules because
#       otherwise we get a reduce/reduce conflict from the rule
#           field : STATS_FN
#       since nothing prevents fields from having the same name as command
#       functions.

def p_cmdexpr_stats(p):
    """cmdexpr : statscmd"""
    p[0] = p[1]

def p_statscmd(p):
    """statscmd : statscmdstart"""
    p[0] = p[1]

def p_statscmd_cont(p):
    """statscmd : statscmdstart statscmdcont"""
    p[0] = p[1]
    p[0].add_children(p[2].children)

def p_statscmdstart(p):
    """statscmdstart : STATS STATS_FN
                     | STATS EVAL
                     | STATS statsoptlist STATS_FN
                     | STATS statsoptlist EVAL"""
    p[0] = ParseTreeNode('STATS')
    fn_idx = 2
    if len(p) > 3:
        fn_idx = 3
        p[0].add_children(p[2].children)
    fn_node = ParseTreeNode(p[fn_idx].upper())
    p[0].add_child(fn_node)

def p_statsoptlist(p):
    """statsoptlist : statsopt"""
    p[0] = ParseTreeNode('_STATS_OPT_LIST')
    p[0].add_child(p[1])

def p_statsoptlist_statsopt(p):
    """statsoptlist : statsopt statsoptlist"""
    p[0] = ParseTreeNode('_STATS_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_statsopt_field(p):
    """statsopt : STATS_OPT EQ field"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_statsopt_delimiter(p):
    """statsopt : STATS_OPT EQ delimiter"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_statscmdstart_asbylist(p):
    """statscmdstart : STATS STATS_FN asbylist
                     | STATS EVAL asbylist
                     | STATS statsoptlist STATS_FN asbylist
                     | STATS statsoptlist EVAL asbylist"""
    p[0] = ParseTreeNode('STATS')
    fn_idx = 2
    if len(p) > 4:
        fn_idx = 3
        p[0].add_children(p[2].children)
    asby_idx = fn_idx + 1
    fn_node = ParseTreeNode(p[fn_idx].upper())
    fn_node.add_children(p[asby_idx].children)
    p[0].add_child(fn_node)

def p_statscmdstart_statsfnexpr(p):
    """statscmdstart : STATS statsfnexpr
                     | STATS statsoptlist statsfnexpr"""
    p[0] = ParseTreeNode('STATS')
    fn_idx = 2
    if len(p) > 3:
        fn_idx = 3
        p[0].add_children(p[2].children)
    p[0].add_children(p[fn_idx].children)

def p_statscmdstart_statsfnexpr_asbylist(p):
    """statscmdstart : STATS statsfnexpr asbylist
                     | STATS statsoptlist statsfnexpr asbylist"""
    p[0] = ParseTreeNode('STATS')
    fn_idx = 2
    if len(p) > 4:
        fn_idx = 3
        p[0].add_children(p[2].children)
    asby_idx = fn_idx + 1
    p[fn_idx].children[0].add_children(p[asby_idx].children)
    p[0].add_children(p[fn_idx].children)
    #p[0].children[0].add_children(p[asby_idx].children)

def p_statsfnexpr_field(p):
    """statsfnexpr : STATS_FN field
                   | EVAL field"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[2])
    p[0].add_child(fn_node)

def p_statsfnexpr_parenfield(p):
    """statsfnexpr : STATS_FN LPAREN field RPAREN
                   | EVAL LPAREN field RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[3])
    p[0].add_child(fn_node)

def p_statsfnexpr_keqv(p):
    """statsfnexpr : STATS_FN LPAREN key EQ value RPAREN
                   | EVAL LPAREN key EQ value RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    eq_node = ParseTreeNode('EQ')
    eq_node.add_children([p[3], p[5]])
    fn_node.add_child(eq_node)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr(p):
    """statsfnexpr : STATS_FN LPAREN statsfnexpr RPAREN
                   | EVAL LPAREN statsfnexpr RPAREN"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[3].children)
    p[0].add_child(fn_node)

def p_statsfnexpr_statsfnexpr(p):
    """statsfnexpr : STATS_FN statsfnexpr
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

def p_statscmdcont_statscmdcont(p):
    """statscmdcont : statscmdcont statscmdcont"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[1].children)
    p[0].add_children(p[2].children)

def p_statscmdcont(p):
    """statscmdcont : COMMA STATS_FN
                    | COMMA EVAL"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    fn_node = ParseTreeNode(p[2].upper())
    p[0].add_child(fn_node)

def p_statscmdcont_asbylist(p):
    """statscmdcont : COMMA STATS_FN asbylist
                    | COMMA EVAL asbylist"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    fn_node = ParseTreeNode(p[2].upper())
    p[0].add_child(fn_node)
    p[0].children[0].add_children(p[3].children)

def p_statscmdcont_statsfnexpr(p):
    """statscmdcont : COMMA statsfnexpr"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[2].children)

def p_statscmdcont_statsfnexpr_asbylist(p):
    """statscmdcont : COMMA statsfnexpr asbylist"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[2].children)
    p[0].children[0].add_children(p[3].children)

def p_asbylist_as(p):
    """asbylist : as field"""
    p[0] = ParseTreeNode('_ASBYLIST')
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[2])

def p_asbylist_by(p):
    """asbylist : by fieldlist"""
    p[0] = ParseTreeNode('_ASBYLIST')
    by_node = ParseTreeNode('BY')
    p[0].add_child(by_node)
    by_node.add_children(p[2].children)

def p_asbylist(p):
    """asbylist : as field by fieldlist"""
    p[0] = ParseTreeNode('_ASBYLIST')
    as_node = ParseTreeNode('AS')
    by_node = ParseTreeNode('BY')
    p[0].add_child(as_node)
    as_node.add_child(p[2])
    p[0].add_child(by_node)
    by_node.add_children(p[4].children)
    
