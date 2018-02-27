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
from functools import partial
from jc2cli.tree import Tree
from jc2cli.base import Base
from jc2cli.context import Context
import jc2cli.tools.loggerator as loggerator
from jc2cli.builtin.handlers import handler
from jc2cli.builtin.commands import builtins_namespace, class_builtins_namespace


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.namespace'
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
class NameSpace(object):
    """NameSpace class provides a container for storing a set of commands
    available at one point to the user.

    One NameSpace represents one mode. It contains a command namespace and
    a CLI instance for handling all those commands.

    It decouples the command tree from the actual CLI implementation.
    """

    def __init__(self, namespace, context, **kwargs):
        self.namespace = namespace
        self.context = context
        self.ns_module = kwargs.get('ns_module', namespace)
        self.handler = kwargs.get('handler', handler)
        self.handler = partial(self.handler, self)
        self.commands = None
        if kwargs.get('start', False):
            self.commands = self.start_commands()
        else:
            self.context.root.create(self.namespace)
        logger.trace('NameSpace {0} with {1}'.format(self.namespace, self.commands.keys() if self.commands else None))
        self.cli_class = kwargs.get('cli_class', Base)
        self.cli = self.create_cli()

    def start_commands(self):
        """start_commands loads namespace commands as available.
        """
        self.commands = self.context.root.start(self.namespace, self.ns_module)
        return self.commands

    def create_cli(self, *args, **kwargs):
        """create_cli creates a new cli instance.
        """
        self.cli = self.cli_class(self, *args, **kwargs)
        return self.cli

    def run_cli(self, *args, **kwargs):
        """run_cli runs cli instance.
        """
        self.cli.run(*args, **kwargs)

    def switch_to(self):
        """switch_to switches to the namespace.
        """
        self.context.root.switch_to(self.namespace)

    def switch_and_run(self, *args, **kwargs):
        """switch_and_run switches to the namespace and run the cli.
        """
        self.switch_to()
        self.run_cli(*args, **kwargs)

    def update_commands(self, commands):
        """update_commands updates commands with given commands.
        """
        self.commands = commands
        # self.cli.commands = self.commands
        logger.trace('NameSpace {0} with {1}'.format(self.namespace, self.commands.keys() if self.commands else None))
        logger.trace('cli commands {0}'.format(self.cli.commands.keys() if self.cli.commands else None))


class Handler(object):
    """Handler class implements a common handler for all namespaces.
    """

    def __init__(self):
        self.ns_handlers = {}
        self.context = Context(Tree)

    def new_ns_context(self):
        """new_ns_context creates a new namespace context.
        """
        return Context(self.context.root)

    def create_namespace(self, namespace, **kwargs):
        """create_namespace creates a new namespace handler.
        """
        new_ns_handler = NameSpace(namespace, self.new_ns_context(), start=False, **kwargs)
        self.ns_handlers[namespace] = new_ns_handler
        if kwargs.get('is_class_cmd', False):
            self.extend_namespace(namespace, class_builtins_namespace())
        else:
            self.extend_namespace(namespace, builtins_namespace())
        self.ns_module = kwargs.get('ns_module', namespace)
        self.extend_namespace(namespace, self.ns_module)
        return new_ns_handler

    def remove_namespace(self, namespace):
        """remove_namespace removes the given namespace handler.
        """
        if namespace in self.ns_handlers:
            del self.ns_handlers[namespace]

    def get_namespace(self, namespace):
        """get_namespace retrieves the given namespace.
        """
        if namespace in self.ns_handlers:
            return self.ns_handlers[namespace]
        return None

    def extend_namespace(self, namespace, ns_extended):
        """extend_namespace extends the namespace handler with the commands
        from a new namespace module.
        """
        if namespace in self.ns_handlers:
            commands = self.context.root.extend(namespace, ns_extended)
            self.get_namespace(namespace).update_commands(commands)
            return True
        return False

    def switch_to_namespace(self, namespace):
        """switch_to_namespace switches to the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_to()
            return True
        return False

    def switch_and_run_namespace(self, namespace):
        """switch_and_run_namespace switches and run the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_and_run()

    def run_namespace(self, namespace):
        """run_namespace runs the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].run_cli()

    def active_namespace(self):
        """active_namespace retrieves the active namespace in the Tree
        singleton.
        """
        return self.context.root.active_namespace

    def create_and_switch_for_namespace(self, namespace):
        """create_and_switch_for_namespace creates a new namespace, switches to
        that namespace and returns the namespace handler.
        """
        self.create_namespace(namespace)
        self.context.root.switch_to(namespace)
        return self.get_namespace(namespace)

    def create_cli_for_namespace(self, namespace):
        """create_cli_for_namespace creates a new namespace, switches to the
        namespace and return the function that execute commands in the cli.
        """
        self.create_namespace(namespace)
        self.context.root.switch_to(namespace)
        return self.get_namespace(namespace).cli.exec_user_input

    def build_cli_for_namespace(self, namespace):
        """build_cli_for_namespace loads all namespace commands, create a new
        namespace, switches to the namespace and returns the function that
        execute commands in the cli."""
        __import__(namespace)
        return self.create_cli_for_namespace(namespace)

    def run_cli_commands_for_namespace(self, namespace, commands):
        """run_cli_commands_for_namespace runs the given commands for the
        given namespace.
        """
        cli = self.build_cli_for_namespace(namespace)
        for cmd in commands:
            cli(cmd)
