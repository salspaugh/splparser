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
    """bucketcmd : BUCKET bucketargs"""
    p[0] = ParseTreeNode('BUCKET')
    p[0].add_child(p[2])

def p_bucketargs(p):
    """bucketargs : field"""
    p[0] = p[1]

def p_bucketargs_as(p):
    """bucketargs : field as field"""
    p[0] = p[1]
    as_node = ParseTreeNode('as')
    p[0].add_child(as_node)
    as_node.add_child(p[3])

def p_bucketcmd_bucketopts_bucketargs(p):
    """bucketcmd : BUCKET bucketoptlist bucketargs"""
    p[0] = ParseTreeNode('BUCKET')
    p[0].add_children(p[2].children)
    p[0].add_child(p[3])

def p_bucketcmd_bucketargs_bucketopts(p):
    """bucketcmd : BUCKET bucketargs bucketoptlist"""
    p[0] = ParseTreeNode('BUCKET')
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
    p[0] = ParseTreeNode('EQ')
    bucket_opt_node = ParseTreeNode(p[1].upper())
    p[0].add_child(bucket_opt_node)
    p[0].add_child(p[3])

def p_error(p):
    raise SPLSyntaxError("Syntax error in bucket parser input!") 

