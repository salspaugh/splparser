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

def correct_groupby(command): # HACK
    groupby = None
    stack = []
    stack.insert(0, command)
    while len(stack) > 0:
        check = stack.pop()
        if check.raw == 'groupby':
            groupby = check
        for c in check.children:
            stack.insert(0, c)
    if not groupby: return
    groupby.parent.children.remove(groupby)
    groupby.children = filter(lambda x: x.raw != 'groupby' and x.raw != 'assign', command.children) + groupby.children 
    for c in groupby.children:
        c.parent = groupby
    command.children = filter(lambda x: x.raw == 'assign', command.children) + [groupby]

def correct_over(command): # HACK
    over = None
    stack = []
    stack.insert(0, command)
    while len(stack) > 0:
        check = stack.pop()
        if check.raw == 'over':
            over = check
        for c in check.children:
            stack.insert(0, c)
    if not over: return
    over.parent.children.remove(over)
    over.children = filter(lambda x: x.raw != 'over' and x.raw != 'assign', command.children) + over.children 
    for c in over.children:
        c.parent = over
    command.children = filter(lambda x: x.raw == 'assign', command.children) + [over]

def p_cmdexpr_chart(p):
    """cmdexpr : chartcmd"""
    p[0] = p[1]

def p_chartcmd(p):
    """chartcmd : CHART carglist
                | SICHART carglist"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2])
    correct_over(p[0])
    correct_groupby(p[0])

def p_carg_statsfnexpr_over(p):
    """carg : statsfnexpr OVER simplefield"""
    over = ParseTreeNode('FUNCTION', raw='over')
    over.add_children([p[1].children[0], p[3]])
    p[3].role = ''.join(['OVER_', p[3].role])
    p[0] = [over]

def p_carg_statsfn_over(p):
    """carg : STATS_FN OVER simplefield"""
    p[1] = canonicalize(p[1]) 
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    p[3].role = ''.join(['OVER_', p[3].role])
    over = ParseTreeNode('FUNCTION', raw='over')
    over.add_children([statsfn, p[3]])
    p[0] = [over]

def p_carg_statsfnexpr_over_by(p):
    """carg : statsfnexpr OVER simplefield splitbyclause"""
    over = ParseTreeNode('FUNCTION', raw='over')
    p[3].role = ''.join(['OVER_', p[3].role])
    over.add_children([p[1].children[0], p[3]])
    p[4][0].children.insert(0, over)
    over.parent = p[4][0]
    p[0] = p[4]

def p_carg_statsfn_over_by(p):
    """carg : STATS_FN OVER simplefield splitbyclause"""
    p[1] = canonicalize(p[1]) 
    over = ParseTreeNode('FUNCTION', raw='over')
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    p[3].role = ''.join(['OVER_', p[3].role])
    over.add_children([statsfn, p[3]])
    p[4][0].children.insert(0, over)
    over.parent = p[4][0]
    p[0] = p[4]

def p_carg_statsfnexpr_as_over(p):
    """carg : statsfnexpr as simplefield OVER simplefield"""
    over = ParseTreeNode('FUNCTION', raw='over')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([p[1].children[0], p[3]])
    p[5].role = ''.join(['OVER_', p[5].role])
    over.add_children([asn, p[5]])
    p[0] = [over]

def p_carg_statsfn_as_over(p):
    """carg : STATS_FN as simplefield OVER simplefield"""
    p[1] = canonicalize(p[1]) 
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    over = ParseTreeNode('FUNCTION', raw='over')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([statsfn, p[3]])
    p[5].role = ''.join(['OVER_', p[5].role])
    over.add_children([asn, p[5]])
    p[0] = [over]

def p_carg_statsfnexpr_as_over_by(p):
    """carg : statsfnexpr as simplefield OVER simplefield splitbyclause"""
    over = ParseTreeNode('FUNCTION', raw='over')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([p[1].children[0], p[3]])
    over.add_children([asn, p[5]])
    p[5].role = ''.join(['OVER_', p[5].role])
    p[6][0].children.insert(0, over)
    over.parent = p[6][0]
    p[0] = p[6]

def p_carg_statsfn_as_over_by(p): # TODO
    """carg : STATS_FN as simplefield OVER simplefield splitbyclause"""
    p[1] = canonicalize(p[1]) 
    over = ParseTreeNode('FUNCTION', raw='over')
    asn = ParseTreeNode('FUNCTION', raw='as')
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    asn.add_children([statsfn, p[3]])
    over.add_children([asn, p[5]])
    p[5].role = ''.join(['OVER_', p[5].role])
    p[6][0].children.insert(0, over)
    over.parent = p[6][0]
    p[0] = p[6]

def p_error(p):
    raise SPLSyntaxError("Syntax error in chart parser input!") 
