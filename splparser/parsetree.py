#!/usr/bin/env python

import json

from . import schema

from itertools import chain

INDENT = '    '

class ParseTreeNode(object):
    
    def __init__(self, role, type="SPL", raw="", is_associative=False, is_argument=False):
        """
        >>> p = ParseTreeNode('TYPE', raw="raw")
        >>> p.role
        'TYPE'
        >>> p.raw
        'raw'
        >>> p.children
        []
        >>> p.parent
        >>> p = ParseTreeNode()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: __init__() takes at least 2 is_arguments (1 given)
        """
        
        self.role = role
        self.type = type
        self.raw = raw
        self.parent = None
        self.children = []
        self.is_associative = is_associative
        self.is_argument = is_argument
        self.values = []

    def __eq__(self, other):
        if len(self.children) == 0 and len(other.children) == 0:
            eq = self._node_eq(other)
            return eq
        if (len(self.children) == 0 and not len(other.children) == 0) or \
            (not len(self.children) == 0 and len(other.children) == 0):
            return False
        return all([self_child == other_child for (self_child, other_child) in zip(self.children, other.children)])

    def _node_eq(self, other):
        return self.role == other.role and self.raw == other.raw

    def flatten(self):
        s = ""
        paren = False
        if len(self.raw) > 0:
            s = ''.join([s, self.raw])
        if len(self.children) > 0:
            if len(s) > 0 and len(''.join([c.raw for c in self.children])) > 0: 
                s = ''.join([s, '('])
                paren = True
            for c in self.children[:-1]:
                s = ''.join([s, c.flatten()])
                s = ''.join([s, ', '])
            s = ''.join([s, self.children[-1].flatten()])
            if paren:     
                s = ''.join([s, ')'])
        return s

    def is_supertree_of(self, other):
        if other is None:
            return True
        if len(self.children) >= 0 and len(other.children) == 0:
            eq = self._node_eq(other)
            return eq
        if len(self.children) == 0 and len(other.children) > 0:
            return False
        if len(self.children) < len(other.children):
            return False
        if len(self.children) > 0 and len(other.children) > 0:
            ocidx = 0
            children_eq = True
            for child in self.children:
                if ocidx >= len(other.children):
                    break
                if child._node_eq(other.children[ocidx]):
                    children_eq = children_eq and child.is_supertree_of(other.children[ocidx])
                    ocidx += 1
            if len(other.children) > ocidx + 1:
                return False
            return self._node_eq(other) and children_eq

    @staticmethod
    def from_dict(d):
        p = ParseTreeNode('')
        p.role = str(d['role'])
        p.raw = str(d['raw'])
        p.is_associative = bool(d['is_associative'])
        p.is_argument = bool(d['is_argument'])
        p.add_children([ParseTreeNode.from_dict(c) for c in d['children']])
        return p

    def template(self, drop_options=False):
        p = self.copy_tree()
        variable_number = 0
        variables = {}
        stack = []
        stack.insert(0, p)
        while len(stack) > 0:
            node = stack.pop()
            if node.role == 'FIELD':
                if not node.raw in variables:
                    variables[node.raw] = ''.join(["x", str(variable_number)])
                    variable_number += 1
                node.raw = variables[node.raw]
            new_children = []
            for c in node.children:
                if drop_options:
                    if not (c.role == 'EQ' and c.children[0].role == 'OPTION'):
                        new_children.append(c)
                else:
                    new_children.append(c)
            node.children = new_children
            for c in node.children:
                stack.insert(0, c)
        return p

    def copy_tree(self):
        children = map(lambda x: x.copy_tree(), self.children) 
        p = ParseTreeNode(self.role, type=self.type, raw=self.raw, 
                            is_associative=self.is_associative, 
                            is_argument=self.is_argument)
        p.values = self.values
        p.add_children(children)
        return p

    def skeleton(self):
        children = map(lambda x: x.skeleton(), self.children) 
        if self.is_argument:
            p = ParseTreeNode('', is_argument=True)
        else:
            p = ParseTreeNode(self.role, type=self.type, raw=self.raw, is_associative=self.is_associative) 
        p.add_children(children)
        return p

    def inverse_skeleton(self):
        children = map(lambda x: x.inverse_skeleton(), self.children) 
        if not self.is_argument:
            p = ParseTreeNode('', is_argument=False)
        else:
            p = ParseTreeNode(self.role, raw=self.raw, is_associative=self.is_associative, is_argument=True)
        p.add_children(children)
        return p

    def command_argument_tuple_list(self):
        stages = self._stage_subtrees()
        command_and_is_arguments = [stage._command_argument_tuple_from_stage() for stage in stages]
        return command_and_is_arguments

    def _stage_subtrees(self):
        if not self.role == 'ROOT':
            raise ValueError("This must be 'ROOT' node for this to work properly.\n")
        return self.children

    def _command_argument_tuple_from_stage(self):
        if not self.role == 'STAGE':
            raise ValueError("This must be 'STAGE' node for this to work properly.\n")
        command = self.children[0].skeleton()._flatten_roles_to_string()
        is_arguments = self.children[0].inverse_skeleton()._flatten_to_list()
        return (command, is_arguments)

    def _flatten_roles_to_string(self):
        flattened_children = [child._flatten_roles_to_string() for child in self.children]
        flattened_children = filter(lambda x: not x == '()', flattened_children)
        children_string = ','.join(flattened_children)
        children_string = ''.join(['(', children_string, ')'])
        if self.role == '':
            return children_string
        if children_string == '()':
            return self.role
        return ''.join([self.role, children_string])

    def _flatten_to_list(self):
        children_list = list(chain.from_iterable([child._flatten_to_list() for child in self.children]))
        if self.raw == '':
            return children_list
        field = (self.field and not self.option)
        return [(self.raw, field)] + children_list

    def add_child(self, child):
        if self.is_associative and child.raw == self.raw and len(child.children) > 0:
            self.add_children(child.children)
        else:
            self.children.append(child)
        for child in self.children:
            child.parent = self
    
    def add_children(self, children):
        """
        >>> p = ParseTreeNode('PARENT')
        >>> x = ParseTreeNode('CHILD', raw="x")
        >>> p.add_child(x)
        >>> a = ParseTreeNode('CHILD', raw="a")
        >>> b = ParseTreeNode('CHILD', raw="b")
        >>> c = ParseTreeNode('CHILD', raw="c")
        >>> x.add_children([a, b, c])
        >>> y = ParseTreeNode('CHILD', raw="y")
        >>> p.add_child(y)
        >>> p.children
        [{role: 'CHILD', raw: 'x', children: [('CHILD': 'a'), ('CHILD': 'b'), ('CHILD': 'c')], parent: ('PARENT')}, {role: 'CHILD', raw: 'y', children: [], parent: ('PARENT')}]
        >>> x.children
        [{role: 'CHILD', raw: 'a', children: [], parent: ('CHILD': 'x')}, {role: 'CHILD', raw: 'b', children: [], parent: ('CHILD': 'x')}, {role: 'CHILD', raw: 'c', children: [], parent: ('CHILD': 'x')}]
        """
        for child in children:
            self.add_child(child)
    
    def remove_child(self, child):
        self.children.remove(child)
        child.parent = None

    def remove_children(self, children):
        """
        >>> p = ParseTreeNode('PARENT')
        >>> x = ParseTreeNode('CHILD', raw="x")
        >>> p.add_child(x)
        >>> a = ParseTreeNode('CHILD', raw="a")
        >>> b = ParseTreeNode('CHILD', raw="b")
        >>> c = ParseTreeNode('CHILD', raw="c")
        >>> x.add_children([a, b, c])
        >>> y = ParseTreeNode('CHILD', raw="y")
        >>> p.add_child(y)
        >>> x.remove_children([a,b])
        >>> x.children
        [{role: 'CHILD', raw: 'c', children: [], parent: ('CHILD': 'x')}]
        >>> p.remove_child(y)
        >>> p.children
        [{role: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: ('PARENT')}]
        >>> a
        {role: 'CHILD', raw: 'a', children: [], parent: None}
        >>> y
        {role: 'CHILD', raw: 'y', children: [], parent: None}
        >>> p.remove_child(y)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "art/splparsetree.py", line 53, in remove_child
            self.children.remove(child)
        ValueError: list.remove(x): x not in list
        >>> p.add_child(x)
        >>> p.remove_child(x)
        >>> p.children
        [{role: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: None}]
        >>> p.remove_child(x)
        >>> p.children
        []
        >>> p.add_child(x)
        >>> p.add_child(x)
        >>> p.remove_children([x, x])
        >>> p
        {role: 'PARENT', raw: '', children: [], parent: None}
        >>> x
        {role: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: None}
        """
        tmp = []
        for child in self.children:
            if child in children:
               child.parent = None
            else:
                tmp.append(child)
        self.children = tmp        

    def clear_children(self):
        self.children = []

    def __repr__(self):
        """
        >>> p = ParseTreeNode('PARENT')
        >>> x = ParseTreeNode('CHILD', raw="x")
        >>> p.add_child(x)
        >>> a = ParseTreeNode('CHILD', raw="a")
        >>> b = ParseTreeNode('CHILD', raw="b")
        >>> c = ParseTreeNode('CHILD', raw="c")
        >>> x.add_children([a, b, c])
        >>> y = ParseTreeNode('CHILD', raw="y")
        >>> p.add_child(y)
        >>> p
        {role: 'PARENT', raw: '', children: [('CHILD': 'x'), ('CHILD': 'y')], parent: None}
        >>> x
        {role: 'CHILD', raw: 'x', children: [('CHILD': 'a'), ('CHILD': 'b'), ('CHILD': 'c')], parent: ('PARENT')}
        >>> a
        {role: 'CHILD', raw: 'a', children: [], parent: ('CHILD': 'x')}
        """
        child_repr = ''
        first = True
        for child in self.children:
            if not first:
                child_repr = ''.join([child_repr, ', ', str(child)])
            else:
                child_repr = str(child)
                first = False
        to_repr = ''.join(["{role: '", self.role,\
                            "', raw: '", self.raw,\
                            "', children: [", child_repr,\
                            "], parent: ", str(self.parent), "}"])
        return to_repr

    def __str__(self):
        """
        >>> p = ParseTreeNode('PARENT')
        >>> x = ParseTreeNode('CHILD', raw="x")
        >>> p.add_child(x)
        >>> a = ParseTreeNode('CHILD', raw="a")
        >>> b = ParseTreeNode('CHILD', raw="b")
        >>> c = ParseTreeNode('CHILD', raw="c")
        >>> x.add_children([a, b, c])
        >>> y = ParseTreeNode('CHILD', raw="y")
        >>> p.add_child(y)
        >>> print(p)
        ('PARENT')
        >>> print(x)
        ('CHILD': 'x')
        >>> print(a)
        ('CHILD': 'a')
        """
        to_str = ''.join(["('", self.role, "'"])
        if not self.raw == "":
            to_str = ''.join([to_str, ": '", self.raw, "'"])
        to_str = ''.join([to_str, ")"])
        return to_str

    def _str_tree(self, recursive=True, indent=1):
        to_str = str(self)
        to_str = ''.join([to_str])
        if recursive:
            for child in self.children:
                to_str = ''.join([to_str, '\n', INDENT*indent, child._str_tree(indent=indent+1)])
        return to_str

    def str_tree(self, recursive=True):
        return self._str_tree(recursive=recursive)

    def print_tree(self, recursive=True):
        """
        >>> p = ParseTreeNode('PARENT')
        >>> x = ParseTreeNode('CHILD', raw="x")
        >>> p.add_child(x)
        >>> p.print_tree()
        ('PARENT')
            ('CHILD': 'x')
        >>> a = ParseTreeNode('CHILD', raw="a")
        >>> b = ParseTreeNode('CHILD', raw="b")
        >>> c = ParseTreeNode('CHILD', raw="c")
        >>> x.add_children([a, b, c])
        >>> p.print_tree()
        ('PARENT')
            ('CHILD': 'x')
                ('CHILD': 'a')
                ('CHILD': 'b')
                ('CHILD': 'c')
        >>> y = ParseTreeNode('CHILD', raw="y")
        >>> p.add_child(y)
        >>> p.print_tree()
        ('PARENT')
            ('CHILD': 'x')
                ('CHILD': 'a')
                ('CHILD': 'b')
                ('CHILD': 'c')
            ('CHILD': 'y')
        >>> p.print_tree(recursive=False)
        ('PARENT')
        """
        print self.str_tree(recursive=recursive)

    def jsonify(self):
        encoding = {}
        encoding['role'] = self.role
        encoding['raw'] = self.raw
        encoding['is_associative'] = self.is_associative
        encoding['is_argument'] = self.is_argument
        encoding['children'] = []
        for child in self.children:
            encoding['children'].append(child.jsonify())
        return encoding

    class ParseTreeNodeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ParseTreeNode):
                return obj.jsonify()
            return json.JSONEncoder.default(self, obj)
    
    def dumps(self, **kwargs):
        return json.dumps(self, cls=self.ParseTreeNodeEncoder, **kwargs)

    def schema(self):
        field_tokens = self.extract_fields()
        fields = {}
        for field_token in field_tokens:
            if not field_token.raw in fields:
                fields[field_token.raw] = schema.Field(field_token.raw)
            field = fields[field_token.raw]
            field.values = list(set(field.values) | set([value.raw for value in field_token.values]))
        s = schema.Schema()
        s.fields = fields.values()
        
        value_tokens = self.extract_values()
        for value_token in value_tokens:
            if value_token.raw == "":
                value_token.raw = value_token.role.lower()
            present = False
            for f in s.fields:
                if value_token.raw in f.values:
                    present = True
            if not present:
                g = schema.Field("")
                g.values = [value_token.raw]
                s.fields.append(g)
        return s

    def extract_fields(self):
        stack = []
        fields = []
        stack.insert(0, self)
        while len(stack) > 0:
            node = stack.pop()
            if node.role == 'FIELD':
                fields.append(node)
            if len(node.children) > 0:
                for c in node.children:
                    stack.insert(0, c)
        return fields
    
    def extract_values(self):
        stack = []
        values = []
        stack.insert(0, self)
        while len(stack) > 0:
            node = stack.pop()
            if node.role == 'VALUE':
                values.append(node)
            if len(node.children) > 0:
                for c in node.children:
                    stack.insert(0, c)
        return values
