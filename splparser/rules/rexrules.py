#!/usr/bin/env python
#


from splparser.parsetree import *

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.rules.common.regexrules import *

from splparser.lexers.rexlexer import tokens

from splparser.exceptions import *

start = 'cmdexpr'

def p_cmdexpr_rex(p):
    """cmdexpr : rexcmd"""
    p[0] = p[1]

def p_rexcmd_rex(p):
    """rexcmd : REX regex"""
    p[0] = ParseTreeNode('COMMAND', raw='rex')
    p[0].add_child(p[2])

def p_rexcmd_some_rex(p):
    """rexcmd : REX rex_req regex
              | REX regex max_match"""
    p[0] = ParseTreeNode('COMMAND', raw='rex')
    p[0].add_children([p[2], p[3]])

def p_rexcmd_more_rex(p):
    """rexcmd : REX rex_req rex_req regex
              | REX rex_req regex max_match
              | REX rex_req max_match regex"""
    p[0] = ParseTreeNode('COMMAND', raw='rex')
    p[0].add_children([p[2], p[3], p[4]])

def p_rexcmd_someother_rex(p):
    """rexcmd : REX rex_req  max_match rex_req regex""" 
    p[0] = ParseTreeNode('COMMAND', raw='rex')
    p[0].add_children([p[2], p[3], p[4], p[5]])

def p_rexcmd_error_rex(p):
    """rexcmd : rexcmd value"""
    p[0] = p[1]
    p[0].add_child(p[2])

def p_rex_req(p):
    """rex_req : rex_opt EQ value"""
    if p[1].raw == 'field':
        p[3].role = 'FIELD'
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_rex_max_match(p):
    """max_match : MAX_MATCH EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    opt_node = ParseTreeNode('OPTION', raw=p[1])
    opt_node.values.append(p[3])
    p[0].add_child(opt_node)
    p[0].add_child(p[3])

def p_rex_opt(p):
    """rex_opt : FIELD
               | MODE"""
    p[0] = ParseTreeNode('OPTION', raw=p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in rex parser input!") 

