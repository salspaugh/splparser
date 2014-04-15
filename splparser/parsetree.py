
import json

from . import schema
from collections import defaultdict
from itertools import chain, count

INDENT = '    '

DATATYPES = {
    "INT": "NUMERIC",
    "FLOAT": "NUMERIC",
    "BIN": "NUMERIC",
    "OCT": "NUMERIC",
    "INT": "NUMERIC",
    "ID": "STRING",
    "WORD": "STRING",
    "NBSTR": "STRING",
    "BOOLEAN": "BOOLEAN"
}

class ParseTreeNode(object):
    
    def __init__(self, role, nodetype="SPL", raw="", is_associative=False, is_argument=False):
        """
        >>> p = ParseTreeNode('TYPE', raw="raw")
        >>> p.role
        'TYPE'
        >>> p.raw
        'raw'
        >>> p.children
        []
        >>> p.parent
        """
        # TODO: Use property decorator for the three strings here.
        self.role = str(role.encode("utf8")) if type(role) == unicode else str(role.decode("utf8").encode("utf8"))
        self.nodetype = str(nodetype.encode("utf8")) if type(nodetype) == unicode else str(nodetype.decode("utf8").encode("utf8"))
        self.raw = str(raw.encode("utf8")) if type(raw) == unicode else str(raw.decode("utf8").encode("utf8"))
        self.parent = None
        self.children = []
        self.is_associative = is_associative
        self.is_argument = is_argument
        self.values = []
        self.corrected = False
        self.bound = False
        self.datatype = None

    def jsonify(self):
        encoding = {}
        encoding['role'] = self.role
        encoding['nodetype'] = self.nodetype
        encoding['raw'] = self.raw
        encoding['is_associative'] = self.is_associative
        encoding['is_argument'] = self.is_argument
        encoding['values'] = self.values
        encoding['corrected'] = self.corrected
        encoding['bound'] = self.bound
        encoding['datatype'] = self.datatype
        encoding['children'] = []
        for child in self.children:
            encoding['children'].append(child.jsonify())
        return encoding
    
    @staticmethod
    def from_dict(d):
        p = ParseTreeNode('')
        role = d['role']
        nodetype = d.get('nodetype', None)
        if nodetype is None:
            nodetype = d.get('type', None) # assbackward-compatability
        raw = d['raw']
        p = ParseTreeNode(role, raw=raw, nodetype=nodetype)
        p.is_associative = bool(d['is_associative'])
        p.is_argument = bool(d['is_argument'])
        p.values = d['values']
        p.corrected = bool(d['corrected'])
        p.bound = bool(d['bound'])
        p.datatype = d['datatype']
        p.add_children([ParseTreeNode.from_dict(c) for c in d['children']])
        return p

    @staticmethod
    def loads(jsonstr):
        return ParseTreeNode.from_dict(json.loads(jsonstr))

    class ParseTreeNodeEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, ParseTreeNode):
                return obj.jsonify()
            return json.JSONEncoder.default(self, obj)
    
    def dumps(self, **kwargs):
        return json.dumps(self, cls=self.ParseTreeNodeEncoder, **kwargs)

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
        if len(str(self.raw)) > 0:
            s = ''.join([s, str(self.raw)])
        if len(self.children) > 0:
            if len(s) > 0 and len(''.join([str(c.raw) for c in self.children])) > 0: 
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

    def template(self, drop_options=False, drop_rename=False, distinguished_argument=None):
        p = self.copy_tree()
        keynum = 0
        valnum = 0
        keyvars = {}
        valvars = {}
        stack = []
        stack.insert(0, p)
        while len(stack) > 0:
            node = stack.pop(0)
            if distinguished_argument and node.raw == distinguished_argument:
                node.raw = "x"
            elif node.role.find('FIELD') > -1:
                if not node.raw in keyvars:
                    keyvars[node.raw] = ''.join(["k", str(keynum)])
                    keynum += 1
                node.raw = keyvars[node.raw]
            elif node.nodetype != 'SPL':
                if not node.raw in valvars:
                    valvars[node.raw] = ''.join(["v", str(valnum)])
                    valnum += 1
                node.raw = valvars[node.raw]
            new_children = []
            for c in node.children:
                if drop_options and not drop_rename:
                    if not (c.role == 'EQ' and c.children[0].role == 'OPTION'):
                        new_children.append(c)
                elif drop_rename and not drop_options:
                    if c.raw == 'as' and c.role == 'FUNCTION':
                        new_children.append(c.children[0])
                    else:
                        new_children.append(c)
                elif drop_options and drop_rename:
                    if not (c.role == 'EQ' and c.children[0].role == 'OPTION') and not c.raw == 'rename':
                        new_children.append(c)
                    elif c.raw == 'as' and c.role == 'FUNCTION': 
                        new_children.append(c.children[0])
                    else:
                        new_children.append(c)
                else:
                    new_children.append(c)
            node.children = []
            node.add_children(new_children)
            for c in node.children:
                stack.insert(0, c)
        return p

    def get_parent_stage(self):
        node = self
        while node:
            if node.role == 'STAGE':
                return node
            node = node.parent
        return None # TODO: Throw error here?

    def drop_options(self):
        p = self.copy_tree()
        stack = []
        stack.insert(0, p)
        while len(stack) > 0:
            node = stack.pop(0)
            if node.role == 'EQ' and node.children[0].role == 'OPTION' or node.role == 'OPTION':
                return None
            new_children = []
            for c in node.children:
                if not (c.role == 'EQ' and c.children[0].role == 'OPTION'):
                    new_children.append(c)
            node.children = []
            node.add_children(new_children)
            for c in node.children:
                stack.insert(0, c)
        return p

    def drop_rename(self):
        p = self.copy_tree()
        stack = []
        stack.insert(0, p)
        while len(stack) > 0:
            node = stack.pop(0)
            if node.role == 'FUNCTION' and node.raw == 'as':
                return None
            new_children = []
            for c in node.children:
                if c.raw == 'as' and c.role == 'FUNCTION': 
                    new_children.append(c.children[0])
                else:
                    new_children.append(c)
            node.children = []
            node.add_children(new_children)
            for c in node.children:
                stack.insert(0, c)
        return p

    def descendant_arguments(self):
        descendants = []
        stack = []
        stack.insert(0, self)
        while len(stack) > 0:
            node = stack.pop(0)
            if node.is_argument:
                descendants.append(node)
            for c in node.children:
                stack.insert(0, c)
        return descendants

    def ast(self):
        p = self.copy_tree()
        p = p.drop_options()
        outerstack = []
        outerstack.insert(0, p)
        corrected = False
        while not corrected:
            groupby = None
            while len(outerstack) > 0:
                node = outerstack.pop(0)
                if node.is_groupby() and not node.corrected:
                    groupby = node
                outerstack = node.children + outerstack
            if not groupby:
                corrected = True
            else:
                stage = groupby.get_parent_stage()
                groupby.parent.children.remove(groupby)
                groupby.parent.add_children(filter(lambda x: x.role.find('GROUPING') == -1, groupby.children))
                groupby.parent = None
                innerstack = []
                innerstack.insert(0, stage)
                while len(innerstack) > 0:
                    node = innerstack.pop(0)
                    if node.is_eval_function() or (node.is_argument and node.parent.raw != 'as'):
                        g = ParseTreeNode('FUNCTION', raw='groupby')
                        g.corrected = True
                        node.parent.swap_children(node, g)
                        g.add_child(node)
                        for c in filter(lambda x: x.role.find('GROUPING') > -1, groupby.children):
                            d = c.copy_tree()
                            g.add_child(d) 
                    else:
                        innerstack = node.children + innerstack
        return p

    def compile(self):
        p = self.copy_tree()
        p = p.drop_options() # TODO: Incorporate these.
        p = p.ast()
        exl = {}
        bound = {}
        var = count()
        stages = p._stage_subtrees()
        for stage in stages:
            keepgoing = True
            while keepgoing:
                stack = []
                stack.insert(0, stage)
                while len(stack) > 0:
                    node = stack.pop(0)
                    if not node.exl and all([c.exl for c in node.children]):
                        if not node.parent:
                            keepgoing = False
                            break
                        #key = ''.join(['X', str(var.next())])
                        key = var.next()
                        new = ParseTreeNode('VAR', raw=key)
                        new.exl = True
                        node.parent.swap_children(node, new)
                        exl[key] = node.copy_tree()       
                    else:
                        stack = node.children + stack
        return exl 

    def swap_children(self, p, q):
        idx = self.children.index(p)
        self.children.remove(p)
        p.parent = None
        self.children.insert(idx, q)
        q.parent = self

    def is_eval_function(self):
        return (self.is_function() and self.raw == 'eval')

    def is_groupby(self):
        return (self.is_function() and self.raw == 'groupby')

    def is_function(self):
        return self.role == 'FUNCTION'

    def decompose(self):
        if self.role == 'COMMAND' or self.role == 'FUNCTION':
            for c in self.children:
                if (c.role == 'COMMAND' or c.role == 'FUNCTION'):
                    pass                  


    def copy_node(self):
        p = ParseTreeNode(self.role, nodetype=self.nodetype, raw=self.raw, 
                            is_associative=self.is_associative, 
                            is_argument=self.is_argument)
        p.corrected = self.corrected
        p.bound = self.bound
        return p
    
    def copy_tree(self):
        children = map(lambda x: x.copy_tree(), self.children) 
        p = self.copy_node()
        p.values = self.values
        p.add_children(children)
        return p

    def ancestral_branch(self):
        children = map(lambda x: x.copy_tree(), self.children) 
        p = self.copy_node()
        p.values = self.values
        p.add_children(children)
        top = self.parent
        bottom = p
        while top:
            t = top.copy_node()
            t.add_child(bottom)
            top = top.parent 
            bottom = t
        return t

    def ancestral_command(self):
        up = self.parent
        while up:
            if up.role == 'COMMAND':
                return up
            up = up.parent
        return None

    def ancestral_function(self):
        up = self.parent
        while up:
            if up.role == 'FUNCTION' or up.role == 'COMMAND':
                return up
            up = up.parent
        return None
        

    def skeleton(self):
        children = map(lambda x: x.skeleton(), self.children) 
        if self.is_argument:
            p = ParseTreeNode('', is_argument=True)
        else:
            p = ParseTreeNode(self.role, nodetype=self.nodetype, raw=self.raw, is_associative=self.is_associative) 
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
        raw = self.raw
        to_str = ''.join(["('", self.role, "'"])
        if not raw == "":
            to_str = ''.join([to_str, ": '", raw, "'"])
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

    def itertree(self):
        stack = [self]
        while len(stack) > 0:
            node = stack.pop(0)
            stack = node.children + stack
            yield node

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

    def get_datatype(self):
        if self.datatype:
            return self.datatype
        if not self.role.find('FIELD') > -1:
            return self.nodetype
        d = defaultdict(int)
        for v in self.values:
            d[v.nodetype] += 1
        if len(d) == 0:
            return None
        vote = max(d)
        return DATATYPES.get(vote, vote)

    def extract_fields(self):
        stack = []
        fields = []
        stack.insert(0, self)
        while len(stack) > 0:
            node = stack.pop(0)
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
            node = stack.pop(0)
            if node.role == 'VALUE':
                values.append(node)
            if len(node.children) > 0:
                for c in node.children:
                    stack.insert(0, c)
        return values
