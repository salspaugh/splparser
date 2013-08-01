#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.evalfnexprrules import *
from splparser.rules.common.simplefieldrules import *

from splparser.lexers.fieldformatlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_fieldformat(p):
    """cmdexpr : fieldformatcmd"""
    p[0] = p[1]

def p_fieldformat_fieldformatexpr(p):
    """fieldformatcmd : FIELDFORMAT oplist"""
    p[0] = ParseTreeNode('COMMAND', raw='fieldformat')
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in fieldformat parser input!") 
