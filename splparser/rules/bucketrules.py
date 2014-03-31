#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.asrules import *
from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *
    
from splparser.lexers.bucketlexer import tokens

start = 'cmdexpr'

def p_cmdexpr_bucket(p):
    """cmdexpr : bucketcmd"""
    p[0] = p[1]

def p_bucketcmd(p):
    """bucketcmd : BUCKET bucketargs
                 | BIN_CMD bucketargs"""
    p[0] = ParseTreeNode('COMMAND', raw='bucket')
    p[0].add_child(p[2])

def p_bucketargs(p):
    """bucketargs : field"""
    p[0] = p[1]

def p_bucketargs_as(p):
    """bucketargs : field as field"""
    p[0] = ParseTreeNode('FUNCTION', raw='as')
    p[0].add_child(p[1])
    p[0].add_child(p[3])

def p_bucketcmd_bucketopts_bucketargs(p):
    """bucketcmd : BUCKET bucketoptlist bucketargs
                 | BIN_CMD bucketoptlist bucketargs"""
    p[0] = ParseTreeNode('COMMAND', raw='bucket')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_bucketcmd_bucketargs_bucketopts(p):
    """bucketcmd : BUCKET bucketargs bucketoptlist
                 | BIN_CMD bucketargs bucketoptlist"""
    p[0] = ParseTreeNode('COMMAND', raw='bucket')
    p[0].add_child(p[2])
    p[0].add_children(p[3].children)

def p_bucketoptlist_base(p):
    """bucketoptlist : bucketopts"""
    p[0] = ParseTreeNode('_BUCKET_OPT_LIST')
    p[0].add_child(p[1])

def p_bucketoptlist(p):
    """bucketoptlist : bucketopts bucketoptlist"""
    p[0] = ParseTreeNode('_BUCKET_OPT_LIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_bucketopts(p):
    """bucketopts : BUCKET_OPT EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    bucket_opt_node = ParseTreeNode('OPTION', raw=p[1])
    bucket_opt_node.values.append(p[3])
    p[0].add_child(bucket_opt_node)
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in bucket parser input!") 

