#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.lexers.auditlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_audit(p):
    """cmdexpr : auditcmd"""
    p[0] = p[1]

def p_cmdexpr_audit_debug(p):
    """auditcmd : AUDIT"""
    p[0] = ParseTreeNode('COMMAND', raw='audit')

def p_error(p):
    raise SPLSyntaxError("Syntax error in audit parser input!") 
