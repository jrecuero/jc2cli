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
from jc2cli.tree import Tree
from jc2cli.decorators import command, help, icommand, argo
from jc2cli.argo_types import Int, Str
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
MODULE = 'CLI.commands'
logger = loggerator.getLoggerator(MODULE)


@icommand('start-recording')
@help('Start recording commands.')
def do_start_recording(ns_handler):
    logger.display('start-recording ...')
    ns_handler.cli.start_recording()
    return True


@icommand('stop-recording')
@help('Stop recording commands.')
def do_stop_recording(ns_handler):
    logger.display('stop-recording ...')
    ns_handler.cli.stop_recording()
    return True


@icommand('display-recording [start]? [end]?')
@help('Display recorded command from [start-end].')
@argo('start', Int(), 0)
@argo('end', Int(), -1)
def do_display_recording(ns_handler, start, end):
    end = None if end == -1 else end
    logger.display('display-recording from {0} to {1}'.format(start, end))
    ns_handler.cli.display_recording(start, end)
    return True


@icommand('clear-recording [start]? [end]?')
@help('Clear recorded command from [start-end].')
@argo('start', Int(), 0)
@argo('end', Int(), -1)
def clear_recording(ns_handler, start, end):
    end = None if end == -1 else end
    logger.display('clear-recording from {0} to {1}'.format(start, end))
    ns_handler.cli.clear_recording(start, end)
    return True


@icommand('save-recording filename [start]? [end]?')
@help('Save recorded command from [start-end].')
@argo('filename', Str(), None)
@argo('start', Int(), 0)
@argo('end', Int(), -1)
def save_recording(ns_handler, filename, start, end):
    end = None if end == -1 else end
    logger.display('save-recording to {0} from {1} to {2}'.format(filename, start, end))
    ns_handler.cli.save_recording(filename, start, end)
    return True


@command('exit')
def do_exit():
    return False


@command('syntax')
@help('Display syntax for all commands.')
def do_syntax():
    for node_instance in Tree.command_tree().values():
        print(node_instance.command.syntax)
    return True


@command('help')
@help('Display this help information.')
def do_help():
    for command_name, node_instance in Tree.command_tree().items():
        print('{0} : {1}'.format(command_name, node_instance.command.help))
    return True


class Defaults(object):

        @command('exit')
        def do_exit(self):
            return do_exit()

        @command('syntax')
        @help('Display syntax for all commands.')
        def do_syntax(self):
            return do_syntax()

        @command('help')
        @help('Display this help information.')
        def do_help(self):
            return do_help()

        @icommand('start-recording')
        @help('Start recording commands.')
        def do_start_recording(self, ns_handler):
            return do_start_recording(ns_handler)


def defaults_namespace():
    return 'jc2cli.default.commands'


def class_defaults_namespace():
    return 'jc2cli.default.commands.Defaults'
