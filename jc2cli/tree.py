from jc2cli.node import Node


class Tree(object):

    __ROOT = None
    __COMMAND_TREE = None

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
    def node(cls, name, cb):
        root = Tree.root()
        node = root.get_node(name)
        if not node:
            node = Node(name, cb)
            root.add_node(node.name, node)
        return node

    @classmethod
    def fnode(cls, f, cb):
        node_name = '{0}.{1}'.format(f.__module__, f.__qualname__)
        return cls.node(node_name, cb)

    @classmethod
    def start(cls, namespace):
        root = Tree.root()
        traverse = {k: v for (k, v) in root.get_db().items() if namespace in k}
        # Command tree can not have duplicated commands (same command name).
        # Check if there are any duplicated command (based on command name).
        assert len(traverse.keys()) == len(set([v.command.name for v in traverse.values()])), 'Duplicated Commands'
        cls.__COMMAND_TREE = {v.command.name: v for (k, v) in traverse.items()}
        return cls.__COMMAND_TREE
