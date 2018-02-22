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
        self.commands = self.context.root.start(self.namespace, self.ns_module)
        return self.commands

    def create_cli(self, *args, **kwargs):
        self.cli = self.cli_class(self, *args, **kwargs)
        return self.cli

    def run_cli(self, *args, **kwargs):
        self.cli.run(*args, **kwargs)

    def switch_to(self):
        self.context.root.switch_to(self.namespace)

    def switch_and_run(self, *args, **kwargs):
        self.switch_to()
        self.run_cli(*args, **kwargs)

    def update_commands(self, commands):
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
        return Context(self.context.root)

    def create_namespace(self, namespace, **kwargs):
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
        if namespace in self.ns_handlers:
            del self.ns_handlers[namespace]

    def get_namespace(self, namespace):
        if namespace in self.ns_handlers:
            return self.ns_handlers[namespace]
        return None

    def extend_namespace(self, namespace, ns_extended):
        if namespace in self.ns_handlers:
            commands = self.context.root.extend(namespace, ns_extended)
            self.get_namespace(namespace).update_commands(commands)
            return True
        return False

    def swith_to_namespace(self, namespace):
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_to()
            return True
        return False

    def switch_and_run_namespace(self, namespace):
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_and_run()

    def run_namespace(self, namespace):
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].run_cli()

    def active_namespace(self):
        return self.context.root.active_namespace
