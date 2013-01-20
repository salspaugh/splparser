# TODO: Make a decorator for command rules.

def p_cmdexpr_search(p):
    """cmdexpr : SEARCH arglist"""
    from splparser.cmdparsers.searchparser import parse
    p[0] = parse(' '.join(p[1:]))

def p_cmdexpr_fields(p):
    """cmdexpr : FIELDS arglist"""
    from splparser.cmdparsers.fieldsparser import parse
    p[0] = parse(' '.join(p[1:]))

def p_cmdexpr_rename(p):
    """cmdexpr : RENAME arglist"""
    from splparser.cmdparsers.renameparser import parse
    p[0] = parse(' '.join(p[1:]))

