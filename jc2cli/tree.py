__docformat__ = 'restructuredtext en'

# -----------------------------------------------------------------------------
#  _                            _
# (_)_ __ ___  _ __   ___  _ __| |_ ___
# | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
# | | | | | | | |_) | (_) | |  | |_\__ \
# |_|_| |_| |_| .__/ \___/|_|   \__|___/
#             |_|
# -----------------------------------------------------------------------------
#
from jc2cli.node import Node
from jc2cli.error_handler import CliError
import jc2cli.tools.loggerator as loggerator


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.tree'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class Tree(object):
    """Tree class contains all class methods required to access all loaded commands.

    Tree contains one single instace for the inner class _Tree, where all commands
    are stored. Every command is fully identified by its module [and class name] and
    function or method name. That information is contained in what is called as
    a Node.

    Active commands available to be used are stored in the __COMMAND_TREE dictionary,
    using 'namespace' as key to identify every set of commands.

    Commands have to be loaded from the Tree.root() to the __COMMAND_TREE in order
    to be able to access to them.
    """

    __ROOT = None
    __COMMAND_TREE = {}
    __ACTIVE_CMD_NS = None
    # __MODE_TREE = {}
    # __ACTIVE_MODE_NS = None

    class _Tree(object):

        def __init__(self, name=None):
            self.__db = {}
            self.name = name

        def get_db(self):
            """get_db returns the whole tree database data.
            """
            return self.__db

        def add_node(self, key, node):
            """add_node adds a node to the node database.
            """
            logger.trace('node {0} to tree {1}'.format(key, self.name))
            if key not in self.__db:
                self.__db[key] = node
            return self.__db[key]

        def rename_node(self, old_key, new_key):
            """rename_node renames a node from the node database.
            """
            self.__db[new_key] = self.__db.pop(old_key)
            self.__db[new_key].name = new_key

        def get_node(self, key):
            """get_node retrieves a node from the node database.
            """
            return self.__db.get(key, None)

    def __new__(cls):
        """__new___ creates a singleton for the Tree class."""
        if cls.__ROOT is None:
            cls.__ROOT = Tree._Tree()
        return cls.__ROOT

    @classmethod
    def root(cls):
        """root creates or retrieves the Tree singleton.
        """
        return cls.__new__(cls)

    @classmethod
    def node(cls, name, cb, mode=False):
        """node adds/retrieves a node to/from the node tree.

        The node is identified by the node name, if the node is already
        present in the node tree, it retrieves the node instead of adding
        it.
        """
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
    def command_tree_namespace(cls, namespace):
        """command_tree_namespace retrieves all commands for the given
        namespace.
        """
        # return cls.__COMMAND_TREE[namespace]
        return {k: v for k, v in cls.__COMMAND_TREE[namespace].items() if v.is_usable()}

    @classmethod
    def active_namespace(cls):
        """active_namespace returns the active namespace.
        """
        return cls.__ACTIVE_CMD_NS

    @classmethod
    def set_active_namespace(cls, namespace):
        """set_active_namespace sets the active namespace to the given
        namespace.
        """
        cls.__ACTIVE_CMD_NS = namespace

    @classmethod
    def command_tree(cls):
        """command_tree retrieves all commands for the active namespace.
        """
        return cls.command_tree_namespace(cls.active_namespace())

    @classmethod
    def set_command_tree(cls, namespace, command_tree):
        """set_command_tree assigns all given commands to the given namespace
        and set the namespace as the active one.
        """
        cls.set_active_namespace(namespace)
        cls.__COMMAND_TREE[cls.active_namespace()] = command_tree
        return cls.command_tree()

    @classmethod
    def get_all_namespaces(cls):
        """get_command_tree_names retrieves all configures namespaces names.
        """
        return cls.__COMMAND_TREE.keys()

    @classmethod
    def extend_command_tree(cls, namespace, command_tree):
        """extend_command_tree extends the given namespace adding all given
        commands.
        """
        if namespace in cls.get_all_namespaces():
            logger.trace('namespace {0} with {1}'.format(namespace, command_tree.keys()))
            cls.__COMMAND_TREE[namespace].update(command_tree)
            return cls.command_tree_namespace(namespace)
        return None

    @classmethod
    def switch_to(cls, namespace):
        """switch_to switches to the given namespace as the active one.
        """
        if namespace in cls.get_all_namespaces():
            cls.set_active_namespace(namespace)
            return True
        else:
            return False

    @classmethod
    def import_ns_module(cls, ns_module):
        """import_ns_module imports all commands from the ns_module.

        Commands will be loaded in the Tree.roo() dictionary, they will be
        available to be loaded in the command tree.
        """
        __import__(ns_module)

    @classmethod
    def build_command_tree_from_ns_module(cls, ns_module, matched=True):
        """build_command_tree_from_ns_module creates a new command tree
        dictionary looking for all commands matching ns_module.
        """
        root = Tree.root()
        # matched only for commands under the exactly ns_module.
        if matched:
            traverse = {k: v for (k, v) in root.get_db().items() if ns_module == '.'.join(k.split('.')[:-1])}
        else:
            traverse = {k: v for (k, v) in root.get_db().items() if ns_module in k}
        # Command tree can not have duplicated commands (same command name).
        # Check if there are any duplicated command (based on command name).
        assert len(traverse.keys()) == len(set([v.command.name for v in traverse.values()])), 'Duplicated Commands'
        logger.trace('ns_module {0} : {1}'.format(ns_module, traverse.keys()))
        return {v.command.name: v for (k, v) in traverse.items()}

    @classmethod
    def start(cls, namespace, ns_module, matched=True, import_ns=False):
        """start creates a namespace with all commands for the given
        ns_module.
        """
        if import_ns:
            cls.import_ns_module(ns_module)
        cls.create(namespace)
        command_tree = cls.build_command_tree_from_ns_module(ns_module, matched)
        return cls.set_command_tree(namespace, command_tree)

    @classmethod
    def create(cls, namespace, command_tree=None):
        """create creates a new namespace to be used for a set of commands.
        """
        cls.__COMMAND_TREE[namespace] = command_tree if command_tree else {}

    @classmethod
    def extend(cls, namespace, ns_module, matched=True):
        """extend method extends all commands found under the ns_module to the
        given namespace.
        """
        command_tree = cls.build_command_tree_from_ns_module(ns_module, matched)
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
        """get_node retrieved a node from the node tree.
        """
        return cls.command_tree().get(command_name, None)

    @classmethod
    def get_command(cls, command_name):
        """get_command retrieved the command from a node.
        """
        node = cls.get_node(command_name)
        if node:
            return node.command
        return None

    @classmethod
    def setup_args_for_run_command(cls, command_name, *args, **kwargs):
        """setup_args_for_run_command configures arguments to be passed to the command
        based in the command line input.
        """
        command = cls.get_command(command_name)
        use_args = None
        if command:
            line = kwargs.get('line', None)
            if command.rules is None:
                raise CliError('Command {0} does not have syntax.'.format(command.name))
            elif command.is_lined():
                use_args = [line, ]
            else:
                use_args = command.build_command_arguments_from_syntax(line)
            command.run_with_args = use_args
        return command, use_args

    @classmethod
    def run(cls, command_name, ns_handler, *args, **kwargs):
        """run executes the callback from a command node.
        """
        result = None
        command = cls.get_command(command_name)
        if command:
            if command.run_with_args is not None:
                use_args = command.run_with_args
            else:
                _, use_args = cls.setup_args_for_run_command(command_name, *args, **kwargs)
            if use_args is not None:
                if command.internal:
                    args = list(args)
                    args.append(ns_handler)
                result = command.cb(*args, *use_args)
                command.run_with_args = None
        return result

    @classmethod
    def run_none(cls, command_name, ns_handler, *args, **kwargs):
        """run_none methods execute a callback when it is defined as a class
        method but it does not make use of the class instance in the callback.
        """
        return cls.run(command_name, ns_handler, None, *args, **kwargs)

    @classmethod
    def run_instance(cls, command_name, ns_handler, instance, *args, **kwargs):
        """run_instance methods execute a callback when it is defined as a
        class method. It receives the instance to be used.
        """
        return cls.run(command_name, ns_handler, instance, *args, **kwargs)
