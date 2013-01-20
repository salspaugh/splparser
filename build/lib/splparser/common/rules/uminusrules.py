
def p_negint(p):
    """int : MINUS int %prec UMINUS"""
    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

