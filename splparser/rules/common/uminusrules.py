
from splparser.parsetree import *

def p_negint(p):
    """int : MINUS int %prec UMINUS"""
    p[0] = ParseTreeNode(role='VALUE', nodetype='INT', raw=''.join([p[1], p[2].raw]), is_argument=True)

