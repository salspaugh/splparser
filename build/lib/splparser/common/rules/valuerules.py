def p_value_times(p):
    """value : field"""
    p[0] = p[1]

#def p_value_email(p):
#    """value : email"""
#    p[0] = p[1]

def p_value_hostname(p):
    """value : hostname"""
    p[0] = p[1]

#def p_value_url(p):
#    """value : url"""
#    p[0] = p[1]

def p_value_ipv6addr(p):
    """value : IPV6ADDR"""
    p[0] = ParseTreeNode('IPV6ADDR', raw=p[1])

def p_value_ipv4addr(p):
    """value : IPV4ADDR"""
    p[0] = ParseTreeNode('IPV4ADDR', raw=p[1])

#def p_value_path(p):
#    """value : path"""
#    p[0] = p[1]
