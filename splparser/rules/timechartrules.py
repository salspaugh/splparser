#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.byrules import *
from splparser.rules.common.chartrules import *
from splparser.rules.common.simplefieldrules import *
from splparser.rules.common.statsfnrules import *

from splparser.lexers.timechartlexer import precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_timechart(p):
    """cmdexpr : timechartcmd"""
    p[0] = p[1]

def p_timechartcmd(p):
    """timechartcmd : TIMECHART carglist
                    | SITIMECHART carglist"""
    p[0] = ParseTreeNode('COMMAND', raw=p[1])
    p[0].add_children(p[2])
   
def p_error(p):
    raise SPLSyntaxError("Syntax error in timechart parser input!") 
