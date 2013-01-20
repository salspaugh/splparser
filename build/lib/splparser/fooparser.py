#!/usr/bin/env python

import ply.yacc
import logging

from splparser.parsetree import *
from splparser.lexer import *

precedence = (
    ('nonassoc', 'NE' ,'LT', 'LE', 'GE', 'GT'),
    ('left', 'OR'),
    ('left', 'AND', 'COMMA'),
    ('right', 'EQ', 'DCOLON'),
    ('left', 'PLUS', 'MINUS'), 
#    ('left', 'PLUS'), 
#    ('right', 'MINUS'), 
    ('left', 'TIMES', 'DIVIDES'), 
    ('right', 'NOT'),
    ('right', 'UMINUS'),
#    ('left', 'UMINUS'),
#    ('right', 'LPAREN'),
#    ('left', 'RPAREN'),
)

start = 'start' 

def p_start(p):
    """start : num"""
    p[0] = p[1]

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

def p_negint(p):
    """int : MINUS int %prec UMINUS"""
    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

#def p_negint(p):
#    """int : MINUS int"""
#    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1])

def p_error(p):
    #print "Syntax error in input!"
    raise SPLSyntaxError("Syntax error in input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "splparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    
    lexer = ply.lex.lex(debug=ldebug, debuglog=ldebuglog)
    parser = ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog)
    # TODO: check that it works to use the same log for runtime
    
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":

    import sys
 
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
                
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
