
from splparser.parsetree import *

def p_as_lc(p):
    """as : ASLC"""
    p[0] = p[1]

def p_as_uc(p):
    """as : ASUC"""
    p[0] = p[1]

def p_by_lc(p):
    """by : BYLC"""
    p[0] = p[1]

def p_by_uc(p):
    """by : BYUC"""
    p[0] = p[1]
