
from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
from splparser.decorators import *

@splcommandrule
def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist"""

@splcommandrule
def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS
               | FIELDS arglist"""

@splcommandrule
def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist"""

@splcommandrule
def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist"""

@splcommandrule
def p_cmdexpr_reverse(p):
    """cmdexpr : REVERSE"""

@splcommandrule
def p_cmdexpr_search(p):
    """cmdexpr : SEARCH arglist"""

@splcommandrule
def p_cmdexpr_stats(p):
    """cmdexpr : STATS arglist"""

@splcommandrule
def p_cmdexpr_table(p):
    """cmdexpr : TABLE arglist"""

@splcommandrule
def p_cmdexpr_tail(p):
    """cmdexpr : TAIL arglist"""

@splcommandrule
def p_cmdexpr_top(p):
    """cmdexpr : TOP arglist"""

@notimplemented
def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist"""
