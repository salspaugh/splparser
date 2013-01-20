#!/usr/bin/env python

import ply.yacc

from splparser.parsetree import *

# TODO: Add support for sparklines.

# NOTE: The strange structure of these rules is because we need to always
#       associate CHART_FN with another token on the RHS of rules because
#       otherwise we get a reduce/reduce conflict from the rule
#           field : CHART_FN
#       since nothing prevents fields from having the same name as command
#       functions.

def p_cmdexpr_chart(p):
    """cmdexpr : chartcmd"""
    p[0] = p[1]

def p_chartcmd(p):
    """chartcmd : chartcmdstart"""
    p[0] = p[1]

def p_chartcmd_cont(p):
    """chartcmd : chartcmdstart chartcmdcont"""
    p[0] = p[1]
    p[0].add_children(p[2].children)

def p_chartcmdstart(p):
    """chartcmdstart : chartplus CHART_FN
                     | chartplus EVAL"""
    p[0] = p[1]
    fn_node = ParseTreeNode(p[2].upper())
    p[0].add_child(fn_node)

def p_chartplus(p):
    """chartplus : CHART"""
    p[0] = ParseTreeNode('CHART')

def p_chartplus_chartopts(p):
    """chartplus : CHART chartoptlist"""
    p[0] = ParseTreeNode('CHART')
    p[0].add_children(p[2].children)

def p_chartoptlist(p):
    """chartoptlist : chartopt"""
    p[0] = ParseTreeNode('_CHART_OPT_LIST')
    p[0].add_child(p[1])

def p_chartoptlist_chartopt(p):
    """chartoptlist : chartopt chartoptlist"""
    p[0] = ParseTreeNode('_CHART_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_chartopt_field(p):
    """chartopt : CHART_OPT EQ field"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_chartopt_delimiter(p):
    """chartopt : CHART_OPT EQ delimiter"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_child(p[3])

def p_chartcmdstart_asbylist(p):
    """chartcmdstart : chartplus CHART_FN asbylist
                     | chartplus EVAL asbylist"""
    p[0] = p[1]
    fn_node = ParseTreeNode(p[2].upper())
    fn_node.add_children(p[3].children)
    p[0].add_child(fn_node)

def p_chartcmdstart_chartfnexpr(p):
    """chartcmdstart : chartplus chartfnexpr"""
    p[0] = p[1]
    p[0].add_children(p[2].children)

def p_chartcmdstart_chartfnexpr_asbylist(p):
    """chartcmdstart : chartplus chartfnexpr asbylist"""
    p[0] = p[1]
    p[0].add_children(p[2].children)
    p[0].children[0].add_children(p[3].children)

def p_chartfnexpr_field(p):
    """chartfnexpr : CHART_FN field
                   | EVAL field"""
    p[0] = ParseTreeNode('_CHARTFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[2])
    p[0].add_child(fn_node)

def p_chartfnexpr_parenfield(p):
    """chartfnexpr : CHART_FN LPAREN field RPAREN
                   | EVAL LPAREN field RPAREN"""
    p[0] = ParseTreeNode('_CHARTFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_child(p[3])
    p[0].add_child(fn_node)

def p_chartfnexpr_keqv(p):
    """chartfnexpr : CHART_FN LPAREN key EQ value RPAREN
                   | EVAL LPAREN key EQ value RPAREN"""
    p[0] = ParseTreeNode('_CHARTFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    eq_node = ParseTreeNode('EQ')
    eq_node.add_children([p[3], p[5]])
    fn_node.add_child(eq_node)
    p[0].add_child(fn_node)

def p_chartfnexpr_chartfnexpr(p):
    """chartfnexpr : CHART_FN LPAREN chartfnexpr RPAREN
                   | EVAL LPAREN chartfnexpr RPAREN"""
    p[0] = ParseTreeNode('_CHARTFNEXPR')
    fn_node = ParseTreeNode(p[1].upper())
    fn_node.add_children(p[3].children)
    p[0].add_child(fn_node)

def p_chartfnexpr_evalfnexpr(p):
    """chartfnexpr : evalfnexpr"""
    p[0] = p[1]

def p_chartcmdcont_chartcmdcont(p):
    """chartcmdcont : chartcmdcont chartcmdcont"""
    p[0] = ParseTreeNode('_CHARTCMDCONT')
    p[0].add_children(p[1].children)
    p[0].add_children(p[2].children)

def p_chartcmdcont(p):
    """chartcmdcont : COMMA CHART_FN
                    | COMMA EVAL"""
    p[0] = ParseTreeNode('_CHARTCMDCONT')
    fn_node = ParseTreeNode(p[2].upper())
    p[0].add_child(fn_node)

def p_chartcmdcont_asbylist(p):
    """chartcmdcont : COMMA CHART_FN asbylist
                    | COMMA EVAL asbylist"""
    p[0] = ParseTreeNode('_CHARTCMDCONT')
    fn_node = ParseTreeNode(p[2].upper())
    p[0].add_child(fn_node)
    p[0].children[0].add_children(p[3].children)

def p_chartcmdcont_chartfnexpr(p):
    """chartcmdcont : COMMA chartfnexpr"""
    p[0] = ParseTreeNode('_CHARTCMDCONT')
    p[0].add_children(p[2].children)

def p_chartcmdcont_chartfnexpr_asbylist(p):
    """chartcmdcont : COMMA chartfnexpr asbylist"""
    p[0] = ParseTreeNode('_CHARTCMDCONT')
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
    
