#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.fieldlistrules import *

from splparser.lexers.joinlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_join(p):
    """cmdexpr : joincmd"""
    p[0] = p[1]

def p_join(p):
    """joincmd : JOIN"""
    p[0] = ParseTreeNode('JOIN')

def p_join_optionlist(p):
    """joincmd : JOIN optionlist"""
    p[0] = ParseTreeNode('JOIN')
    p[0].add_children(p[2])

def p_join_optionlist_fieldlist(p):
    """joincmd : JOIN optionlist fieldlist"""
    p[0] = ParseTreeNode('JOIN')
    p[0].add_children(p[2] + [p[3]])

def p_optionlist_single(p):
    """optionlist : JOIN_OPT EQ field"""
    opt = ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt]

def p_optionlist(p):
    """optionlist : JOIN_OPT EQ field optionlist"""
    opt= ParseTreeNode(p[1].upper(), option=True)
    opt.values.append(p[3])
    opt.add_child(p[3])
    p[0] = [opt] + p[4]

def p_error(p):
    raise SPLSyntaxError("Syntax error in join parser input!")
