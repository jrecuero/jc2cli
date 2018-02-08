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
from jc2cli.default.handlers import handler
from jc2cli.default.commands import defaults_namespace, class_defaults_namespace


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

    def __init__(self, namespace, context, **kwargs):
        self.namespace = namespace
        self.context = context
        self.ns_module = kwargs.get('ns_module', namespace)
        self.handler = kwargs.get('handler', handler)
        self.handler = partial(self.handler, self)
        self.commands = self.start_commands()
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


class Handler(object):

    def __init__(self):
        self.ns_handlers = {}
        self.context = Context(Tree)

    def new_ns_context(self):
        return Context(self.context.root)

    def create_namespace(self, namespace, **kwargs):
        new_ns_handler = NameSpace(namespace, self.new_ns_context(), **kwargs)
        self.ns_handlers[namespace] = new_ns_handler
        if kwargs.get('with_defaults', True):
            self.extend_namespace(namespace, defaults_namespace())
        if kwargs.get('with_class_defaults', False):
            self.extend_namespace(namespace, class_defaults_namespace())
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
            self.context.root.extend(namespace, ns_extended)
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
