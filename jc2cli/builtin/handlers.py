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
MODULE = 'BUILTIN.handlers'
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
def handler(ns_handler, command_name, *args, **kwargs):
    """handler is the default handler for commands defined as regular
    function.
    """
    root = ns_handler.context.root
    return root.run(command_name, ns_handler, *args, **kwargs)


def handler_instance(ns_handler, instance, command_name, *args, **kwargs):
    """handler_instance is the default handler for commands defined as
    methods in a class.

    The handler will pass the given instance to the command.
    """
    root = ns_handler.context.root
    return root.run_instance(command_name, ns_handler, instance, *args, **kwargs)


def handler_none(ns_handler, command_name, *args, **kwargs):
    """handler_none is the default hadnler for commands defined as method in
    a class that not require to recive an instance.
    """
    root = ns_handler.context.root
    return root.run_instance(command_name, ns_handler, None, *args, **kwargs)


def handler_mode(child_ns_handler, ns_handler, command_name, *args, **kwargs):
    """handler_mode is the default handler that allows to get inside inner
    modes.
    """
    root = ns_handler.context.root
    result = root.run(command_name, ns_handler, *args, **kwargs)
    if result and root.get_node(command_name).is_mode():
        child_ns_handler.switch_and_run(*args, **kwargs)
        ns_handler.switch_to()
    return result


def handler_root(root_handler, ns_handler, command_name, *args, **kwargs):
    root = ns_handler.context.root
    result = root.run(command_name, ns_handler, *args, **kwargs)
    if result and root.get_node(command_name).is_mode():
        mode_ns_handler = root_handler.get_ns_handler(root.get_node(command_name).command.ns_mode)
        mode_ns_handler.switch_and_run(*args, **kwargs)
    return result
