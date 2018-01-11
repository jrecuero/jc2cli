from functools import wraps


class Command(object):

    def __init__(self, cb):
        self.cb = cb
        self._syntax = None
        self.name = None
        self.params = {}

    @property
    def syntax(self):
        return self._syntax

    @syntax.setter
    def syntax(self, value):
        self._syntax = value
        self.name = self.syntax.split()[0]

    def add_param(self, key, value):
        self.params[key] = value


class Node(object):

    def __init__(self, name, cb=None):
        self.name = name
        self.command = Command(cb) if cb else None


class Tree(object):

    __ROOT = None

    class _Tree(object):

        def __init__(self):
            self.db = {}

        def add_node(self, key, node):
            print('Add node {0}'.format(key))
            if key not in self.db:
                self.db[key] = node
            return self.db[key]

        def get_node(self, key):
            return self.db.get(key, None)

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


def command(syntax):

    def command_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        print('called for {}'.format(syntax))
        node = Tree.node(f.__qualname__, _wrapper)
        node.command.syntax = syntax
        return _wrapper
    return command_wrapper


def argo(argo_name, argo_type, argo_default=None):

    def argo_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        print('called for {}'.format(argo_name))
        node = Tree.node(f.__qualname__, _wrapper)
        node.command.add_param(argo_name, (argo_name, argo_type, argo_default))
        return _wrapper
    return argo_wrapper


@command('START app default')
@argo('app', str, "none")
@argo('default', str)
def start():
    print('start')


@command("END time")
@argo('time', int, 0)
def end():
    print('end')


class Cli(object):

    def __init__(self):
        pass

    @command('START app default')
    @argo('app', str, "none")
    @argo('default', str)
    def cli_start(self):
        print('start')

    @command("END time")
    @argo('time', int, 0)
    def cli_end(self):
        print('end')
