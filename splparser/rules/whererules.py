#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.evalfnexprrules import *
from splparser.rules.common.simplefieldrules import *

from splparser.lexers.wherelexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_where(p):
    """cmdexpr : wherecmd"""
    p[0] = p[1]

def p_where_whereexpr(p):
    """wherecmd : WHERE oplist"""
    p[0] = ParseTreeNode('WHERE')
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in where parser input!") 
