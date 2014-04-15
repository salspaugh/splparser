#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.valuerules import *

from splparser.lexers.outputcsvlexer import tokens

BOOLEAN_OPTIONS = ["append", "create_empty", "dispatch", "singlefile", "usexml"]

start = 'cmdexpr'

def p_cmdexpr(p):
    """cmdexpr : outputcsvcmd"""
    p[0] = p[1]

def p_cmdexpr_outputcsv(p):
    """outputcsvcmd : OUTPUTCSV
                    | OUTPUTCSV outputcsvarglist"""
    p[0] = ParseTreeNode('COMMAND', raw='outputcsv')
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_outputcsvarglist_outputcsvargs(p):
    """outputcsvarglist : outputcsvarg
                        | outputcsvarg outputcsvarglist"""
    p[0] = ParseTreeNode('_OUTPUTCSVARGLIST')
    p[0].add_child(p[1])
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_outputcsvarg_opt(p):
    """outputcsvarg : OUTPUTCSV_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw=p[1])
    if opt.raw in BOOLEAN_OPTIONS:
        p[3].nodetype = 'BOOLEAN'
    opt.values.append(p[3])
    p[0].add_children([opt, p[3]])

def p_outputcsvarg_path(p):
    """outputcsvarg : value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt = ParseTreeNode('OPTION', raw='filename')
    opt.values.append(p[1])
    p[0].add_children([opt, p[1]])

def p_error(p):
    raise SPLSyntaxError("Syntax error in outputcsv parser input!")
