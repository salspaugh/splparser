from splparser.parsetree import *

from splparser.rules.common.asrules import *
from splparser.rules.common.byrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.simplefieldlistrules import *
from splparser.rules.common.statsfnrules import *

def p_carglist_carg(p):
    """carglist : carg"""
    p[0] = ParseTreeNode('_CARGLIST')
    if p[1].type == '_COPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])

def p_carglist(p):
    """carglist : carg carglist"""
    p[0] = ParseTreeNode('_CARGLIST')
    if p[1].type == '_COPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[2].children)    

def p_carglist_comma(p):
    """carglist : carg COMMA carglist"""
    p[0] = ParseTreeNode('_CARGLIST')
    if p[1].type == '_COPTLIST':
        p[0].add_children(p[1].children)
    else:
        p[0].add_child(p[1])
    p[0].add_children(p[3].children)    

def p_carg(p):
    """carg : coptlist"""
    p[0] = p[1]

def p_ctoptlist_copt(p):
    """coptlist : copt"""
    p[0] = ParseTreeNode('_COPTLIST')
    p[0].add_child(p[1])

def p_ctoptlist(p):
    """coptlist : copt coptlist"""
    p[0] = ParseTreeNode('_COPTLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)    

def p_copt(p):
    """copt : CHART_OPT EQ simplevalue
            | COMMON_OPT EQ simplevalue"""
    p[0] = ParseTreeNode('EQ')
    copt_node = ParseTreeNode(p[1].upper())
    p[0].add_child(copt_node)
    p[0].add_child(p[3])

def p_carg_statsfn(p):
    """carg : STATS_FN"""
    p[0] = ParseTreeNode(p[1].upper())

def p_carg_statsfn_as(p):
    """carg : STATS_FN as simplefield"""
    p[0] = ParseTreeNode(p[1].upper())
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])

def p_carg_statsfnexpr(p):
    """carg : statsfnexpr"""
    p[0] = p[1].children[0]

def p_carg_statsfnexpr_as(p):
    """carg : statsfnexpr as simplefield"""
    p[0] = p[1].children[0]
    as_node = ParseTreeNode('AS')
    p[0].add_child(as_node)
    as_node.add_child(p[3])

def p_carg_macro(p):
    """carg : MACRO"""
    p[0] = ParseTreeNode('MACRO', raw=p[1])

def p_carg_statsfn_by(p):
    """carg : STATS_FN splitbyclause"""
    p[0] = ParseTreeNode(p[1].upper())
    p[0].add_children(p[2].children)

def p_carg_statsfnexpr_by(p):
    """carg : statsfnexpr splitbyclause"""
    p[0] = p[1].children[0]
    p[0].add_children(p[2].children)

def p_splitbyclause(p):
    """splitbyclause : by simplefieldlist"""
    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
    by_node = ParseTreeNode('BY')
    p[0].add_child(by_node)
    by_node.add_children(p[2].children)

def p_splitbyclause_where(p):
    """splitbyclause : by simplefieldlist wherecomp"""
    p[0] = ParseTreeNode('_SPLITBYCLAUSE')
    by_node = ParseTreeNode('BY')
    p[0].add_child(by_node)
    by_node.add_children(p[2].children)
    by_node.add_child(p[3])

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
