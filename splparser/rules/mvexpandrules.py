#!/usr/bin/env python

from splparser.parsetree import *

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.mvexpandlexer import tokens
from splparser.exceptions import SPLSyntaxError

start = 'cmdexpr'

def p_cmdexpr_fillnull(p):
    """cmdexpr : mvexpandcmd"""
    p[0] = p[1]

def p_fillnullcmd_fillnull(p):
    """mvexpandcmd : MVEXPAND"""
    p[0] = ParseTreeNode('MVEXPAND')

def p_fillnullcmd_value(p):
    """mvexpandcmd : MVEXPAND field"""
    p[0] = ParseTreeNode('MVEXPAND')
    p[0].add_child(p[2])

def p_fieldlist(p):
    """mvexpandcmd : MVEXPAND field m_limit"""
    p[0] = ParseTreeNode('MVEXPAND')
    p[0].add_children([p[2],p[3]])

def p_value(p):
    """m_limit : LIMIT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1] = ParseTreeNode(p[1].upper(), option=True)
    p[1].values.append(p[3])
    p[0].add_children([p[1],p[3]])

def p_error(p):
    raise SPLSyntaxError("Syntax error in mvexpand parser input!") 
