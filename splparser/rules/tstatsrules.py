#!/usr/bin/env python

import re

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.byrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.simplefieldlistrules import *
from splparser.rules.common.statsfnrules import *
from splparser.rules.common.searchclauserules import *

from splparser.lexers.tstatslexer import precedence, tokens

BOOLEAN_OPTIONS = ["prestats", "local", "append", "summariesonly"]

start = 'cmdexpr'

# NOTE: The strange structure of these rules is because we need to always
#       associate STATS_FN with another token on the RHS of rules because
#       otherwise we get a reduce/reduce conflict from the rule
#           simplefield : STATS_FN
#       since nothing prevents simplefields from having the same name as command
#       functions.

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
    groupby.children = filter(lambda x: x.raw != 'groupby' and x.raw != 'assign', command.children) + groupby.children 
    for c in groupby.children:
        c.parent = groupby
    command.children = filter(lambda x: x.raw == 'assign', command.children) + [groupby]

def p_cmdexpr_stats(p):
    """cmdexpr : statscmd"""
    p[0] = p[1]

def p_statscmd_statsoptlist(p):
    """statscmd : statscmd statsoptlist"""
    p[0] = p[1]
    p[0].add_children(p[2].children)

def p_statscmd(p):
    """statscmd : statscmdstart"""
    p[0] = p[1]

def p_statscmd_cont(p):
    """statscmd : statscmdstart statscmdcont
                | statscmdstart fromstmt statscmdcont"""
    p[0] = p[1]
    p[0].add_children(p[2].children)
    correct_groupby(p[0])
    if len(p) > 3:
        p[0].add_children(p[2].children)

def p_statscmdstart(p):
    """statscmdstart : TSTATS STATS_FN
                     | TSTATS COMMON_FN  
                     | TSTATS EVAL
                     | TSTATS statsoptlist STATS_FN
                     | TSTATS statsoptlist COMMON_FN
                     | TSTATS statsoptlist EVAL"""
    p[2] = canonicalize(p[2]) 
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    fn_idx = 2
    if len(p) > 3:
        fn_idx = 3
        p[0].add_children(p[2].children)
    fn_node = ParseTreeNode('FUNCTION', raw=p[fn_idx])
    p[0].add_child(fn_node)

def p_statsoptlist(p):
    """statsoptlist : statsopt"""
    p[0] = ParseTreeNode('_TSTATS_OPT_LIST')
    p[0].add_child(p[1])

