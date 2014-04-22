
import re

from splparser.parsetree import *

from splparser.rules.common.asrules import *
from splparser.rules.common.byrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.simplefieldlistrules import *
from splparser.rules.common.statsfnrules import *

def check_option_value(option, value):
    log_pattern = r'[\d]*\.?[\d]*log[\d]*\.?[\d]*'
    if option in ("sep", "format", "nullstr", "otherstr"):
        if not value.nodetype in ['WORD', 'ID', 'NBSTR', 'LITERAL']:
            value.nodetype = 'NBSTR'
    if option in ("limit", "bins", "span", "start", "end"):
        if not value.nodetype in ['INT', 'FLOAT']:
            value.nodetype = 'INT'
        if len(re.findall(log_pattern, value.raw)) == 1:
            value.nodetype = 'LOG'
    if option in ("cont", "usenull", "useother"):
        value.nodetype = 'BOOLEAN'
    if option in ("agg"):
        value.role = value.raw.upper()
        value.nodetype = "SPL"

def p_carglist_carg(p):
    """carglist : carg"""
    p[0] = p[1]

def p_carglist(p):
    """carglist : carg carglist"""
    p[0] = p[1] + p[2]

def p_carglist_comma(p):
    """carglist : carg COMMA carglist"""
    p[0] = p[1] + p[3]

def p_carg(p):
    """carg : coptlist"""
    p[0] = p[1]

def p_ctoptlist_copt(p):
    """coptlist : copt"""
    p[0] = p[1]

def p_ctoptlist(p):
    """coptlist : copt coptlist"""
    p[0] = p[1] + p[2]

def p_copt(p):
    """copt : CHART_OPT EQ simplevalue
            | COMMON_OPT EQ simplevalue"""
    p[1] = canonicalize(p[1])
    check_option_value(p[1], p[3]) 
    eq = ParseTreeNode('EQ', raw='assign')
    copt = ParseTreeNode('OPTION', raw=p[1])
    copt.values.append(p[3])
    eq.add_children([copt, p[3]])
    p[0] = [eq]

def p_carg_statsfn(p):
    """carg : STATS_FN"""
    p[1] = canonicalize(p[1])
    p[0] = [ParseTreeNode('FUNCTION', raw=p[1])]

def p_carg_statsfn_as(p):
    """carg : STATS_FN as simplefield"""
    p[1] = canonicalize(p[1])
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([statsfn, p[3]])
    p[0] = [asn]

def p_carg_statsfnexpr(p):
    """carg : statsfnexpr"""
    p[0] = [p[1].children[0]]

def p_carg_statsfnexpr_as(p):
    """carg : statsfnexpr as simplefield"""
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([p[1].children[0], p[3]])
    p[0] = [asn]

def p_carg_macro(p):
    """carg : MACRO"""
    p[0] = [ParseTreeNode('MACRO', raw=p[1], is_argument=True)]

def p_carg_statsfn_by(p):
    """carg : STATS_FN splitbyclause"""
    p[1] = canonicalize(p[1])
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    p[2][0].children.insert(0, statsfn)
    statsfn.parent = p[2][0]
    p[0] = p[2]

def p_carg_statsfnexpr_by(p):
    """carg : statsfnexpr splitbyclause"""
    statsfn = p[1].children
    p[2][0].children = statsfn + p[2][0].children
    statsfn[0].parent = p[2][0]
    p[0] = p[2]

def p_carg_statsfnexpr_as_by(p):
    """carg : statsfnexpr as simplefield splitbyclause"""
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([p[1].children[0], p[3]])
    p[4][0].children.insert(0, asn)
    asn.parent = p[4][0]
    p[0] = p[4]

def p_carg_statsfn_as_by(p):
    """carg : STATS_FN as simplefield splitbyclause"""
    p[1] = canonicalize(p[1])
    statsfn = ParseTreeNode('FUNCTION', raw=p[1])
    asn = ParseTreeNode('FUNCTION', raw='as')
    asn.add_children([statsfn, p[3]])
    p[4][0].children.insert(0, asn)
    asn.parent = p[4][0]
    p[0] = p[4]

def p_splitbyclause(p):
    """splitbyclause : by simplefieldlist"""
    by = ParseTreeNode('FUNCTION', raw='groupby')
    for c in p[2].children:
        c.role = 'GROUPING_' + c.role
    by.add_children(p[2].children)
    p[0] = [by]

# TODO: How do we include the 'where*' rules in the schema extraction?
def p_splitbyclause_where(p):
    """splitbyclause : by simplefieldlist wherecomp"""
    by = ParseTreeNode('FUNCTION', raw='groupby')
    for c in p[2].children:
        c.role = 'GROUPING_' + c.role
    by.add_children(p[2].children)
    p[0] = [by, p[3]]

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
    wherestr = '_'.join([p[1], p[2]])
    where = ParseTreeNode('FUNCTION', raw=wherestr)
    where.add_child(p[3])

def p_wherethreshcomp_gt(p):
    """wherethreshcomp : GT int"""
    p[0] = ParseTreeNode('FUNCTION', raw='gt')
    p[0].add_child(p[2])

def p_wherethreshcomp_lt(p):
    """wherethreshcomp : LT int"""
    p[0] = ParseTreeNode('FUNCTION', raw='lt')
    p[0].add_child(p[2])
