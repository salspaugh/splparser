#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError

from splparser.rules.commandrules import *

from splparser.lexers.toplevellexer import tokens

start = 'start'

def p_pipeline_start(p):
    """start : pipeline"""
    p[0] = ParseTreeNode('ROOT')
    p[0].add_children(p[1].children)

def p_pipeline_generator(p):
    """start : PIPE pipeline"""
    p[0] = ParseTreeNode('ROOT')
    p[0].add_children(p[2].children)

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

def p_stage_cmdexpr_subsearch(p):
    """stage : cmdexpr LBRACKET start RBRACKET"""
    p[0] = ParseTreeNode('STAGE')
    p[0].add_child(p[1])
    subsearch = ParseTreeNode('SUBSEARCH')
    subsearch.add_child(p[3])
    p[1].add_child(subsearch)

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

def p_args_where(p):
    """args : WHERE"""
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

def p_cmdexpr_userdefinedcommand(p):
    """cmdexpr : USER_DEFINED_COMMAND 
               | USER_DEFINED_COMMAND arglist"""
    p[0] = ParseTreeNode('USER_DEFINED_COMMAND', nodetype='USER_DEFINED', raw=p[1])
    if len(p) > 2:
        args = ParseTreeNode('ARGS', nodetype='UNKNOWN', raw=p[2], is_argument=True)
        p[0].add_child(args)

def p_error(p):
    msg = "Syntax error in top-level parser input: " + str(p)
    raise TerminatingSPLSyntaxError(msg)
