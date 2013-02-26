#!/usr/bin/env python

import imp
import logging
import os
import ply.yacc

from splparser.parsetree import *
from splparser.exceptions import SPLSyntaxError

from splparser.cmdparsers.common.asrules import *
from splparser.cmdparsers.common.simplefieldrules import *
from splparser.cmdparsers.common.simplevaluerules import *
from splparser.cmdparsers.common.statsfnrules import *
from splparser.cmdparsers.common.uminusrules import *
    
from splparser.cmdparsers.renamelexer import lexer, precedence, tokens

PARSETAB_DIR = 'parsetabs'
PARSETAB = 'rename_parsetab'

start = 'cmdexpr'

def p_cmdexpr_rename(p):
    """cmdexpr : renamecmd"""
    p[0] = p[1]

def p_rename_renameexprlist(p):
    """renamecmd : RENAME renameexprlist"""
    p[0] = ParseTreeNode('RENAME')
    p[0].add_children(p[2].children)

# WARNING: The order of the next two rules is important.
def p_renameexprlist_renameexpr(p):
    """renameexprlist : renameexpr"""    
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])

def p_renameexprlist_renameexprlist(p):
    """renameexprlist : renameexpr COMMA renameexprlist"""
    p[0] = ParseTreeNode('_RENAMEEXPRLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_renameexpr_simplefield(p):
    """renameexpr : simplefield as simplevalue"""
    as_node = ParseTreeNode('AS')
    as_node.add_children([p[1], p[3]])
    p[0] = as_node

def p_renameexpr_statsfnexpr(p):
    """renameexpr : statsfnexpr as simplevalue"""
    as_node = ParseTreeNode('AS')
    as_node.add_children(p[1].children)
    as_node.add_child(p[3])
    p[0] = as_node

def p_error(p):
    raise SPLSyntaxError("Syntax error in rename parser input!") 

logging.basicConfig(
    level = logging.DEBUG,
    filename = "renameparser.log",
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
