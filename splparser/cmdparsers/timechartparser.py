#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.asrules import *
from splparser.cmdparsers.common.byrules import *
from splparser.cmdparsers.common.simplefieldrules import *
from splparser.cmdparsers.common.simplefieldlistrules import *
from splparser.cmdparsers.common.statsfnrules import *

from splparser.cmdparsers.statslexer import lexer, precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_timechart(p):
    """cmdexpr : timechartcmd"""

def p_timechartcmd(p):
    """timechartcmd : TIMECHART tcarglist"""
   
def p_tctarglist_tcarg(p):
    """tcarglist : tcarg"""

def p_tctarglist(p):
    """tcarglist : tcarg tcarglist"""

def p_tcarg(p):
    """tcarg : tcopt"""

def p_tcopt(p):
    """tcopt : TIMECHART_OPT EQ simplevalue"""

def p_tcarg(p):
    """tcarg : statsfnexpr"""

def p_tcarg_by(p):
    """tcarg : statsfnexpr splitbyclause"""

def p_splitbyclause(p):
    """splitbyclause : by simplefield"""

def p_splitbyclause_tcopt(p):
    """splitbyclause : by simplefield tcoptlist"""

def p_splitbyclause_where(p):
    """splitbyclause : by simplefield whereclause"""

def p_splitbyclause_tcopt_where(p):
    """splitbyclause : by simplefield tcoptlist statfnexpr wherecomp"""

def p_wherecomp(p):
    """wherecomp : int
                 | whereincomp
                 | wherethreshcomp"""

def p_whereincomp(p):
    """whereincomp : IN TOP int
                   | NOTIN TOP int
                   | IN BOTTOM int
                   | NOTIN BOTTOM int"""

def p_wherethreshcomp(p):
    """wherethreshcomp : GT int
                       | LT int"""

def p_error(p):
    raise SPLSyntaxError("Syntax error in timechart parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "timechartparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="stats_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
