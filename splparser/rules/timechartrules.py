#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.asrules import *
from splparser.cmdparsers.common.byrules import *
from splparser.cmdparsers.common.simplefieldrules import *
from splparser.cmdparsers.common.statsfnrules import *

from splparser.lexers.timechartlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_timechart(p):
    """cmdexpr : timechartcmd"""
    p[0] = p[1]

def p_timechartcmd(p):
    """timechartcmd : TIMECHART tcarglist"""
    p[0] = ParseTreeNode('TIMECHART')
    p[0].add_children(p[2].children)
   
def p_tctarglist_tcarg(p):
    """tcarglist : tcarg"""
    p[0] = ParseTreeNode('_TCARGLIST')
    if p[1].type == '_TCOPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])

def p_tcarglist(p):
    """tcarglist : tcarg tcarglist"""
    p[0] = ParseTreeNode('_TCARGLIST')
    if p[1].type == '_TCOPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[2].children)    

def p_tcarglist_comma(p):
    """tcarglist : tcarg COMMA tcarglist"""
    p[0] = ParseTreeNode('_TCARGLIST')
    if p[1].type == '_TCOPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[3].children)    

def p_tcarg(p):
    """tcarg : tcoptlist"""
    p[0] = p[1]

def p_tctoptlist_tcopt(p):
    """tcoptlist : tcopt"""
    p[0] = ParseTreeNode('_TCOPTLIST')
    p[0].add_child(p[1])

def p_tctoptlist(p):
    """tcoptlist : tcopt tcoptlist"""
    p[0] = ParseTreeNode('_TCOPTLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)    

def p_tcopt(p):
    """tcopt : TIMECHART_OPT EQ simplevalue
             | COMMON_OPT EQ simplevalue"""
    p[0] = ParseTreeNode('EQ')
    tcopt_node = ParseTreeNode(p[1].upper())
    p[0].add_child(tcopt_node)
    p[0].add_child(p[3])

def p_tcarg_statsfn(p):
    """tcarg : STATS_FN"""
    p[0] = ParseTreeNode(p[1].upper())

def p_tcarg_statsfn_as(p):
    """tcarg : STATS_FN as simplefield"""
    p[0] = ParseTreeNode(p[1].upper())
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])

def p_tcarg_statsfnexpr(p):
    """tcarg : statsfnexpr"""
    p[0] = p[1].children[0]

def p_tcarg_statsfnexpr_as(p):
    """tcarg : statsfnexpr as simplefield"""
    p[0] = p[1].children[0]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])

def p_tcarg_macro(p):
    """tcarg : MACRO"""
    p[0] = ParseTreeNode('MACRO', raw=p[1])

def p_tcarg_statsfn_by(p):
    """tcarg : STATS_FN splitbyclause"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[2].children)

def p_tcarg_statsfnexpr_by(p):
    """tcarg : statsfnexpr splitbyclause"""
    p[0] = p[1].children[0]
    p[0].add_children(p[2].children)

def p_splitbyclause(p):
    """splitbyclause : by simplefield"""
    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
    by_node = ParseTreeNode('BY')
    p[0].add_child(by_node)
    by_node.add_child(p[2])

#def p_splitbyclause_tcopt(p):
#    """splitbyclause : by simplefield tcoptlist"""
#    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
#    by_node = ParseTreeNode('BY')
#    p[0].add_child(by_node)
#    by_node.add_child(p[2])
#    p[0].add_children(p[3].children)

def p_splitbyclause_where(p):
    """splitbyclause : by simplefield wherecomp"""
    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
    by_node = ParseTreeNode('BY')
    p[0].add_child(by_node)
    by_node.add_child(p[2])
    by_node.add_child(p[3])

##def p_splitbyclause_tcopt_where(p):
##    """splitbyclause : by simplefield tcoptlist statsfnexpr wherecomp"""
##    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
##    by_node = ParseTreeNode('BY')
##    p[0].add_child(by_node)
##    p[0] = ParseTreeNode('BY')
##    p[0] = ParseTreeNode('BY')
##    p[0].add_child(p[2])
##    p[0].add_children(p[3].children)
##    p[0].add_child(p[4])
##    p[0].add_children(p[5].children)
#
def p_wherecomp(p):
    """wherecomp : int
                 | whereincomp
                 | wherethreshcomp"""
    p[0] = p[1]    

def p_whereincomp(p):
    """whereincomp : IN TOP int
                   | NOTIN TOP int
                   | IN BOTTOM int
                   | NOTIN BOTTOM int"""
    p[0] = ParseTreeNode(p[1].upper())
    tb_node = ParseTreeNode(p[2].upper())
    p[0].add_child(tb_node)
    tb_node.add_child(p[3])

def p_wherethreshcomp_gt(p):
    """wherethreshcomp : GT int"""
    p[0] = ParseTreeNode('GT')
    p[0].add_child(p[2])

def p_wherethreshcomp_lt(p):
    """wherethreshcomp : LT int"""
    p[0] = ParseTreeNode('LT')
    p[0].add_child(p[2])

def p_error(p):
    raise SPLSyntaxError("Syntax error in timechart parser input!") 
