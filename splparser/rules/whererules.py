#!/usr/bin/env python

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.rules.common.evalfnexprrules import *
from splparser.rules.common.simplefieldrules import *

from splparser.lexers.wherelexer import precedence, tokens

start = 'cmdexpr'

def update_eq_nodes(p):
    stack = []
    stack.insert(0, p)
    while len(stack) > 0:
        node = stack.pop()
        if node.role == 'EQ':
            node.role = 'FUNCTION'
            node.raw = 'eq'
        for c in node.children:
            stack.insert(0, c)

def p_cmdexpr_where(p):
    """cmdexpr : wherecmd"""
    p[0] = p[1]

def p_where_whereexpr(p):
    """wherecmd : WHERE oplist"""
    p[0] = ParseTreeNode('COMMAND', raw='where')
    update_eq_nodes(p[2]) 
    p[0].add_children(p[2].children)

def p_error(p):
    raise SPLSyntaxError("Syntax error in where parser input!") 
