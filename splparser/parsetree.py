#!/usr/bin/env python

import json

INDENT = '    '

class ParseTreeNode(object):
    
    def __init__(self, type, raw="", associative=False):
        """
        >>> p = ParseTreeNode('TYPE', raw="raw")
        >>> p.type
        'TYPE'
        >>> p.raw
        'raw'
        >>> p.children
        []
        >>> p.parent
        >>> p = ParseTreeNode()
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        TypeError: __init__() takes at least 2 arguments (1 given)
        """
        self.type = type
        self.raw = raw
        self.parent = None
        self.children = []
        self.label = self.type.lower()
        #if not raw == '':
        #    self.label = self.type
        self.associative = associative

    def add_child(self, child):
        if self.associative and child.type == self.type and len(child.children) > 0:
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
        [{type: 'CHILD', raw: 'x', children: [('CHILD': 'a'), ('CHILD': 'b'), ('CHILD': 'c')], parent: ('PARENT')}, {type: 'CHILD', raw: 'y', children: [], parent: ('PARENT')}]
        >>> x.children
        [{type: 'CHILD', raw: 'a', children: [], parent: ('CHILD': 'x')}, {type: 'CHILD', raw: 'b', children: [], parent: ('CHILD': 'x')}, {type: 'CHILD', raw: 'c', children: [], parent: ('CHILD': 'x')}]
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
        [{type: 'CHILD', raw: 'c', children: [], parent: ('CHILD': 'x')}]
        >>> p.remove_child(y)
        >>> p.children
        [{type: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: ('PARENT')}]
        >>> a
        {type: 'CHILD', raw: 'a', children: [], parent: None}
        >>> y
        {type: 'CHILD', raw: 'y', children: [], parent: None}
        >>> p.remove_child(y)
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
          File "art/splparsetree.py", line 53, in remove_child
            self.children.remove(child)
        ValueError: list.remove(x): x not in list
        >>> p.add_child(x)
        >>> p.remove_child(x)
        >>> p.children
        [{type: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: None}]
        >>> p.remove_child(x)
        >>> p.children
        []
        >>> p.add_child(x)
        >>> p.add_child(x)
        >>> p.remove_children([x, x])
        >>> p
        {type: 'PARENT', raw: '', children: [], parent: None}
        >>> x
        {type: 'CHILD', raw: 'x', children: [('CHILD': 'c')], parent: None}
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
        {type: 'PARENT', raw: '', children: [('CHILD': 'x'), ('CHILD': 'y')], parent: None}
        >>> x
        {type: 'CHILD', raw: 'x', children: [('CHILD': 'a'), ('CHILD': 'b'), ('CHILD': 'c')], parent: ('PARENT')}
        >>> a
        {type: 'CHILD', raw: 'a', children: [], parent: ('CHILD': 'x')}
        """
        child_repr = ''
        first = True
        for child in self.children:
            if not first:
                child_repr = ''.join([child_repr, ', ', str(child)])
            else:
                child_repr = str(child)
                first = False
        to_repr = ''.join(["{type: '", self.type,\
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
        to_str = ''.join(["('", self.type, "'"])
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
        encoding = {'node': (self.type) if self.raw == '' else (self.type, self.raw)}
        if len(self.children) > 0:
            encoding['children'] = []
        for child in self.children:
            encoding['children'].append(child.jsonify())
        return encoding

    class ParseTreeNodeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ParseTreeNode):
                return obj.jsonify()
            return json.JSONEncoder.default(self, obj)
    
    def dumps(self):
        return json.dumps(self, cls=self.ParseTreeNodeEncoder)
