#!/urs/bin/env python

from splparser.parsetree import *

def p_delimiter_comma(p):
    """delimiter : COMMA"""
    p[0] = ParseTreeNode('COMMA')

# TODO: Make other delimiters like tabs work.

# WARNING: The order of the next two rules is important.
def p_fieldlist_field(p):
    """fieldlist : field"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])

def p_fieldlist_comma(p):
    """fieldlist : field COMMA fieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[3].children)

def p_fieldlist_space(p):
    """fieldlist : field fieldlist"""
    p[0] = ParseTreeNode('_FIELDLIST')
    p[0].add_child(p[1])
    p[0].add_children(p[2].children)

def p_field_literal(p):
    """field : LITERAL"""
    p[0] = ParseTreeNode('LITERAL', raw=p[1])

#def p_field_timestamp(p):
#    """field : timestamp"""
#    p[0] = p[1]

def p_field_word(p):
    """field : wordid"""
    p[0] = p[1]

def p_field_times(p):
    """field : connector"""
    if p[1] == '*':
        p[0] = ParseTreeNode('WILDCARD')
    else:
        p[0] = p[1]

def p_field_email(p):
    """field : EMAIL"""
    p[0] = ParseTreeNode('EMAIL', raw=p[1])

def p_field_id(p):
    """field : id"""
    p[0] = p[1]

# TODO: Make sure keys can actually be nbstr or if they must be IDs.
def p_field_nbstr(p):
    """field : NBSTR"""
    p[0] = ParseTreeNode('NBSTR', raw=p[1])

## TODO: Think about if other key values can be field names too ...
def p_field_host(p):
    """field : HOST"""
    p[0] = ParseTreeNode('HOST')

# TODO: EVAL_FN can probably be field names too.
def p_field_stats_fn(p):
    """field : STATS_FN""" # HACK 
    p[0] = ParseTreeNode('WORD', raw=p[1])

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

def p_field_num(p):
    """field : num"""
    p[0] = p[1]

def p_num_bin(p):
    """num : BIN"""
    p[0] = ParseTreeNode('BIN', raw=p[1])

def p_num_oct(p):
    """num : OCT"""
    p[0] = ParseTreeNode('OCT', raw=p[1])

def p_num_hex(p):
    """num : HEX"""
    p[0] = ParseTreeNode('HEX', raw=p[1])

#def p_num_int(p):
#    """num : INT"""
#    p[0] = ParseTreeNode('INT', raw=p[1])

def p_num_int(p):
    """num : int"""
    p[0] = p[1]

#def p_negint(p):
#    """int : UMINUS int"""
#    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

def p_negint(p):
    """int : MINUS int %prec UMINUS"""
    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

#def p_negint(p):
#    """int : MINUS int"""
#    p[0] = ParseTreeNode('INT', raw=''.join([p[1], p[2].raw]))

def p_posint(p):
    """int : INT"""
    p[0] = ParseTreeNode('INT', raw=p[1])

def p_num_float(p):
    """num : FLOAT"""
    p[0] = ParseTreeNode('FLOAT', raw=p[1])
