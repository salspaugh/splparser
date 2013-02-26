#!/usr/bin/env python

from splparser.lexer import tokens
from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.commandrules import *

start = 'start'

def p_pipeline_start(p):
    """start : pipeline"""
    p[0] = ParseTreeNode('ROOT')
    p[0].add_children(p[1].children)

def p_pipeline_stage(p):
    """pipeline : stage"""
    p[0] = ParseTreeNode('_PIPELINE')
    p[0].add_child(p[1])

def p_pipeline_pipe(p):
    """pipeline : pipeline PIPE stage"""
    p[0] = ParseTreeNode('_PIPELINE')
    p[0].add_children(p[1].children) 
    p[0].add_child(p[3])

def p_stage_cmdexpr(p):
    """stage : cmdexpr"""
    p[0] = ParseTreeNode('STAGE')
    p[0].add_child(p[1])

def p_stage_macro(p):
    """stage : MACRO"""
    p[0] = ParseTreeNode('STAGE')
    p[0].add_child(ParseTreeNode('MACRO', raw=p[1]))

def p_arglist(p):
    """arglist : args"""
    p[0] = p[1]

def p_args(p):
    """args : ARGS"""
    p[0] = p[1]

def p_args_fields(p):
    """args : FIELDS"""
    p[0] = p[1]

def p_arglist_arg(p):
    """arglist : arglist args"""
    p[0] = ' '.join(p[1:])

def p_arglist_macro(p):
    """arglist : arglist MACRO"""
    p[0] = ' '.join(p[1:])

def p_macro_arglist(p):
    """arglist : MACRO arglist"""
    p[0] = ' '.join(p[1:])

def p_error(p):
    msg = "Syntax error in top-level parser input: " + p
    raise TerminatingSPLSyntaxError(msg)
