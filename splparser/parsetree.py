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
    """A node in a parse tree representing a single parsed element.

    The parse function in splparser returns a ParseTreeNode representing the root node of a parse tree.
    """

    # TODO: Reorder functions in this module to be in logical groupings.

    def __init__(self, role, nodetype="SPL", raw="", is_associative=False, is_argument=False):
        """The constructor for ParseTreeNode

        :param self: The current object
        :type self: ParseTreeNode
        :param role: The 'type' of node represented; e.g., ROOT, STAGE, COMMAND, FUNCTION, FIELD
        :type role: str
        :param nodetype: The data type of the node value; only applies to FIELD and VALUE roles
        :type nodetype: str
        :param raw: The value of the parsed element
        :type raw: str
        :param is_associative: Whether the node value is an associative operator; only applies to FUNCTION roles
        :type is_associative: bool
        :param is_argument: Whether the node value is an argument versus part of the SPL language
        :type is_argument: bool
        :rtype: ParseTreeNode

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
        """Recursively convert the ParseTreeNode to types directly convertible to JSON.

        This function creates a dict that stores all of the attributes of the given
        ParseTreeNode as dict, list, str, int, etc. types. It recursively 
        performs this operation on the children ParseTreeNode objects.

        This is the inverse function of the function from_dict.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: dict
        """
        encoding = {}
        encoding['role'] = self.role
        encoding['nodetype'] = self.nodetype
        encoding['raw'] = self.raw
        encoding['is_associative'] = self.is_associative
        encoding['is_argument'] = self.is_argument
        encoding['values'] = []
        for value in self.values:
            encoding['values'].append(value.jsonify())
        encoding['corrected'] = self.corrected
        encoding['bound'] = self.bound
        encoding['datatype'] = self.datatype
        encoding['children'] = []
        for child in self.children:
            encoding['children'].append(child.jsonify())
        return encoding
    
    @staticmethod
    def from_dict(d):
        """Recursively convert a dict representing a ParseTreeNode to a ParseTreeNode.

        This function creates a ParseTreeNode from a dict whose contents are the
        attributes and values of the object. It recursively performs this operation
        on the "children" key.

        This is the inverse function of the function jsonify.

        :param d: A dictionary that corresponds to a ParseTreeNode object
        :type d: dict
        :rtype: ParseTreeNode
        """
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
        # TODO: Add code to make sure all keys are set as attributes.
        return p

    @staticmethod
    def loads(jsonstr):
        """Convert a JSON string that corresponds to a ParseTreeNode to a ParseTreeNode.

        This converts a str object to a ParseTreeNode if it represents a valid
        ParseTreeNode.

        :param jsonstr: A string that encodes a ParseTreeNode in JSON format
        :type jsonstr: str
        :rtype: ParseTreeNode
        """
        return ParseTreeNode.from_dict(json.loads(jsonstr))

    class ParseTreeNodeEncoder(json.JSONEncoder):
        """An object that knows how to decode a JSON string representing a ParseTreeNode.

        This needs to be passed to the json module load or loads functions to
        tell it how to decode a ParseTreeNode object.
        """
        def default(self, obj):
            """Method that must be implemented to decode the JSON string.
            """
            if isinstance(obj, ParseTreeNode):
                return obj.jsonify()
            return json.JSONEncoder.default(self, obj)
    
    def dumps(self, **kwargs):
        """Convert the current object to a JSON-encoded string.
        
        :param self: The current object
        :type self: ParseTreeNode
        :param kwargs: Keyword arguments that are passed to json.dumps
        :rtype: str
        """
        return json.dumps(self, cls=self.ParseTreeNodeEncoder, **kwargs)

    def __eq__(self, other):
        # TODO: Add check to see that other is a ParseTreeNode.
        if len(self.children) == 0 and len(other.children) == 0:
            eq = self._node_eq(other)
            return eq
        if (len(self.children) == 0 and not len(other.children) == 0) or \
            (not len(self.children) == 0 and len(other.children) == 0):
            return False
        return all([self_child == other_child for (self_child, other_child) in zip(self.children, other.children)])

    def _node_eq(self, other):
        """Test whether a ParseTreeNode is equal to another one.

        :param self: The current object
        :type self: ParseTreeNode
        :param other: The object to compare to
        :type other: ParseTreeNode
        :rtype: bool
        """
        return self.role == other.role and self.raw == other.raw

    def flatten(self):
        """Convert a ParseTreeNode to a flattened string representation.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: str
        """
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
        """Tests whether one tree is a supertree of the other node.

        :param self: The current object
        :type self: ParseTreeNode
        :param other: The object to compare to
        :type other: ParseTreeNode
        :rtype: bool
        """
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
        """Replaces all parameters in a ParseTreeNode tree with generic symbols.

        This function takes a ParseTreeNode tree representing a specific query
        and converts it to a "template" -- the same query with parameters
        replaced with generic symbols.

        :param self: The current object
        :type self: ParseTreeNode
        :param drop_options: Whether or not to remove options
        :type drop_options: bool
        :param drop_rename: Whether or not to drop rename clauses
        :type drop_rename: bool
        :param distinguished_argument: If there is an argument to name 
            differently from other variables
        :type distinguished_argument: str
        :rtype: str
        """
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
        """Return the first node that is an ancestor of this one that has role="STAGE".

        This function traverses up the tree from the current node until it 
        finds a node whose role is "STAGE" and then returns that node. If 
        there is no such node then the function returns None.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
        node = self
        while node:
            if node.role == 'STAGE':
                return node
            node = node.parent
        return None # TODO: Throw error here?

    def drop_options(self):
        """Return a new tree with the subtrees of the current node that represent option parameters removed.

        This function traverses a copy of the subtree starting at the current node and
        removes all subtrees that represent option clauses. It does this by
        removing nodes whose role is "OPTION" or whose role is "EQ" and whose
        first child is "OPTION". The reasoning for why one might want to 
        remove option clauses is that often these are not very important to 
        the functioning of the query so if you wanted to count how many queries
        of a certain type there are you might want to ignore the options when
        doing this accounting.

        This is similar to the drop_rename function.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
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
        """Return a new tree with the subtrees of the current node that represent rename clauses removed.

        This function creates a copy of the tree starting at the current node
        and removes all subtrees from that copy that represent rename clauses.
        This includes nodes whose role is "FUNCTION" and whose raw value is "as".
        The reasoning for why one might want to do this is that renaming is
        something that is often done for asthetic reasons and thus is not
        integral to the transformations the query is applying to the data. So if
        you wanted to tally similarity across a set of queries you might want
        to ignore rename operations.

        This is similar to the drop_options function.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
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
        """Return all argument nodes from the subtree of the current node.

        This function traverses the subtree starting from the current node and
        returns a list of nodes that have is_argument set to True.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: list
        """
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
        """Return a copy of the tree rearranged to correspond to the order operations would be executed in.

        This function creates a copy of the tree starting at the current node
        and rearranges the subtrees so that the operations are in an order
        that more closely corresponds to the order in which they should be
        applied to the data.

        This is an experimental function.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
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
        """Produce a list of operations to apply to execute the given query.

        This function takes a ParseTreeNode representing a query and "compiles"
        it into a list of single transformations to apply to the arguments in 
        the query. It actually returns a dictionary whose keys represent the
        variable to compute and whose values represent the operations needed to
        compute that variable.

        This is an experimental function.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: dict
        """
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
        """Replace a given child node in a tree with another node.

        This function replaces the given child node p with the other node q.

        :param self: The current object
        :type self: ParseTreeNode
        :param p: The child node to remove and replace with another
        :type p: ParseTreeNode
        :param q: The child node to add in place of the other
        :type q: ParseTreeNode
        :rtype: None
        """
        idx = self.children.index(p)
        self.children.remove(p)
        p.parent = None
        self.children.insert(idx, q)
        q.parent = self

    def is_eval_function(self):
        """Returns True if the current node is the start of an eval function.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: bool
        """
        return (self.is_function() and self.raw == 'eval')

    def is_groupby(self):
        """Returns True if the current node is the start of a group by clause.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: bool
        """
        return (self.is_function() and self.raw == 'groupby')

    def is_function(self):
        """Returns True if the current node's role is "FUNCTION".

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: bool
        """
        return self.role == 'FUNCTION'

    def copy_node(self):
        """Make a copy of the current node but not its children.
        
        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
        p = ParseTreeNode(self.role, nodetype=self.nodetype, raw=self.raw, 
                            is_associative=self.is_associative, 
                            is_argument=self.is_argument)
        p.corrected = self.corrected
        p.bound = self.bound
        # TODO: Check that all attributes are copied using inspect or the __dict__.
        return p
    
    def copy_tree(self):
        """Recursively copy the entire tree.
        
        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
        children = map(lambda x: x.copy_tree(), self.children) 
        p = self.copy_node()
        p.values = self.values
        p.add_children(children)
        return p

    def ancestral_branch(self):
        """Return a copy of all the nodes along the current branch above the current node.

        This function traverses up the tree from the current node, while making
        a copy of the nodes along the path, finally returning the top-most node
        on the branch.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
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
        """Return the first node that is an ancestor of the current one and has role="COMMAND".

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
        up = self.parent
        while up:
            if up.role == 'COMMAND':
                return up
            up = up.parent
        return None

    def ancestral_function(self):
        """Return the first node that is an ancestor of the current one and has role="COMMAND" or role="FUNCTION".

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode or None
        """
        up = self.parent
        while up:
            if up.role == 'FUNCTION' or up.role == 'COMMAND':
                return up
            up = up.parent
        return None
        

    def skeleton(self):
        """Return a recursive copy of the tree at the current node with all raw argument values set to blank.

        This function recursively traverses the tree starting at the current 
        node and copies it, while setting all argument values to blank.
        This makes it possible to compare two queries to see if they are the
        same except for their arguments.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
        children = map(lambda x: x.skeleton(), self.children) 
        if self.is_argument:
            p = ParseTreeNode('', is_argument=True)
        else:
            p = ParseTreeNode(self.role, nodetype=self.nodetype, raw=self.raw, is_associative=self.is_associative) 
        p.add_children(children)
        return p

    def inverse_skeleton(self):
        """Return a recursive copy of the tree at the current node with all raw values except argument values set to blank.

        This function recursively traverses the tree starting at the current 
        node and copies it, while setting all non-argument values to blank.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
        children = map(lambda x: x.inverse_skeleton(), self.children) 
        if not self.is_argument:
            p = ParseTreeNode('', is_argument=False)
        else:
            p = ParseTreeNode(self.role, raw=self.raw, is_associative=self.is_associative, is_argument=True)
        p.add_children(children)
        return p

    def command_argument_tuple_list(self):
        """Return a list of (command, arguments) pairs from the subtree starting at the current node.

        Traverse the subtree starting at the current node and extract the
        arguments for each Splunk command, returning a list of
        (command, argument) tuples.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: ParseTreeNode
        """
        stages = self._stage_subtrees()
        command_and_arguments = [stage._command_argument_tuple_from_stage() for stage in stages]
        return command_and_arguments

    def _stage_subtrees(self):
        if not self.role == 'ROOT':
            raise ValueError("This must be 'ROOT' node for this to work properly.\n")
        return self.children

    def _command_argument_tuple_from_stage(self):
        if not self.role == 'STAGE':
            raise ValueError("This must be 'STAGE' node for this to work properly.\n")
        command = self.children[0].skeleton()._flatten_roles_to_string()
        arguments = self.children[0].inverse_skeleton()._flatten_to_list()
        return (command, arguments)

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
        """Add the given ParseTreeNode as a child to the current node.

        :param self: The current object
        :type self: ParseTreeNode
        :param child: The node to add as a child of the current node
        :type child: ParseTreeNode
        :rtype: None
        """
        if self.is_associative and child.raw == self.raw and len(child.children) > 0:
            self.add_children(child.children)
        else:
            self.children.append(child)
        for child in self.children:
            child.parent = self
    
    def add_children(self, children):
        """Add each of the ParseTreeNodes in the given list as a child of the current node.
        
        :param self: The current object
        :type self: ParseTreeNode
        :param children: The nodes to add as children of the current node
        :type children: list
        :rtype: None

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
        """Remove the given ParseTreeNode from the children of the current node.

        :param self: The current object
        :type self: ParseTreeNode
        :param child: The node to remove from the children of the current node
        :type child: ParseTreeNode
        :rtype: None
        """
        self.children.remove(child)
        child.parent = None

    def remove_children(self, children):
        """Remove the given list of ParseTreeNodes from the children of the current node.

        :param self: The current object
        :type self: ParseTreeNode
        :param children: The nodes to remove from the children of the current node
        :type children: list
        :rtype: None
        
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
        """Remove all children from the current node.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: None
        """
        self.children = []

    def __repr__(self):
        """Return a string representation of the current node for debugging purposes.

        Doesn't conform to the recommended guidelines for __repr__ functions.
        This should be fixed.

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
        # TODO: Ensure that the output of this function conforms to the recommended guidelines for __repr__ functions.
        child_repr = ''
        first = True
        for child in self.children:
            if not first:
                child_repr = ''.join([child_repr, ', ', str(child)])
            else:
                child_repr = str(child)
                first = False
        to_repr = ''.join(["ParseTreeNode: ", "{role: '", self.role,\
                            "', raw: '", self.raw,\
                            "', children: [", child_repr,\
                            "], parent: ", str(self.parent), "}"])
        return to_repr

    def __str__(self):
        """Return a human-friendly string representation of the current node only.
       
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
        """Recursively create the string representation of the tree starting at the current node.

        This function recurses through the tree starting at the current node
        and creates a string representation of the tree. Optionally you can
        choose to not have the function recurse into the subtree of the node.

        :param self: The current object
        :type self: ParseTreeNode
        :param recursive: Whether or not to recurse
        :type recursive: bool
        :rtype: str
        """
        return self._str_tree(recursive=recursive)

    def print_tree(self, recursive=True):
        """Print a string representation of the whole tree starting at the current node.
        
        If recursive is set to False, only the current node is printed.

        :param self: The current object
        :type self: ParseTreeNode
        :param recursive: Whether or not to recurse
        :type recursive: bool
        :rtype: None

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
        """Iterate through the entire tree depth-first, yielding nodes along the way.

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: generator
        """
        stack = [self]
        while len(stack) > 0:
            node = stack.pop(0)
            stack = node.children + stack
            yield node

    def schema(self):
        """Return the schema inferred from the query in the subtree starting at the current node.

        This is an experimental function.
        
        :param self: The current object
        :type self: ParseTreeNode
        :rtype: Schema
        """
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
        """Return the estimated data type of the raw value of the current node.
        
        :param self: The current object
        :type self: ParseTreeNode
        :rtype: str
        """
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
        """Return a list of nodes in the subtree starting at the current node that have role="FIELD".

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: list
        """
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
        """Return a list of nodes in the subtree starting at the current node that have role="VALUE".

        :param self: The current object
        :type self: ParseTreeNode
        :rtype: list
        """
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
