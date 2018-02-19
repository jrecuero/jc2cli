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
from functools import wraps
from jc2cli.tree import Tree
from jc2cli.arguments import Argument
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
MODULE = 'CLI.decorators'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#
def _command(f, wrapper, syntax, namespace, internal=False):
    """_command implements common functionality for @command and @icommand
    decorators.
    """
    logger.display('command : syntax : {0}'.format(syntax))
    node = Tree.fnode(f, wrapper)
    node.command.syntax = syntax
    node.command.internal = internal
    if namespace:
        Tree().rename_node(node.name, '{0}.{1}'.format(namespace, f.__qualname__))
    node.command.build_command_parsing_tree()


def _mode(f, wrapper, syntax, ns_mode, namespace, internal=False):
    """_mode implements common functionality for @mode and @imode
    decorators.
    """
    logger.display('mode : syntax : {0} : namespace {1}'.format(syntax, ns_mode))
    node = Tree.fnode(f, wrapper, mode=True)
    node.command.syntax = syntax
    node.command.namespace = ns_mode
    node.command.internal = internal
    if namespace:
        Tree().rename_node(node.name, '{0}.{1}'.format(namespace, f.__qualname__))
    node.command.build_command_parsing_tree()


def command(syntax, namespace=None):
    """command decorator creates a new command.
    """

    def command_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        _command(f, _wrapper, syntax, namespace)
        return _wrapper
    return command_wrapper


def icommand(syntax, namespace=None):
    """icommand decorator creates a new internal command.

    Internal command receives one extra parameter, namespace handler.
    """

    def command_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        _command(f, _wrapper, syntax, namespace, internal=True)
        return _wrapper
    return command_wrapper


def mode(syntax, ns_mode, namespace=None):
    """mode decorator creates a new mode.
    """

    def mode_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        _mode(f, _wrapper, syntax, ns_mode, namespace)
        return _wrapper
    return mode_wrapper


def imode(syntax, ns_mode, namespace=None):
    """imode decorator creates a new internal mode.

    Internal mode receives one extra parameter, namespace handler.
    """

    def mode_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        _mode(f, _wrapper, syntax, ns_mode, namespace, internal=True)
        return _wrapper
    return mode_wrapper


def argo(argo_name, argo_type, argo_default=None):
    """argo decorator adds a new argument to a command or mode.
    """

    def argo_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        logger.display('called for {0}'.format(argo_name))
        node = Tree.fnode(f, _wrapper)
        argument = Argument(argo_name, argo_type, default=argo_default)
        node.command.add_argument(argument)
        return _wrapper
    return argo_wrapper


def help(help_str):
    """help decorator adds help description to a command or mode.
    """

    def help_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        node = Tree.fnode(f, _wrapper)
        node.command.help = help_str
        return _wrapper
    return help_wrapper
