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
from jc2cli.builtin.argos import Int, Str
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
MODULE = 'BUILTIN.commands'
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
def do_clear_recording(ns_handler, start, end):
    end = None if end == -1 else end
    logger.display('clear-recording from {0} to {1}'.format(start, end))
    ns_handler.cli.clear_recording(start, end)
    return True


@icommand('save-recording filename [start]? [end]?')
@help('Save recorded command from [start-end].')
@argo('filename', Str(), None)
@argo('start', Int(), 0)
@argo('end', Int(), -1)
def do_save_recording(ns_handler, filename, start, end):
    end = None if end == -1 else end
    logger.display('save-recording to {0} from {1} to {2}'.format(filename, start, end))
    ns_handler.cli.save_recording(filename, start, end)
    return True


@icommand('import filename')
@help('Import and execute commands from a file')
@argo('filename', Str(), None)
def do_import(ns_handler, filename):
    logger.display('Import and execute commands from {0}'.format(filename))
    ns_handler.cli.load_commands_from_file(filename)
    return True


@icommand('debug [cmd | tree | ns | nscmd]+')
@help('Internal command for CLI application debug')
@argo('cmd', Str(help='command tree structure for command  ...'), '')
@argo('tree', Str(help='commands imported for pattern ... ["." for all]'), '')
@argo('ns', Str(help='namespaces for pattern ... ["." for all]'), '')
@argo('nscmd', Str(help='commands in namespace with pattern ... ["." for all]'), '')
def do_debug_cmd(ns_handler, cmd, tree, ns, nscmd):
    if cmd:
        node = Tree.get_node(cmd)
        if node:
            logger.display(node.command.syntax_root)
    elif tree:
        tree = '' if tree == '.' else tree
        for k, v in Tree.root().get_db().items():
            if tree in k:
                logger.display('{} : {}'.format(k, v))
    elif ns:
        ns = '' if ns == '.' else ns
        for n in Tree.get_all_namespaces():
            if ns in n:
                logger.display('{}'.format(n))
    elif nscmd:
        nscmd = '' if nscmd == '.' else nscmd
        for n in Tree.get_all_namespaces():
            if nscmd in n:
                for k, v in Tree.command_tree_namespace(n).items():
                    logger.display('[{}] {} : {}'.format(n, k, v))
    return True


@command('exit')
@help('Exit')
def do_exit():
    return False


@command('syntax [cmd]?')
@argo('cmd', Str(), 'none')
@help('Display syntax for all commands.')
def do_syntax(cmd):
    for node_instance in Tree.command_tree().values():
        if 'none' == cmd:
            logger.display(node_instance.command.syntax)
        elif node_instance.command.name == cmd:
            command = node_instance.command
            logger.display('\n{}'.format(command.name))
            logger.display('{}\n'.format('-' * len(command.name)))
            logger.display('{}\n\n'.format(command.help))
            logger.display('Syntax')
            logger.display('------\n')
            logger.display('{}\n\n'.format(command.syntax))
            logger.display('Syntax description')
            logger.display('------------------\n')
            for arg in command.arguments.traverse():
                logger.display('{} ({}) : {}\n'.format(arg.name, arg.type.__class__.__name__, arg.completer.help_str))
    return True


@command('help')
@help('Display this help information.')
def do_help():
    for command_name, node_instance in Tree.command_tree().items():
        logger.display('{0} : {1}'.format(command_name, node_instance.command.help))
    return True


class BuiltIns(object):

        @command('exit')
        @help('Exit')
        def do_exit(self):
            return do_exit()

        @command('syntax [cmd]?')
        @help('Display syntax for all commands.')
        @argo('cmd', Str(), 'none')
        def do_syntax(self, cmd):
            return do_syntax(cmd)

        @command('help')
        @help('Display this help information.')
        def do_help(self):
            return do_help()

        @icommand('start-recording')
        @help('Start recording commands.')
        def do_start_recording(self, ns_handler):
            return do_start_recording(ns_handler)

        @icommand('stop-recording')
        @help('Stop recording commands.')
        def do_stop_recording(self, ns_handler):
            return do_stop_recording(ns_handler)

        @icommand('display-recording [start]? [end]?')
        @help('Display recorded command from [start-end].')
        @argo('start', Int(), 0)
        @argo('end', Int(), -1)
        def do_display_recording(self, ns_handler, start, end):
            return do_display_recording(ns_handler, start, end)

        @icommand('clear-recording [start]? [end]?')
        @help('Clear recorded command from [start-end].')
        @argo('start', Int(), 0)
        @argo('end', Int(), -1)
        def do_clear_recording(self, ns_handler, start, end):
            return do_clear_recording(ns_handler, start, end)

        @icommand('save-recording filename [start]? [end]?')
        @help('Save recorded command from [start-end].')
        @argo('filename', Str(), None)
        @argo('start', Int(), 0)
        @argo('end', Int(), -1)
        def do_save_recording(self, ns_handler, filename, start, end):
            return do_save_recording(ns_handler, filename, start, end)

        @icommand('import filename')
        @help('Import and execute commands from a file')
        @argo('filename', Str(), None)
        def do_import(self, ns_handler, filename):
            return do_import(ns_handler, filename)

        @icommand('debug cmd')
        @help('Internal command for CLI application debug')
        @argo('cmd', Str(), None)
        def do_debug_cmd(self, ns_handler, cmd):
            return do_debug_cmd(ns_handler, cmd)


def builtins_namespace():
    return 'jc2cli.builtin.commands'


def class_builtins_namespace():
    return 'jc2cli.builtin.commands.BuiltIns'
