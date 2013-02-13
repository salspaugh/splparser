#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.evalfnexprrules import *
from splparser.cmdparsers.common.fieldrules import *
from splparser.cmdparsers.common.simplevaluerules import *

from splparser.cmdparsers.evallexer import lexer, precedence, tokens

start = 'cmdexpr'

def p_cmdexpr_eval(p):
    """cmdexpr : evalcmd"""
    p[0] = p[1]

def p_eval_evalexpr(p):
    """evalcmd : EVAL evalexpr"""
    p[0] = ParseTreeNode('EVAL')
    p[0].add_child(p[2])

def p_evalexpr(p):
    """evalexpr : field eqevalfnexpr"""
    p[0] = ParseTreeNode('EVALEXPR')
    p[0].add_child(p[1])
    p[0].add_child(p[2])

def p_evalfnexpr_oplist(p):
    """evalexpr : oplist"""
    p[0] = ParseTreeNode('EVALEXPR')
    p[0].add_children(p[1].children)

def p_eqevalfnexpr(p):
    """eqevalfnexpr : EQ evalfnexpr"""
    p[0] = p[2]

def p_eqevalfnexpr_field(p):
    """eqevalfnexpr : EQ field"""
    p[0] = p[2]

def p_eqevalfnexpr_opexpr(p):
    """eqevalfnexpr : EQ opexpr"""
    p[0] = p[2]


def p_error(p):
    raise SPLSyntaxError("Syntax error in eval parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "evalparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule="eval_parsetab")
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
