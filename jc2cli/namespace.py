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
from jc2cli.builtin.handlers import handler, handler_none, handler_instance
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

    ns_module should match the part of the module that contains all commands
    that we want to run. namespace could be equal to the ns_module, that is
    done by default, or could be any other value if we don't want to expose
    the full module path.

    module: exmaples.work.main
    ns_module: example.work.main.Cli
    namespae: main-cli

    module is only required if __import__ has to be called.
    """

    def __init__(self, namespace, context, **kwargs):
        self.namespace = namespace
        self.context = context
        self.ns_module = kwargs.get('ns_module', namespace)
        self.module = kwargs.get('module', self.ns_module)
        self.matched = kwargs.get('matched', True)
        if kwargs.get('import_ns', False):
            __import__(self.module)
        self.handler, self._class_cmd_obj = self._get_handler(**kwargs)
        self.commands = None
        if kwargs.get('start', False):
            self.commands = self.start_commands()
        else:
            self.context.root.create(self.namespace)
        logger.trace('NameSpace {0} with {1}'.format(self.namespace, self.commands.keys() if self.commands else None))
        self.cli_class = kwargs.get('cli_class', Base)
        self.cli = self.create_cli(**kwargs)

    def _get_handler(self, **kwargs):
        class_cmd_obj = kwargs.get('class_cmd_obj', None)
        if kwargs.get('is_class_cmd', False):
            default_handler = handler_none
        elif class_cmd_obj:
            default_handler = handler_instance
        else:
            default_handler = handler
        hdlr = kwargs.get('handler', default_handler)
        hdlr = partial(hdlr, self)
        if class_cmd_obj:
            hdlr = partial(hdlr, class_cmd_obj)
        return hdlr, class_cmd_obj

    def start_commands(self):
        """start_commands loads namespace commands as available.
        """
        self.commands = self.context.root.start(self.namespace, self.ns_module, self.matched)
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

    def extend(self, ns_extended):
        """extend extends the namespace with the commands from a new
        namespace module.
        """
        commands = self.context.root.extend(self.namespace, ns_extended, self.matched)
        self.update_commands(commands)
        return True


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
        if kwargs.get('is_class_cmd', False) or kwargs.get('class_cmd_obj', False):
            self.extend_namespace(namespace, class_builtins_namespace())
        else:
            self.extend_namespace(namespace, builtins_namespace())
        ns_module = kwargs.get('ns_module', namespace)
        self.extend_namespace(namespace, ns_module)
        return new_ns_handler

    def remove_namespace(self, namespace):
        """remove_namespace removes the given namespace handler.
        """
        if namespace in self.ns_handlers:
            del self.ns_handlers[namespace]

    def get_ns_handler(self, namespace):
        """get_ns_handler retrieves the given namespace.
        """
        if namespace in self.ns_handlers:
            return self.ns_handlers[namespace]
        return None

    def extend_namespace(self, namespace, ns_extended):
        """extend_namespace extends the namespace handler with the commands
        from a new namespace module.
        """
        if namespace in self.ns_handlers:
            return self.get_ns_handler(namespace).extend(ns_extended)
        return False

    def switch_to_namespace(self, namespace):
        """switch_to_namespace switches to the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_to()
            return True
        return False

    def switch_and_run_cli_for_namespace(self, namespace, **kwargs):
        """switch_and_run_cli_for_namespace switches and run the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].switch_and_run(**kwargs)

    def run_cli_for_namespace(self, namespace, **kwargs):
        """run_cli_for_namespace runs the given namespace.
        """
        if namespace in self.ns_handlers:
            self.ns_handlers[namespace].run_cli(**kwargs)

    def active_namespace(self):
        """active_namespace retrieves the active namespace in the Tree
        singleton.
        """
        return self.context.root.active_namespace

    def get_ns_handler_after_create_and_switch(self, namespace, **kwargs):
        """get_ns_handler_after_create_and_switch creates a new namespace, switches to
        that namespace and returns the namespace handler.
        """
        self.create_namespace(namespace, **kwargs)
        self.context.root.switch_to(namespace)
        return self.get_ns_handler(namespace)

    def get_cli_exec_after_create_and_switch(self, namespace, **kwargs):
        """get_cli_exec_after_create_and_switch creates a new namespace, switches to the
        namespace and return the function that execute commands in the cli.
        """
        self.create_namespace(namespace, **kwargs)
        self.context.root.switch_to(namespace)
        return self.get_ns_handler(namespace).cli.exec_user_input

    def get_cli_exec_after_build_namespace(self, namespace, **kwargs):
        """get_cli_exec_after_build_namespace loads all namespace commands, create a new
        namespace, switches to the namespace and returns the function that
        execute commands in the cli."""
        kwargs['import_ns'] = True
        return self.get_cli_exec_after_create_and_switch(namespace, **kwargs)

    def run_cli_commands_for_namespace(self, namespace, commands, **kwargs):
        """run_cli_commands_for_namespace runs the given commands for the
        given namespace.
        """
        cli = self.get_cli_exec_after_build_namespace(namespace, **kwargs)
        for cmd in commands:
            cli(cmd)
