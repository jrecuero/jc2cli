from jc2cli.node import Node


class Tree(object):

    __ROOT = None
    __COMMAND_TREE = {}
    __MODE_TREE = {}
    __ACTIVE_CMD_NS = None
    __ACTIVE_MODE_NS = None

    class _Tree(object):

        def __init__(self, name=None):
            self.__db = {}
            self.name = name

        def get_db(self):
            """get_db returns the whole tree database data.
            """
            return self.__db

        def add_node(self, key, node):
            print('Add node {0} to tree {1}'.format(key, self.name))
            if key not in self.__db:
                self.__db[key] = node
            return self.__db[key]

        def rename_node(self, old_key, new_key):
            self.__db[new_key] = self.__db.pop(old_key)
            self.__db[new_key].name = new_key

        def get_node(self, key):
            return self.__db.get(key, None)

    def __new__(cls):
        if cls.__ROOT is None:
            cls.__ROOT = Tree._Tree()
        return cls.__ROOT

    @classmethod
    def root(cls):
        return cls.__new__(cls)

    @classmethod
    def command_tree_namespace(cls, namespace):
        return cls.__COMMAND_TREE[namespace]

    @classmethod
    def command_tree(cls):
        return cls.command_tree_namespace(cls.__ACTIVE_CMD_NS)

    @classmethod
    def set_command_tree(cls, namespace, command_tree):
        cls.__ACTIVE_CMD_NS = namespace
        cls.__COMMAND_TREE[cls.__ACTIVE_CMD_NS] = command_tree
        return cls.__COMMAND_TREE[cls.__ACTIVE_CMD_NS]

    @classmethod
    def extend_command_tree(cls, namespace, command_tree):
        if namespace in cls.__COMMAND_TREE.keys():
            cls.__COMMAND_TREE[namespace].update(command_tree)
            return cls.__COMMAND_TREE[namespace]
        return None

    @classmethod
    def switch_to(cls, namespace):
        if namespace in cls.__COMMAND_TREE.keys():
            cls.__ACTIVE_CMD_NS = namespace
            return True
        else:
            return False

    @classmethod
    def build_command_tree_from_ns_module(cls, ns_module, full_matched=True):
        """build_command_tree_from_ns_module creates a new command tree
        dictionary looking for all commands matching ns_module.
        """
        root = Tree.root()
        # full_matched only for commands under the exactly ns_module.
        if full_matched:
            traverse = {k: v for (k, v) in root.get_db().items() if ns_module == '.'.join(k.split('.')[:-1])}
        else:
            traverse = {k: v for (k, v) in root.get_db().items() if ns_module in k}
        # Command tree can not have duplicated commands (same command name).
        # Check if there are any duplicated command (based on command name).
        assert len(traverse.keys()) == len(set([v.command.name for v in traverse.values()])), 'Duplicated Commands'
        return {v.command.name: v for (k, v) in traverse.items()}

    @classmethod
    def node(cls, name, cb, mode=False):
        root = Tree.root()
        node = root.get_node(name)
        if not node:
            node = Node(name, cb, mode)
            root.add_node(node.name, node)
        return node

    @classmethod
    def fnode(cls, f, cb, mode=False):
        """fnode creates a node based on the qualified name for the
        function callback. It makes use of the module where the callback
        is defined and the callback function qualified name."""
        node_name = '{0}.{1}'.format(f.__module__, f.__qualname__)
        return cls.node(node_name, cb, mode)

    @classmethod
    def start(cls, namespace, ns_module, full_matched=True):
        """start creates a namespace with all commands for the given
        ns_module.
        """
        cls.create(namespace)
        command_tree = cls.build_command_tree_from_ns_module(ns_module, full_matched)
        return cls.set_command_tree(namespace, command_tree)

    @classmethod
    def create(cls, namespace, command_tree=None):
        """create creates a new namespace to be used for a set of commands.
        """
        cls.__COMMAND_TREE[namespace] = command_tree if command_tree else {}

    @classmethod
    def extend(cls, namespace, ns_module, full_matched=True):
        """extend method extends all commands found under the ns_module to the
        given namespace.
        """
        command_tree = cls.build_command_tree_from_ns_module(ns_module, full_matched)
        return cls.extend_command_tree(namespace, command_tree)

    @classmethod
    def extend_with_namespace(cls, namespace_base, namespace_ext):
        """extend_with_namespace extends the given namespace with the command
        tree from the extension namespace.
        """
        command_tree_ext = cls.command_tree_namespace(namespace_ext)
        return cls.extend_command_tree(namespace_base, command_tree_ext)

    @classmethod
    def get_node(cls, command_name):
        return cls.command_tree().get(command_name, None)

    @classmethod
    def run(cls, command_name, *args, **kwargs):

        #  node = cls.get_node(command_name)
        #  if node and node.command:
        #      return node.command.cb(*args, **kwargs)
        # return None
        node = cls.get_node(command_name)
        if node and node.command:
            command = node.command
            line = kwargs.get('line', None)
            if command.rules is None:
                use_args, cli_args = command.build_command_arguments_from_argos(line)
            else:
                cli_args = None
                use_args = command.build_command_arguments_from_syntax(line)
            if use_args is not None:
                if cli_args:
                    return command.cb(*use_args, cli_args)
                else:
                    return command.cb(*use_args)

    @classmethod
    def run_none(cls, command_name, *args, **kwargs):
        """run_none methods execute a callback when it is defined as a class
        method but it does not make use of the class instance in the callback.
        """
        return cls.run(command_name, None, *args, **kwargs)

    @classmethod
    def run_instance(cls, command_name, instance, *args, **kwargs):
        """run_instance methods execute a callback when it is defined as a
        class method. It receives the instance to be used.
        """
        return cls.run(command_name, instance, *args, **kwargs)
