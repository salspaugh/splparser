
def p_field_id(p):
    """field : id"""
    p[0] = p[1]

def p_field_times(p):
    """field : connector"""
    if p[1] == '*':
        p[0] = ParseTreeNode('WILDCARD')
    else:
        p[0] = p[1]


def p_connector(p): # HACK
    """connector : PLUS
                 | MINUS
                 | COLON"""
    try:
        p[0] = p[1].raw
    except:
        p[0] = p[1]


def p_id(p): # HACK
    """id : connector wordid
          | wordid connector
          | wordid connector wordid
          | wordid connector id
          | id connector wordid
          | id connector id"""
    r = ''
    for item in p[1:]:
        try:
            r = ''.join([r, item.raw])
        except:
            r = ''.join([r, item])
    p[0] = ParseTreeNode('ID', raw=r)
