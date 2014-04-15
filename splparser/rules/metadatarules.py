#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.fieldrules import *
from splparser.rules.common.valuerules import *

from splparser.lexers.metadatalexer import tokens

start = 'cmdexpr'

def p_cmdexpr(p):
    """cmdexpr : metadatacmd"""
    p[0] = p[1]

def p_cmdexpr_metadata(p):
    """metadatacmd : METADATA metadataarglist"""
    p[0] = ParseTreeNode('COMMAND', raw='metadata')
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_metadataarglist_metadataargs(p):
    """metadataarglist : metadataarg
                       | metadataarg metadataarglist"""
    p[0] = ParseTreeNode('_METADATAARGLIST')
    p[0].add_child(p[1])
    if len(p) > 2:
        p[0].add_children(p[2].children)

def p_metadataarg_eq(p):
    """metadataarg : field EQ value"""
    p[0] = ParseTreeNode('EQ', raw='assign')
    p[1].values.append(p[3])
    p[0].add_children([p[1], p[3]])

def p_field_search_opt(p):
    """field : METADATA_OPT"""
    p[0] = ParseTreeNode('OPTION', raw=p[1])

def p_error(p):
    raise SPLSyntaxError("Syntax error in metadata parser input!")
