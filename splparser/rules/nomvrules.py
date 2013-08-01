#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *

from splparser.lexers.nomvlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_nomv(p):
    """cmdexpr : nomvcmd"""
    p[0] = p[1]

def p_cmdexpr_nomv_single(p):
    """nomvcmd : NOMV"""
    p[0] = ParseTreeNode('COMMAND', raw='novm')

def p_addtotalscmd_nomv(p):
    """nomvcmd : NOMV field"""
    p[0] = ParseTreeNode('COMMAND', raw='nomv')
    p[0].add_child(p[2])

def p_error(p):
    raise SPLSyntaxError("Syntax error in nomv parser input!")
