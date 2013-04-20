#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.byrules import *
from splparser.rules.common.chartrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.statsfnrules import *

from splparser.lexers.chartlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_chart(p):
    """cmdexpr : chartcmd"""
    p[0] = p[1]

def p_chartcmd(p):
    """chartcmd : CHART carglist
                | SICHART carglist"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[2].children)

def p_carg_statsfnexpr_over(p):
    """carg : statsfnexpr OVER simplefield"""
    p[0] = p[1].children[0]
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[3])
    p[0].add_child(over_node)

def p_carg_statsfn_over(p):
    """carg : STATS_FN OVER simplefield"""
    p[0] = ParseTreeNode(p[1].upper())
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[3])
    p[0].add_child(over_node)

def p_carg_statsfnexpr_over_by(p):
    """carg : statsfnexpr OVER simplefield splitbyclause"""
    p[0] = p[1].children[0]
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[3])
    p[0].add_child(over_node)
    p[0].add_children(p[4].children)

def p_carg_statsfn_over_by(p):
    """carg : STATS_FN OVER simplefield splitbyclause"""
    p[0] = ParseTreeNode(p[1].upper())
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[3])
    p[0].add_child(over_node)
    p[0].add_children(p[4].children)

def p_carg_statsfnexpr_as_over(p):
    """carg : statsfnexpr as simplefield OVER simplefield"""
    p[0] = p[1].children[0]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    over_node = parsetreenode('over')
    over_node.add_child(p[5])
    p[0].add_child(over_node)
    p[1].expr = True
    p[3].values.append(p[1].children)

def p_carg_statsfn_as_over(p):
    """carg : STATS_FN as simplefield OVER simplefield"""
    p[0] = ParseTreeNode(p[1].upper())
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    over_node = parsetreenode('over')
    over_node.add_child(p[5])
    p[0].add_child(over_node)
    p[1].expr = True
    p[3].values.append(p[1])

def p_carg_statsfnexpr_as_by(p):
    """carg : statsfnexpr as simplefield splitbyclause"""
    p[0] = p[1].children[0]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    p[0].add_children(p[4].children)
    p[1].expr = True
    p[3].values.append(p[1].children)

def p_carg_statsfn_as_by(p):
    """carg : STATS_FN as simplefield splitbyclause"""
    p[0] = ParseTreeNode(p[1].upper())
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    p[0].add_children(p[4].children)
    p[1].expr = True
    p[3].values.append(p[1])

def p_carg_statsfnexpr_as_over_by(p):
    """carg : statsfnexpr as simplefield OVER simplefield splitbyclause"""
    p[0] = p[1].children[0]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[5])
    p[0].add_child(over_node)
    p[0].add_children(p[6].children)
    p[1].expr = True
    p[3].values.append(p[1].children)

def p_carg_statsfn_as_over_by(p):
    """carg : STATS_FN as simplefield OVER simplefield splitbyclause"""
    p[0] = ParseTreeNode(p[1].upper())
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])
    over_node = ParseTreeNode('OVER')
    over_node.add_child(p[5])
    p[0].add_child(over_node)
    p[0].add_children(p[6].children)
    p[1].expr = True
    p[3].values.append(p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in chart parser input!") 