def p_statsoptlist_statsopt(p):
    """statsoptlist : statsopt statsoptlist"""
    p[0] = ParseTreeNode('_TSTATS_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_statsopt_simplefield(p):
    """statsopt : TSTATS_OPT EQ simplefield"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in BOOLEAN_OPTIONS:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    p[0].add_child(opt)
    p[0].add_child(p[3])

def p_statsopt_delimiter(p):
    """statsopt : TSTATS_OPT EQ COMMA"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    comma = ParseTreeNode('VALUE', nodetype="NBSTR", raw=p[3])
    opt.values.append(comma)
    p[0].add_child(opt)
    p[0].add_child(comma)

def p_statscmdstart_statsfnexpr(p):
    """statscmdstart : TSTATS statsfnexpr
                     | TSTATS statsoptlist statsfnexpr"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    fn_idx = 2
    if len(p) > 3:
        fn_idx = 3
        p[0].add_children(p[2].children)
    p[0].add_children(p[fn_idx].children)

def p_statscmdcont_fromstmt(p):
    """statscmdcont : fromstmt"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_child(p[1])

def p_statscmdcont_fromstmt_where(p):
    """statscmdcont : fromstmt wherestmt"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_child(p[1])
    p[0].add_child(p[2])

def p_fromstmt(p):
    """fromstmt : from simplevalue"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_children([p[1], p[2]])

def p_statscmdcont_statscmdcont(p):
    """statscmdcont : statscmdcont statscmdcont"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[1].children)
    p[0].add_children(p[2].children)

def p_statscmdcont(p):
    """statscmdcont : COMMA STATS_FN
                    | COMMA COMMON_FN
                    | COMMA EVAL"""
    p[2] = canonicalize(p[2]) 
    p[0] = ParseTreeNode('_STATSCMDCONT')
    fn_node = ParseTreeNode('FUNCTION', raw=p[2])
    p[0].add_child(fn_node)

def p_statscmdcont_nocomma(p):
    """statscmdcont : STATS_FN
                    | COMMON_FN
                    | EVAL"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSCMDCONT')
    fn_node = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(fn_node)

def p_statscmdcont_statsfnexpr(p):
    """statscmdcont : COMMA statsfnexpr"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[2].children)

def p_statscmdcont_statsfnexpr_nocomma(p):
    """statscmdcont : statsfnexpr"""
    p[0] = ParseTreeNode('_STATSCMDCONT')
    p[0].add_children(p[1].children)

def p_statsfnexpr_fnas(p):
    """statsfnexpr : STATS_FN as simplefield
                   | COMMON_FN as simplefield"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    asn = ParseTreeNode('FUNCTION', raw='as')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    asn.add_children([fn, p[3]])
    p[0].add_child(asn)

def p_statsfnexpr_fnexpras(p):
    """statsfnexpr : statsfnexpr as simplefield"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children(p[1].children + [p[3]])
    p[0].add_child(asn)

def p_statsfnexpr_fnasby(p):
    """statsfnexpr : STATS_FN as simplefield by simplefieldlist
                   | COMMON_FN as simplefield by simplefieldlist"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    asn = ParseTreeNode('FUNCTION', raw='as')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    asn.add_children([fn, p[3]])
    for c in p[5].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([asn] + p[5].children)
    p[0].add_child(by)

def p_statsfnexpr_fnasby_where(p):
    """statsfnexpr : STATS_FN as simplefield wherestmt by simplefieldlist
                   | COMMON_FN as simplefield wherestmt by simplefieldlist"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    asn = ParseTreeNode('FUNCTION', raw='as')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    asn.add_children([fn, p[3]])
    p[0].add_child(p[4])
    for c in p[6].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([asn] + p[6].children)
    p[0].add_child(by)

def p_statsfnexpr_fnexprasby(p):
    """statsfnexpr : statsfnexpr as simplefield by simplefieldlist"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children(p[1].children + [p[3]])
    for c in p[5].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([asn] + p[5].children)
    p[0].add_child(by)

def p_statsfnexpr_fnexprasby_where(p):
    """statsfnexpr : statsfnexpr as simplefield wherestmt by simplefieldlist"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children(p[1].children + [p[3]])
    p[0].add_child(p[4])
    for c in p[6].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([asn] + p[6].children)
    p[0].add_child(by)

def p_statsfnexpr_fnby(p):
    """statsfnexpr : STATS_FN by simplefieldlist
                   | COMMON_FN by simplefieldlist"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    for c in p[3].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([fn] + p[3].children)
    p[0].add_child(by)

def p_statsfnexpr_fnby_where(p):
    """statsfnexpr : STATS_FN wherestmt by simplefieldlist
                   | COMMON_FN wherestmt by simplefieldlist"""
    p[1] = canonicalize(p[1]) 
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    fn = ParseTreeNode('FUNCTION', raw=p[1])
    p[0].add_child(p[2])
    for c in p[4].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children([fn] + p[4].children)
    p[0].add_child(by)

def p_statsfnexpr_fnexprby(p):
    """statsfnexpr : statsfnexpr by simplefieldlist"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    for c in p[3].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children(p[1].children + p[3].children)
    p[0].add_child(by)

def p_statsfnexpr_fnexprby_where(p):
    """statsfnexpr : statsfnexpr wherestmt by simplefieldlist"""
    p[0] = ParseTreeNode('_STATSFNEXPR')
    by = ParseTreeNode('FUNCTION', raw='groupby')
    p[0].add_child(p[2])
    for c in p[4].children:
        c.role = '_'.join(['GROUPING', c.role])
    by.add_children(p[1].children + p[4].children)
    p[0].add_child(by)


def p_from(p):
    """from : FROMUC
            | FROMLC"""
    p[0] = ParseTreeNode('OPTION', raw='from')

def p_where(p):
    """where : WHEREUC
             | WHERELC"""
    p[0] = ParseTreeNode('FUNCTION', raw='where')

def p_wherestmt(p):
    """wherestmt : where searchexpr"""
    p[0] = p[1]
    p[0].add_child(p[2])

def p_searchexpr_eq(p):
    """searchexpr : simplefield EQ simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='eq')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_ne(p):
    """searchexpr : simplefield NE simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='ne')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_lt(p):
    """searchexpr : simplefield LT simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='lt')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_le(p):
    """searchexpr : simplefield LE simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='le')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_ge(p):
    """searchexpr : simplefield GE simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='ge')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_searchexpr_gt(p):
    """searchexpr : simplefield GT simplevalue"""
    p[0] = ParseTreeNode('FUNCTION', raw='gt')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])    

def p_error(p):
    raise SPLSyntaxError("Syntax error in tstats parser input!") 
