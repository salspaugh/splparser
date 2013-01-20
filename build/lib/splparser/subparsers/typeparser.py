#!/urs/bin/env python

from splparser.parsetree import *

#def p_email_local(p):
#    """email_local : domain
#                   | LITERAL
#                   | NBSTR"""
#    p[0] = p[1]
#
#def p_email(p):
#    """email : email_local AT hostname
#             | email_local AT LBRACKET IPV4ADDR RBRACKET
#             | email_local AT LBRACKET IPV6ADDR RBRACKET"""
#    r = ""
#    for pthing in p[1:]:
#        if isinstance(pthing, ParseTreeNode):
#            r = "".join([r, pthing.raw])
#        else:
#            r = "".join([r, pthing])
#    p[0] = ParseTreeNode('EMAIL', raw=r)

def p_connector(p): # HACK
    """connector : PLUS
                 | MINUS
                 | COLON"""
    try:
        p[0] = p[1].raw
    except:
        p[0] = p[1]

def p_wordid_word(p):
    """wordid : WORD"""
    p[0] = ParseTreeNode('WORD', raw=p[1])

def p_wordid_id(p):
    """wordid : ID"""
    p[0] = ParseTreeNode('ID', raw=p[1])

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

# TODO: OBSOLETE? Now lexes to nbstr.
#def p_timestamp(p):
#    """timestamp : num SLASH num SLASH num COLON num COLON num COLON num
#                 | num SLASH num SLASH num COLON ID"""
#    r = ''
#    for item in p[1:]:
#        try:
#            r = ''.join([r, item.raw])
#        except:
#            r = ''.join([r, item])
#    p[0] = ParseTreeNode('TIMESTAMP', raw=r)

def p_hostname(p):
    """hostname : wordid PERIOD wordid
                | wordid PERIOD id
                | id PERIOD wordid
                | id PERIOD id"""
    r = ".".join([p[1].raw, p[3].raw])
    p[0] = ParseTreeNode('HOSTNAME', raw=r)

def p_hostname_wordid(p):
    """hostname : hostname PERIOD wordid
                | hostname PERIOD id"""
    r = ".".join([p[1].raw, p[3].raw])
    p[0] = ParseTreeNode('HOSTNAME', raw=r)

#def p_url(p):
#    pass
#
#def p_path(p):
#    pass
