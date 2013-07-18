#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.loadjoblexer import tokens

start = 'cmdexpr'

def p_cmdexpr_loadjob(p):
    """cmdexpr : loadjobcmd"""
    p[0] = p[1]

def p_cmdexpr_loadjob_single(p):
    """loadjobcmd : LOADJOB"""
    p[0] = ParseTreeNode('LOADJOB')

def p_cmdexpr_loadjob_field(p):
    """loadjobcmd : LOADJOB fieldlist wc_stringlist"""
    p[0] = ParseTreeNode('LOADJOB')
    p[0].add_children(p[2].children)
    p[0].add_children(p[3].children)

def p_loadjobcmd_loadjob(p):
    """loadjobcmd : LOADJOB wc_stringlist
                  | LOADJOB fieldlist"""
    p[0] = ParseTreeNode('LOADJOB')
    p[0].add_children(p[2].children)

def p_loadjob_opt(p):
    """wc_string : LOADJOB_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode(p[1].upper(), option=True)
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_loadjob_opt_list(p):
    """wc_stringlist : wc_string"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])

def p_loadjob_optlist(p):
    """wc_stringlist : wc_string wc_stringlist"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in loadjob parser input!")
