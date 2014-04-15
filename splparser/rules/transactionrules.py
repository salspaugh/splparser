#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.transactionlexer import tokens

start = 'cmdexpr'

boolean_options = ["connected", "keeporphans", "unifyends", "keepevicted", "mvlist", "mvraw"]

def p_cmdexpr_transaction(p):
    """cmdexpr : transactioncmd"""
    p[0] = p[1]

def p_transaction_options(p):
    """transactioncmd : TRANSACTION optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='transaction')
    p[0].add_children(p[2])

def p_transaction_fieldlist_options(p):
    """transactioncmd : TRANSACTION fieldlist optionlist"""
    p[0] = ParseTreeNode('COMMAND', raw='transaction')
    p[0].add_children(p[2].children + p[3])

def p_optionlist_single(p):
    """optionlist : TRANSACTION_OPT EQ field"""
    eq = ParseTreeNode('EQ', raw='assign')    
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    eq.add_children([opt, p[3]])
    p[0] = [eq]

def p_optionlist(p):
    """optionlist : TRANSACTION_OPT EQ field optionlist"""
    eq = ParseTreeNode('EQ', raw='assign')    
    opt = ParseTreeNode('OPTION', raw=p[1])
    p[3].role = 'VALUE'
    if opt.raw in boolean_options:
        p[3].nodetype = 'BOOLEAN'
    eq.add_children([opt, p[3]])
    p[0] = [eq] + p[4]


def p_error(p):
    raise SPLSyntaxError("Syntax error in transaction parser input!")
