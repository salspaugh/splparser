# TODO: Make a decorator for command rules.
# TODO: Better error handling.

from splparser.exceptions import SPLSyntaxError

def p_cmdexpr_search(p):
    """cmdexpr : SEARCH arglist"""
    from splparser.cmdparsers.searchparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_eval(p):
    """cmdexpr : EVAL arglist"""
    from splparser.cmdparsers.evalparser import parse
    p[0] = parse(' '.join(p[1:]))

def p_cmdexpr_stats(p):
    """cmdexpr : STATS arglist"""
    from splparser.cmdparsers.statsparser import parse
    p[0] = parse(' '.join(p[1:]))

def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS arglist"""
    from splparser.cmdparsers.fieldsparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist"""
    from splparser.cmdparsers.renameparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_table(p):
    """cmdexpr : TABLE arglist"""
    from splparser.cmdparsers.tableparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_top(p):
    """cmdexpr : TOP arglist"""
    from splparser.cmdparsers.topparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_head(p):
    """cmdexpr : HEAD arglist"""
    from splparser.cmdparsers.headparser import parse
    p[0] = parse(' '.join(p[1:]))

def p_cmdexpr_tail(p):
    """cmdexpr : TAIL arglist"""
    from splparser.cmdparsers.tailparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_reverse(p):
    """cmdexpr : REVERSE"""
    from splparser.cmdparsers.reverseparser import parse
    try:
        p[0] = parse(' '.join(p[1:]))
    except SPLSyntaxError as e:
        print e.message
        exit()

def p_cmdexpr_chart(p):
    """cmdexpr : CHART arglist"""
    from splparser.cmdparsers.chartparser import parse
    p[0] = parse(' '.join(p[1:]))
