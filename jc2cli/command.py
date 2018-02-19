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
import shlex
from jc2cli.arguments import Arguments
from jc2cli.error_handler import CliError
import jc2cli.parser.syntax_parser as syntax_parser
import jc2cli.tools.loggerator as loggerator
from jc2cli.parser.node import Start, PrefixNode
from jc2cli.parser.rules import RuleHandler as RH


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.command'
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
class Command(object):

    def __init__(self, cb):
        self.cb = cb
        self._syntax = None
        self.syntax_root = None
        self.name = None
        self.help = None
        self.rules = None
        self.internal = False
        self.arguments = Arguments()

    def __str__(self):
        return '{0}:{1}'.format(self.__class__.__name__, self.name)

    @property
    def syntax(self):
        return self._syntax

    @syntax.setter
    def syntax(self, value):
        self._syntax = value
        _, self.rules = syntax_parser.process_syntax(value)
        self.name = self.syntax.split()[0]

    def add_argument(self, argument):
        """add_argument adds a new argument to the command.
        """
        self.arguments.insert_argument(argument)

    def len_arguments(self):
        """len_arguments returns the command number of arguments.
        """
        return self.arguments.len()

    def is_lined(self):
        """is_lined checks if the commands has any Line argument.
        """
        for x in self.arguments.traverse():
            if x.is_lined():
                return True
        return False

    def build_command_parsing_tree(self):
        """build_commands_parsing_tree buildsthe command parsing tree using
        the command arguments and the command syntax.

        Returns:
            boolean: True if syntax tree is created, None else.
        """
        root = Start()
        if self.arguments:
            self.arguments.index()
            trav = root
            for rule in self.rules:
                new_trav = trav.build_children_node_from_rule(rule, self.arguments)
                trav = new_trav
            self.syntax_root = root
            return root
        return None

    def get_cli_args(self, line):
        """get_cli_args retrieves the command arguments stored in the command
        function and provided by @argo and @argos decorators; and the arguments
        passed by the user in the command line.

        Returns:
            :any:`list`: cli arguments.
        """
        if self.arguments is not None:
            self.arguments.index()
            try:
                if line.count('"') % 2 == 1:
                    line = line.replace('"', '*')
                cli_args = shlex.split(line)
                return cli_args
            except ValueError:
                return None
        return None

    def map_passed_args_to_command_arguments(self, cli_args):
        """map_passes_args_to_commands_arguments uses the command arguments
        and argument values passed by the user in the CLI, map those using
        the command parsing tree in order to generate all arguments to be
        passed to the command function.

        Args:
            root (node): node where mapping should starts.
            cmd_argos (list): list with command arguments.
            cli_args (list): list with CLI arguments.

        Returns:
            :any:`list` : List with arguments being used.
        """
        node_path = self.syntax_root.find_path(cli_args)
        matched_nodes = list()
        is_prefix = False
        for node, value in zip(node_path, cli_args):
            is_node_prefix = isinstance(node, PrefixNode)
            if is_prefix and is_node_prefix:
                raise CliError(MODULE, 'Value not provided for optional argument')
            elif not is_node_prefix:
                is_prefix = False
            is_prefix = isinstance(node, PrefixNode)
            arg_value = node.map_arg_to_value(value)
            node.store_value_in_argo(arg_value, node in matched_nodes)
            matched_nodes.append(node)
        if is_prefix:
            raise CliError(MODULE, 'Value not provided for optional argument')
        use_args = self.arguments.get_indexed_values()
        return use_args

    def build_command_arguments_from_syntax(self, line):
        """build_command_arguments_syntax builds arguments to be passed to the
        command function.

        Returns:
            list: list with argument to be passed to the command function.
        """
        cli_args = self.get_cli_args(line)
        if len(cli_args)  < RH.syntax_min_args(self.rules):
            raise CliError(MODULE, "Number of Args: Too few arguments")

        use_args = self.map_passed_args_to_command_arguments(cli_args)
        if use_args is None:
            raise CliError(MODULE, 'Incorrect arguments')
        if not all(map(lambda x: x is not None, use_args)):
            raise CliError(MODULE, 'Mandatory argument is not present')
        return use_args
