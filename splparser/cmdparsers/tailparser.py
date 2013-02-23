#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.taillexer import lexer, tokens

PARSETAB_DIR = 'parsetabs'
PARSETAB = 'tail_parsetab'

start = 'cmdexpr'

def p_cmdexpr_tail(p):
    """cmdexpr : tailcmd"""
    p[0] = p[1]

def p_tailcmd_tail(p):
    """tailcmd : TAIL"""
    p[0] = ParseTreeNode('TAIL')

def p_tailcmd_tail_int(p):
    """tailcmd : TAIL INT"""
    p[0] = ParseTreeNode('TAIL')
    int_node = ParseTreeNode('INT', raw=p[2])
    p[0].add_child(int_node)

def p_error(p):
    raise SPLSyntaxError("Syntax error in tail parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "tailparser.log",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)

log = logging.getLogger()

def parse(data, ldebug=False, ldebuglog=log, pdebug=False, pdebuglog=log):
    here = os.path.dirname(__file__)
    path_to_parsetab = os.path.join(here, PARSETAB_DIR, PARSETAB + '.py')
    
    try:
        parsetab = imp.load_source(PARSETAB, path_to_parsetab)
    except IOError: # parsetab files don't exist in our installation
        parsetab = PARSETAB

    try:
        os.stat(PARSETAB_DIR)
    except:
        try:
            os.makedirs(PARSETAB_DIR)
        except OSError:
            sys.stderr.write("ERROR: Need permission to write to ./" + PARSETAB_DIR + "\n")
            raise

    parser= ply.yacc.yacc(debug=pdebug, debuglog=pdebuglog, tabmodule=parsetab, outputdir=PARSETAB_DIR)
    return parser.parse(data, debug=pdebuglog, lexer=lexer)

if __name__ == "__main__":
    import sys
    lexer = ply.lex.lex()
    parser = ply.yacc.yacc()
    print parser.parse(sys.argv[1:], debug=log, lexer=lexer)
