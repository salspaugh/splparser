# TODO: Make a decorator for command rules.
# TODO: Better error handling.

from splparser.exceptions import SPLSyntaxError, TerminatingSPLSyntaxError
import splparser.parser

def p_cmdexpr_search(p):
    """cmdexpr : SEARCH arglist"""
    from splparser.cmdparsers.searchparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist"""
    from splparser.cmdparsers.evalparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except Exception as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message) 

def p_cmdexpr_stats(p):
    """cmdexpr : STATS arglist"""
    from splparser.cmdparsers.statsparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS
               | FIELDS arglist"""
    from splparser.cmdparsers.fieldsparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist"""
    from splparser.cmdparsers.renameparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_table(p):
    """cmdexpr : TABLE arglist"""
    from splparser.cmdparsers.tableparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_top(p):
    """cmdexpr : TOP arglist"""
    from splparser.cmdparsers.topparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist"""
    from splparser.cmdparsers.headparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_tail(p):
    """cmdexpr : TAIL arglist"""
    from splparser.cmdparsers.tailparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_reverse(p):
    """cmdexpr : REVERSE"""
    from splparser.cmdparsers.reverseparser import parse as cmdparse
    try:
        p[0]  = cmdparse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        raise TerminatingSPLSyntaxError(e.message)

def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist"""
    from splparser.cmdparsers.chartparser import parse as cmdparse
    p[0]  = cmdparse(' '.join(p[1:]))
